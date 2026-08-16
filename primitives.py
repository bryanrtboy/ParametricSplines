"""Curve point generation for Parametric Splines."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin

TAU = pi * 2.0
EPSILON = 1.0e-5
RIGHT_ANGLE = pi / 2.0
MAX_ANGLE = TAU * 10.0


@dataclass(frozen=True)
class Parameter:
    name: str
    socket_type: str
    default: float | int | bool
    min_value: float | int | None = None
    max_value: float | int | None = None
    subtype: str | None = None
    description: str = ""


@dataclass(frozen=True)
class PrimitiveSpec:
    key: str
    label: str
    node_group: str
    parameters: tuple[Parameter, ...]
    cyclic: bool
    dimensions: str = "2D"


SPECS: tuple[PrimitiveSpec, ...] = (
    PrimitiveSpec("ARC", "Arc", "PS_Arc", (
        Parameter("Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Start Angle", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Sweep Angle", "NodeSocketFloat", RIGHT_ANGLE, -MAX_ANGLE, MAX_ANGLE, "ANGLE"),
        Parameter("Segments", "NodeSocketInt", 24, 1, 1024),
    ), False),
    PrimitiveSpec("CIRCLE", "Circle", "PS_Circle", (
        Parameter("Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Segments", "NodeSocketInt", 64, 3, 2048),
    ), True),
    PrimitiveSpec("ELLIPSE", "Ellipse", "PS_Ellipse", (
        Parameter("Radius X", "NodeSocketFloat", 1.5, EPSILON, None, "DISTANCE"),
        Parameter("Radius Y", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Segments", "NodeSocketInt", 64, 3, 2048),
    ), True),
    PrimitiveSpec("RECTANGLE", "Rectangle", "PS_Rectangle", (
        Parameter("Width", "NodeSocketFloat", 2.0, EPSILON, None, "DISTANCE"),
        Parameter("Height", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
    ), True),
    PrimitiveSpec("ROUNDED_RECTANGLE", "Rounded Rectangle", "PS_RoundedRectangle", (
        Parameter("Width", "NodeSocketFloat", 2.0, EPSILON, None, "DISTANCE"),
        Parameter("Height", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Corner Radius", "NodeSocketFloat", 0.2, 0.0, None, "DISTANCE"),
        Parameter("Corner Segments", "NodeSocketInt", 8, 1, 256),
    ), True),
    PrimitiveSpec("NSIDE", "n-Side", "PS_NSide", (
        Parameter("Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Sides", "NodeSocketInt", 5, 3, 512),
        Parameter("Rotation", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
    ), True),
    PrimitiveSpec("STAR", "Star", "PS_Star", (
        Parameter("Outer Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Inner Radius", "NodeSocketFloat", 0.45, EPSILON, None, "DISTANCE"),
        Parameter("Points", "NodeSocketInt", 5, 2, 256),
        Parameter("Rotation", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
    ), True),
    PrimitiveSpec("FLOWER", "Flower", "PS_Flower", (
        Parameter("Base Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Petal Depth", "NodeSocketFloat", 0.25, 0.0, None, "DISTANCE"),
        Parameter("Petals", "NodeSocketInt", 6, 1, 256),
        Parameter("Rotation", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Resolution", "NodeSocketInt", 192, 12, 4096),
    ), True),
    PrimitiveSpec("COGWHEEL", "Cogwheel", "PS_Cogwheel", (
        Parameter("Root Radius", "NodeSocketFloat", 0.8, EPSILON, None, "DISTANCE"),
        Parameter("Outer Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Teeth", "NodeSocketInt", 16, 3, 512),
        Parameter("Tooth Ratio", "NodeSocketFloat", 0.5, 0.05, 0.95, "FACTOR"),
        Parameter("Rotation", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
    ), True),
    PrimitiveSpec("CYCLOID", "Cycloid", "PS_Cycloid", (
        Parameter("Radius", "NodeSocketFloat", 0.25, EPSILON, None, "DISTANCE"),
        Parameter("Turns", "NodeSocketFloat", 3.0, EPSILON, 100.0),
        Parameter("Resolution", "NodeSocketInt", 240, 12, 4096),
    ), False),
    PrimitiveSpec("HELIX", "Helix", "PS_Helix", (
        Parameter("Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Height", "NodeSocketFloat", 2.0, EPSILON, None, "DISTANCE"),
        Parameter("Turns", "NodeSocketFloat", 3.0, EPSILON, 100.0),
        Parameter("Resolution", "NodeSocketInt", 240, 12, 4096),
        Parameter("Clockwise", "NodeSocketBool", False),
    ), False, "3D"),
    PrimitiveSpec("SPIRAL", "Spiral", "PS_Spiral", (
        Parameter("Start Radius", "NodeSocketFloat", 0.1, 0.0, None, "DISTANCE"),
        Parameter("End Radius", "NodeSocketFloat", 1.5, EPSILON, None, "DISTANCE"),
        Parameter("Turns", "NodeSocketFloat", 3.0, EPSILON, 100.0),
        Parameter("Resolution", "NodeSocketInt", 240, 12, 4096),
        Parameter("Clockwise", "NodeSocketBool", False),
    ), False),
    PrimitiveSpec("PIE_SLICE", "Pie Slice", "PS_PieSlice", (
        Parameter("Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Start Angle", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Sweep Angle", "NodeSocketFloat", RIGHT_ANGLE, -MAX_ANGLE, MAX_ANGLE, "ANGLE"),
        Parameter("Segments", "NodeSocketInt", 24, 1, 1024),
    ), True),
    PrimitiveSpec("RING_SECTOR", "Ring Sector", "PS_RingSector", (
        Parameter("Outer Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Inner Radius", "NodeSocketFloat", 0.5, EPSILON, None, "DISTANCE"),
        Parameter("Start Angle", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Sweep Angle", "NodeSocketFloat", RIGHT_ANGLE, -MAX_ANGLE, MAX_ANGLE, "ANGLE"),
        Parameter("Inner Angle Offset", "NodeSocketFloat", 0.0, -MAX_ANGLE, MAX_ANGLE, "ANGLE"),
        Parameter("Segments", "NodeSocketInt", 24, 1, 1024),
    ), True),
)

SPECS_BY_KEY = {spec.key: spec for spec in SPECS}


def clamp(value, minimum=None, maximum=None):
    if minimum is not None and value < minimum:
        return minimum
    if maximum is not None and value > maximum:
        return maximum
    return value


def clean_points(points: list[tuple[float, float, float]], cyclic: bool) -> list[tuple[float, float, float]]:
    cleaned: list[tuple[float, float, float]] = []
    for point in points:
        if not cleaned or _distance_sq(cleaned[-1], point) > EPSILON * EPSILON:
            cleaned.append(point)
    if cyclic and len(cleaned) > 1 and _distance_sq(cleaned[0], cleaned[-1]) <= EPSILON * EPSILON:
        cleaned.pop()
    return cleaned


def _distance_sq(a, b) -> float:
    return sum((a[index] - b[index]) ** 2 for index in range(3))


def _arc(radius: float, start_angle: float, sweep_angle: float, segments: int) -> list[tuple[float, float, float]]:
    radius = max(radius, EPSILON)
    segments = max(int(segments), 1)
    start = float(start_angle)
    sweep = float(sweep_angle)
    return [
        (radius * cos(start + sweep * i / segments), radius * sin(start + sweep * i / segments), 0.0)
        for i in range(segments + 1)
    ]


def generate_points(kind: str, values: dict[str, float | int | bool]) -> tuple[list[tuple[float, float, float]], bool]:
    spec = SPECS_BY_KEY[kind]
    cyclic = spec.cyclic

    def value(name: str):
        return values.get(name, next(param.default for param in spec.parameters if param.name == name))

    if kind == "ARC":
        points = _arc(value("Radius"), value("Start Angle"), value("Sweep Angle"), value("Segments"))
    elif kind == "CIRCLE":
        points = _arc(value("Radius"), 0.0, TAU, max(int(value("Segments")), 3))[:-1]
    elif kind == "ELLIPSE":
        segments = max(int(value("Segments")), 3)
        rx = max(float(value("Radius X")), EPSILON)
        ry = max(float(value("Radius Y")), EPSILON)
        points = [(rx * cos(TAU * i / segments), ry * sin(TAU * i / segments), 0.0) for i in range(segments)]
    elif kind == "RECTANGLE":
        width = max(float(value("Width")), EPSILON)
        height = max(float(value("Height")), EPSILON)
        points = _rectangle(width, height)
    elif kind == "ROUNDED_RECTANGLE":
        points = _rounded_rectangle(
            max(float(value("Width")), EPSILON),
            max(float(value("Height")), EPSILON),
            max(float(value("Corner Radius")), 0.0),
            max(int(value("Corner Segments")), 1),
        )
    elif kind == "NSIDE":
        sides = max(int(value("Sides")), 3)
        radius = max(float(value("Radius")), EPSILON)
        rotation = float(value("Rotation"))
        points = [(radius * cos(rotation + TAU * i / sides), radius * sin(rotation + TAU * i / sides), 0.0) for i in range(sides)]
    elif kind == "STAR":
        points = _star(float(value("Outer Radius")), float(value("Inner Radius")), int(value("Points")), float(value("Rotation")))
    elif kind == "FLOWER":
        points = _flower(float(value("Base Radius")), float(value("Petal Depth")), int(value("Petals")), float(value("Rotation")), int(value("Resolution")))
    elif kind == "COGWHEEL":
        points = _cogwheel(float(value("Root Radius")), float(value("Outer Radius")), int(value("Teeth")), float(value("Tooth Ratio")), float(value("Rotation")))
    elif kind == "CYCLOID":
        points = _cycloid(float(value("Radius")), float(value("Turns")), int(value("Resolution")))
    elif kind == "HELIX":
        points = _helix(float(value("Radius")), float(value("Height")), float(value("Turns")), int(value("Resolution")), bool(value("Clockwise")))
    elif kind == "SPIRAL":
        points = _spiral(float(value("Start Radius")), float(value("End Radius")), float(value("Turns")), int(value("Resolution")), bool(value("Clockwise")))
    elif kind == "PIE_SLICE":
        points = _arc(value("Radius"), value("Start Angle"), value("Sweep Angle"), value("Segments"))
        points.append((0.0, 0.0, 0.0))
    elif kind == "RING_SECTOR":
        points = _ring_sector(
            float(value("Outer Radius")),
            float(value("Inner Radius")),
            float(value("Start Angle")),
            float(value("Sweep Angle")),
            float(value("Inner Angle Offset")),
            int(value("Segments")),
        )
    else:
        points = []

    return clean_points(points, cyclic), cyclic


def _rectangle(width: float, height: float) -> list[tuple[float, float, float]]:
    half_w = width / 2.0
    half_h = height / 2.0
    return [(-half_w, -half_h, 0.0), (half_w, -half_h, 0.0), (half_w, half_h, 0.0), (-half_w, half_h, 0.0)]


def _rounded_rectangle(width: float, height: float, corner_radius: float, corner_segments: int) -> list[tuple[float, float, float]]:
    radius = min(corner_radius, width / 2.0 - EPSILON, height / 2.0 - EPSILON)
    if radius <= EPSILON:
        return _rectangle(width, height)
    half_w = width / 2.0
    half_h = height / 2.0
    centers = (
        (half_w - radius, half_h - radius, 0.0, RIGHT_ANGLE),
        (-half_w + radius, half_h - radius, RIGHT_ANGLE, pi),
        (-half_w + radius, -half_h + radius, pi, pi + RIGHT_ANGLE),
        (half_w - radius, -half_h + radius, pi + RIGHT_ANGLE, TAU),
    )
    points: list[tuple[float, float, float]] = []
    steps = max(corner_segments, 1)
    for cx, cy, start, end in centers:
        for index in range(steps + 1):
            if points and index == 0:
                continue
            angle = start + (end - start) * index / steps
            points.append((cx + radius * cos(angle), cy + radius * sin(angle), 0.0))
    return points


def _star(outer_radius: float, inner_radius: float, points_count: int, rotation: float) -> list[tuple[float, float, float]]:
    outer = max(outer_radius, EPSILON)
    inner = clamp(inner_radius, EPSILON, outer - EPSILON)
    count = max(points_count, 2)
    rot = rotation
    return [
        ((outer if i % 2 == 0 else inner) * cos(rot + pi * i / count), (outer if i % 2 == 0 else inner) * sin(rot + pi * i / count), 0.0)
        for i in range(count * 2)
    ]


def _flower(base_radius: float, petal_depth: float, petals: int, rotation: float, resolution: int) -> list[tuple[float, float, float]]:
    base = max(base_radius, EPSILON)
    depth = max(petal_depth, 0.0)
    petal_count = max(petals, 1)
    steps = max(resolution, petal_count * 8, 12)
    rot = rotation
    return [
        ((base + depth * (0.5 + 0.5 * cos(petal_count * TAU * i / steps))) * cos(rot + TAU * i / steps),
         (base + depth * (0.5 + 0.5 * cos(petal_count * TAU * i / steps))) * sin(rot + TAU * i / steps),
         0.0)
        for i in range(steps)
    ]


def _cogwheel(root_radius: float, outer_radius: float, teeth: int, tooth_ratio: float, rotation: float) -> list[tuple[float, float, float]]:
    root = max(root_radius, EPSILON)
    outer = max(outer_radius, root + EPSILON)
    count = max(teeth, 3)
    ratio = clamp(tooth_ratio, 0.05, 0.95)
    rot = rotation
    points: list[tuple[float, float, float]] = []
    for tooth in range(count):
        base = rot + TAU * tooth / count
        tooth_angle = TAU / count
        flank = tooth_angle * (1.0 - ratio) / 2.0
        angles = (base, base + flank, base + tooth_angle - flank, base + tooth_angle)
        radii = (root, outer, outer, root)
        points.extend((r * cos(a), r * sin(a), 0.0) for r, a in zip(radii, angles))
    return points


def _ring_sector(
    outer_radius: float,
    inner_radius: float,
    start_angle: float,
    sweep_angle: float,
    inner_angle_offset: float,
    segments: int,
) -> list[tuple[float, float, float]]:
    outer = max(outer_radius, EPSILON)
    inner = clamp(inner_radius, EPSILON, outer - EPSILON)
    steps = max(segments, 1)
    direction = 1.0 if sweep_angle >= 0.0 else -1.0
    max_inward_offset = max(abs(sweep_angle) / 2.0 - EPSILON, 0.0)
    offset = clamp(inner_angle_offset, -max_inward_offset, max_inward_offset)

    outer_arc = _arc(outer, start_angle, sweep_angle, steps)
    inner_start = start_angle + direction * offset
    inner_sweep = sweep_angle - direction * offset * 2.0
    inner_arc = list(reversed(_arc(inner, inner_start, inner_sweep, steps)))
    return outer_arc + inner_arc


def _cycloid(radius: float, turns: float, resolution: int) -> list[tuple[float, float, float]]:
    r = max(radius, EPSILON)
    t = max(turns, EPSILON)
    steps = max(resolution, 12)
    return [(r * (theta - sin(theta)), r * (1.0 - cos(theta)), 0.0) for theta in (TAU * t * i / steps for i in range(steps + 1))]


def _helix(radius: float, height: float, turns: float, resolution: int, clockwise: bool) -> list[tuple[float, float, float]]:
    r = max(radius, EPSILON)
    h = max(height, EPSILON)
    t = max(turns, EPSILON)
    steps = max(resolution, 12)
    direction = -1.0 if clockwise else 1.0
    return [(r * cos(direction * TAU * t * i / steps), r * sin(direction * TAU * t * i / steps), h * i / steps) for i in range(steps + 1)]


def _spiral(start_radius: float, end_radius: float, turns: float, resolution: int, clockwise: bool) -> list[tuple[float, float, float]]:
    start = max(start_radius, 0.0)
    end = max(end_radius, EPSILON)
    t = max(turns, EPSILON)
    steps = max(resolution, 12)
    direction = -1.0 if clockwise else 1.0
    points: list[tuple[float, float, float]] = []
    for index in range(steps + 1):
        alpha = index / steps
        radius = start + (end - start) * alpha
        angle = direction * TAU * t * alpha
        points.append((radius * cos(angle), radius * sin(angle), 0.0))
    return points
