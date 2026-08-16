"""Geometry Nodes modifier helpers."""

from __future__ import annotations

import bpy

from .primitives import Parameter, PrimitiveSpec

GROUP_INPUT_X = -240
GROUP_OUTPUT_X = 520
GROUP_VERSION = 7


def ensure_node_group(spec: PrimitiveSpec):
    group = bpy.data.node_groups.get(spec.node_group)
    if group is None:
        group = bpy.data.node_groups.new(spec.node_group, "GeometryNodeTree")
        group.is_modifier = True
        group.use_fake_user = True
        _build_group(group, spec)
    else:
        _ensure_interface(group, spec)
        if group.get("ps_group_version") != GROUP_VERSION:
            _build_group(group, spec)
    group["ps_primitive"] = spec.key
    group["ps_group_version"] = GROUP_VERSION
    return group


def modifier_values(modifier, spec: PrimitiveSpec) -> dict[str, float | int | bool]:
    values = {}
    for parameter in spec.parameters:
        identifier = socket_identifier(modifier.node_group, parameter.name)
        raw_value = modifier.get(identifier, parameter.default)
        values[parameter.name] = _coerce_value(raw_value, parameter)
    return values


def set_modifier_defaults(modifier, spec: PrimitiveSpec) -> None:
    for parameter in spec.parameters:
        identifier = socket_identifier(modifier.node_group, parameter.name)
        modifier[identifier] = parameter.default


def socket_identifier(group, socket_name: str) -> str:
    for item in group.interface.items_tree:
        if getattr(item, "item_type", None) == "SOCKET" and item.name == socket_name:
            return item.identifier
    return socket_name


def _build_group(group, spec: PrimitiveSpec) -> None:
    group.nodes.clear()
    _ensure_interface(group, spec)
    input_node = group.nodes.new("NodeGroupInput")
    output_node = group.nodes.new("NodeGroupOutput")
    set_position = group.nodes.new("GeometryNodeSetPosition")
    input_node.location.x = GROUP_INPUT_X
    output_node.location.x = GROUP_OUTPUT_X
    set_position.location.x = 220

    if "Geometry" in input_node.outputs and "Geometry" in set_position.inputs:
        group.links.new(input_node.outputs["Geometry"], set_position.inputs["Geometry"])
    if "Geometry" in set_position.outputs and "Geometry" in output_node.inputs:
        group.links.new(set_position.outputs["Geometry"], output_node.inputs["Geometry"])

    zero_value = _combined_zero_value(group, input_node, spec)
    if zero_value and "Offset" in set_position.inputs:
        combine_xyz = group.nodes.new("ShaderNodeCombineXYZ")
        combine_xyz.location.x = 0
        combine_xyz.location.y = -280
        group.links.new(zero_value, combine_xyz.inputs["X"])
        group.links.new(combine_xyz.outputs["Vector"], set_position.inputs["Offset"])


def _combined_zero_value(group, input_node, spec: PrimitiveSpec):
    value_output = None
    y = -120
    for parameter in spec.parameters:
        if parameter.socket_type not in {"NodeSocketFloat", "NodeSocketInt"}:
            continue
        if parameter.name not in input_node.outputs:
            continue
        if value_output is None:
            value_output = input_node.outputs[parameter.name]
            continue
        add_node = group.nodes.new("ShaderNodeMath")
        add_node.operation = "ADD"
        add_node.location.x = -120
        add_node.location.y = y
        y -= 80
        group.links.new(value_output, add_node.inputs[0])
        group.links.new(input_node.outputs[parameter.name], add_node.inputs[1])
        value_output = add_node.outputs[0]

    if value_output is None:
        return None

    zero_node = group.nodes.new("ShaderNodeMath")
    zero_node.operation = "MULTIPLY"
    zero_node.inputs[1].default_value = 0.0
    zero_node.location.x = -120
    zero_node.location.y = y
    group.links.new(value_output, zero_node.inputs[0])
    return zero_node.outputs[0]


def _ensure_interface(group, spec: PrimitiveSpec) -> None:
    desired_inputs = {"Geometry", *(parameter.name for parameter in spec.parameters)}
    for item in list(group.interface.items_tree):
        if (
            getattr(item, "item_type", None) == "SOCKET"
            and item.in_out == "INPUT"
            and item.name not in desired_inputs
        ):
            group.interface.remove(item)

    existing_inputs = {
        item.name: item
        for item in group.interface.items_tree
        if getattr(item, "item_type", None) == "SOCKET" and item.in_out == "INPUT"
    }
    existing_outputs = {
        item.name: item
        for item in group.interface.items_tree
        if getattr(item, "item_type", None) == "SOCKET" and item.in_out == "OUTPUT"
    }
    if "Geometry" not in existing_inputs:
        group.interface.new_socket(name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    if "Geometry" not in existing_outputs:
        group.interface.new_socket(name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    for parameter in spec.parameters:
        if parameter.name in existing_inputs:
            _configure_socket(existing_inputs[parameter.name], parameter)
        else:
            socket = group.interface.new_socket(name=parameter.name, in_out="INPUT", socket_type=parameter.socket_type)
            _configure_socket(socket, parameter)


def _configure_socket(socket, parameter: Parameter) -> None:
    socket.description = parameter.description
    if hasattr(socket, "default_value"):
        socket.default_value = parameter.default
    if parameter.min_value is not None and hasattr(socket, "min_value"):
        socket.min_value = parameter.min_value
    if parameter.max_value is not None and hasattr(socket, "max_value"):
        socket.max_value = parameter.max_value
    if parameter.subtype and hasattr(socket, "subtype"):
        socket.subtype = parameter.subtype


def _coerce_value(value, parameter: Parameter):
    if parameter.socket_type == "NodeSocketBool":
        return bool(value)
    if parameter.socket_type == "NodeSocketInt":
        coerced = int(value)
    else:
        coerced = float(value)
    if parameter.min_value is not None and coerced < parameter.min_value:
        coerced = parameter.min_value
    if parameter.max_value is not None and coerced > parameter.max_value:
        coerced = parameter.max_value
    return coerced
