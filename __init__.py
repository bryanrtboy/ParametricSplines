"""Parametric Splines Blender extension."""

from . import operators

bl_info = {
    "name": "Parametric Splines",
    "author": "Bryan Leister",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "Add > Curve > Parametric Splines",
    "description": "Persistent, non-destructive curve primitives with modifier controls.",
    "category": "Add Curve",
}


def register():
    operators.register()


def unregister():
    operators.unregister()
