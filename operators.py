"""Operators, menu integration, and update handling."""

from __future__ import annotations

import bpy
from bpy.app.handlers import persistent
from bpy.types import Operator

from .nodes import ensure_node_group, modifier_values, set_modifier_defaults
from .primitives import SPECS, SPECS_BY_KEY, generate_points

MODIFIER_NAME = "Parametric Curve"
OBJECT_KIND_PROP = "ps_primitive"
SIGNATURE_PROP = "ps_signature"
UPDATING = False
UPDATE_TIMER_INTERVAL = 0.05


def create_curve_object(context, spec):
    curve = bpy.data.curves.new(spec.label, "CURVE")
    curve.dimensions = spec.dimensions
    curve.resolution_u = 12
    curve.bevel_depth = 0.0
    curve.fill_mode = _fill_mode_for_dimensions(spec.dimensions)

    obj = bpy.data.objects.new(spec.label, curve)
    context.collection.objects.link(obj)
    obj[OBJECT_KIND_PROP] = spec.key

    context.view_layer.objects.active = obj
    obj.select_set(True)

    modifier = obj.modifiers.new(MODIFIER_NAME, "NODES")
    modifier.node_group = ensure_node_group(spec)
    set_modifier_defaults(modifier, spec)
    update_curve_object(obj)
    return obj


def update_curve_object(obj) -> None:
    kind = obj.get(OBJECT_KIND_PROP)
    if kind not in SPECS_BY_KEY or obj.type != "CURVE":
        return

    modifier = _parametric_modifier(obj)
    if modifier is None or modifier.node_group is None:
        return

    spec = SPECS_BY_KEY[kind]
    values = modifier_values(modifier, spec)
    signature = repr((kind, tuple(sorted(values.items()))))
    if obj.get(SIGNATURE_PROP) == signature:
        return

    obj.data.dimensions = spec.dimensions
    obj.data.fill_mode = _fill_mode_for_dimensions(spec.dimensions)
    points, cyclic = generate_points(kind, values)
    _replace_curve_spline(obj.data, points, cyclic)
    obj[SIGNATURE_PROP] = signature


def _replace_curve_spline(curve, points, cyclic: bool) -> None:
    curve.splines.clear()
    if len(points) < 2:
        return
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (co[0], co[1], co[2], 1.0)
    spline.use_cyclic_u = cyclic
    spline.use_smooth = False


def _fill_mode_for_dimensions(dimensions: str) -> str:
    return "BOTH" if dimensions == "2D" else "FULL"


def _parametric_modifier(obj):
    for modifier in obj.modifiers:
        if modifier.type == "NODES" and modifier.name.startswith(MODIFIER_NAME):
            return modifier
    return None


class PARAMETRIC_SPLINES_OT_add(Operator):
    bl_idname = "curve.parametric_curve_add"
    bl_label = "Add Parametric Curve"
    bl_options = {"REGISTER", "UNDO"}

    primitive: bpy.props.EnumProperty(
        name="Primitive",
        items=[(spec.key, spec.label, "") for spec in SPECS],
    )

    def execute(self, context):
        create_curve_object(context, SPECS_BY_KEY[self.primitive])
        return {"FINISHED"}


def curve_add_menu(self, context):
    layout = self.layout
    layout.label(text="Parametric Curves", icon="CURVE_DATA")
    for spec in SPECS:
        operator = layout.operator(PARAMETRIC_SPLINES_OT_add.bl_idname, text=spec.label)
        operator.primitive = spec.key
    layout.separator()


@persistent
def depsgraph_update(scene, depsgraph):
    global UPDATING
    if UPDATING:
        return
    UPDATING = True
    try:
        for obj in _updated_parametric_objects(scene, depsgraph):
            update_curve_object(obj)
    finally:
        UPDATING = False


def timer_update():
    if UPDATING:
        return UPDATE_TIMER_INTERVAL
    obj = bpy.context.object
    if obj and obj.get(OBJECT_KIND_PROP):
        update_curve_object(obj)
    return UPDATE_TIMER_INTERVAL


def _updated_parametric_objects(scene, depsgraph):
    objects = []
    seen = set()

    def add_object(obj):
        if obj and obj.get(OBJECT_KIND_PROP) and obj.name not in seen:
            objects.append(obj)
            seen.add(obj.name)

    for update in depsgraph.updates:
        datablock = update.id
        if isinstance(datablock, bpy.types.Curve):
            for obj in scene.objects:
                if obj.type == "CURVE" and obj.data == datablock:
                    add_object(obj)

    # Modifier socket edits may not appear in depsgraph.updates, or may be
    # accompanied by unrelated updates. In normal UI use, the edited object is
    # active, and unchanged signatures exit cheaply.
    add_object(bpy.context.object)

    return objects


classes = (
    PARAMETRIC_SPLINES_OT_add,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_curve_add.prepend(curve_add_menu)
    if depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(depsgraph_update)
    if not bpy.app.timers.is_registered(timer_update):
        bpy.app.timers.register(timer_update, persistent=True)


def unregister():
    if bpy.app.timers.is_registered(timer_update):
        bpy.app.timers.unregister(timer_update)
    if depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(depsgraph_update)
    try:
        bpy.types.VIEW3D_MT_curve_add.remove(curve_add_menu)
    except ValueError:
        pass
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
