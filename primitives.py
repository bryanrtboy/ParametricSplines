"""Curve point generation for Parametric Curves."""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, atan2, cos, pi, sin, sqrt, tan

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
        Parameter("Corner Radius", "NodeSocketFloat", 0.0, 0.0, None, "DISTANCE"),
        Parameter("Corner Segments", "NodeSocketInt", 8, 1, 256),
    ), True),
    PrimitiveSpec("NSIDE", "n-Side", "PS_NSide", (
        Parameter("Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Sides", "NodeSocketInt", 5, 3, 512),
        Parameter("Rotation", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Corner Radius", "NodeSocketFloat", 0.0, 0.0, None, "DISTANCE"),
        Parameter("Corner Segments", "NodeSocketInt", 8, 1, 256),
    ), True),
    PrimitiveSpec("STAR", "Star", "PS_Star", (
        Parameter("Outer Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Inner Radius", "NodeSocketFloat", 0.45, EPSILON, None, "DISTANCE"),
        Parameter("Points", "NodeSocketInt", 5, 2, 256),
        Parameter("Rotation", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Corner Radius", "NodeSocketFloat", 0.0, 0.0, None, "DISTANCE"),
        Parameter("Corner Segments", "NodeSocketInt", 3, 1, 64),
    ), True),
    PrimitiveSpec("FLOWER", "Flower", "PS_Flower", (
        Parameter("Base Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Petal Depth", "NodeSocketFloat", 0.25, 0.0, None, "DISTANCE"),
        Parameter("Petals", "NodeSocketInt", 6, 1, 256),
        Parameter("Rotation", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Inner Tension", "NodeSocketFloat", 1.0, 0.1, 5.0, "FACTOR"),
        Parameter("Outer Tension", "NodeSocketFloat", 1.0, 0.1, 5.0, "FACTOR"),
        Parameter("Resolution", "NodeSocketInt", 192, 12, 4096),
    ), True),
    PrimitiveSpec("COGWHEEL", "Cogwheel", "PS_Cogwheel", (
        Parameter("Root Radius", "NodeSocketFloat", 0.8, EPSILON, None, "DISTANCE"),
        Parameter("Outer Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Teeth", "NodeSocketInt", 16, 3, 512),
        Parameter("Tooth Ratio", "NodeSocketFloat", 0.5, 0.05, 0.95, "FACTOR"),
        Parameter("Corner Radius", "NodeSocketFloat", 0.0, 0.0, None, "DISTANCE"),
        Parameter("Corner Segments", "NodeSocketInt", 3, 1, 64),
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
        Parameter("Corner Radius", "NodeSocketFloat", 0.0, 0.0, None, "DISTANCE"),
        Parameter("Corner Segments", "NodeSocketInt", 3, 1, 64),
        Parameter("Segments", "NodeSocketInt", 24, 1, 1024),
    ), True),
    PrimitiveSpec("RING_SECTOR", "Ring Sector", "PS_RingSector", (
        Parameter("Outer Radius", "NodeSocketFloat", 1.0, EPSILON, None, "DISTANCE"),
        Parameter("Inner Radius", "NodeSocketFloat", 0.5, EPSILON, None, "DISTANCE"),
        Parameter("Start Angle", "NodeSocketFloat", 0.0, None, None, "ANGLE"),
        Parameter("Sweep Angle", "NodeSocketFloat", RIGHT_ANGLE, -MAX_ANGLE, MAX_ANGLE, "ANGLE"),
        Parameter("Inner Angle Offset", "NodeSocketFloat", 0.0, -MAX_ANGLE, MAX_ANGLE, "ANGLE"),
        Parameter("Corner Radius", "NodeSocketFloat", 0.0, 0.0, None, "DISTANCE"),
        Parameter("Corner Segments", "NodeSocketInt", 3, 1, 64),
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


def _distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return sqrt(_distance_sq(a, b))


def _distance_sq(a, b) -> float:
    return sum((a[index] - b[index]) ** 2 for index in range(3))


def _length(vector: tuple[float, float]) -> float:
    return sqrt(vector[0] * vector[0] + vector[1] * vector[1])


def _normalize(vector: tuple[float, float]) -> tuple[float, float]:
    length = _length(vector)
    if length <= EPSILON:
        return (0.0, 0.0)
    return (vector[0] / length, vector[1] / length)


def _dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _shortest_ccw_sweep(start_angle: float, end_angle: float) -> float:
    sweep = (end_angle - start_angle) % TAU
    if sweep > pi:
        sweep -= TAU
    return sweep


def _lerp_point(a: tuple[float, float, float], b: tuple[float, float, float], factor: float) -> tuple[float, float, float]:
    return (
        a[0] + (b[0] - a[0]) * factor,
        a[1] + (b[1] - a[1]) * factor,
        a[2] + (b[2] - a[2]) * factor,
    )


def _resample_closed_polyline(points: list[tuple[float, float, float]], count: int) -> list[tuple[float, float, float]]:
    if len(points) < 2 or count <= 0:
        return points

    lengths = []
    total_length = 0.0
    for index, point in enumerate(points):
        next_point = points[(index + 1) % len(points)]
        length = _distance(point, next_point)
        lengths.append(length)
        total_length += length

    if total_length <= EPSILON:
        return points[:count]

    resampled: list[tuple[float, float, float]] = []
    segment_index = 0
    segment_start_distance = 0.0
    for target_index in range(count):
        target_distance = total_length * target_index / count
        while segment_start_distance + lengths[segment_index] < target_distance and segment_index < len(points) - 1:
            segment_start_distance += lengths[segment_index]
            segment_index += 1
        segment_length = max(lengths[segment_index], EPSILON)
        factor = (target_distance - segment_start_distance) / segment_length
        resampled.append(_lerp_point(points[segment_index], points[(segment_index + 1) % len(points)], factor))
    return resampled


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
        points = _rounded_rectangle(width, height, max(float(value("Corner Radius")), 0.0), max(int(value("Corner Segments")), 1))
    elif kind == "NSIDE":
        sides = max(int(value("Sides")), 3)
        radius = max(float(value("Radius")), EPSILON)
        rotation = float(value("Rotation"))
        points = _nside(radius, sides, rotation)
        points = _rounded_polygon(points, max(float(value("Corner Radius")), 0.0), max(int(value("Corner Segments")), 1))
    elif kind == "STAR":
        points = _star(float(value("Outer Radius")), float(value("Inner Radius")), int(value("Points")), float(value("Rotation")))
        points = _rounded_polygon(points, max(float(value("Corner Radius")), 0.0), max(int(value("Corner Segments")), 1))
    elif kind == "FLOWER":
        points = _flower(
            float(value("Base Radius")),
            float(value("Petal Depth")),
            int(value("Petals")),
            float(value("Rotation")),
            float(value("Inner Tension")),
            float(value("Outer Tension")),
            int(value("Resolution")),
        )
    elif kind == "COGWHEEL":
        points = _cogwheel(
            float(value("Root Radius")),
            float(value("Outer Radius")),
            int(value("Teeth")),
            float(value("Tooth Ratio")),
            max(float(value("Corner Radius")), 0.0),
            max(int(value("Corner Segments")), 1),
            float(value("Rotation")),
        )
    elif kind == "CYCLOID":
        points = _cycloid(float(value("Radius")), float(value("Turns")), int(value("Resolution")))
    elif kind == "HELIX":
        points = _helix(float(value("Radius")), float(value("Height")), float(value("Turns")), int(value("Resolution")), bool(value("Clockwise")))
    elif kind == "SPIRAL":
        points = _spiral(float(value("Start Radius")), float(value("End Radius")), float(value("Turns")), int(value("Resolution")), bool(value("Clockwise")))
    elif kind == "PIE_SLICE":
        points = _pie_slice(
            float(value("Radius")),
            float(value("Start Angle")),
            float(value("Sweep Angle")),
            int(value("Segments")),
            max(float(value("Corner Radius")), 0.0),
            max(int(value("Corner Segments")), 1),
        )
    elif kind == "RING_SECTOR":
        points = _ring_sector(
            float(value("Outer Radius")),
            float(value("Inner Radius")),
            float(value("Start Angle")),
            float(value("Sweep Angle")),
            float(value("Inner Angle Offset")),
            int(value("Segments")),
            max(float(value("Corner Radius")), 0.0),
            max(int(value("Corner Segments")), 1),
        )
    else:
        points = []

    return clean_points(points, cyclic), cyclic


def _rectangle(width: float, height: float) -> list[tuple[float, float, float]]:
    half_w = width / 2.0
    half_h = height / 2.0
    return [(-half_w, -half_h, 0.0), (half_w, -half_h, 0.0), (half_w, half_h, 0.0), (-half_w, half_h, 0.0)]


def _nside(radius: float, sides: int, rotation: float) -> list[tuple[float, float, float]]:
    return [(radius * cos(rotation + TAU * i / sides), radius * sin(rotation + TAU * i / sides), 0.0) for i in range(sides)]


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


def _rounded_polygon(
    vertices: list[tuple[float, float, float]],
    corner_radius: float,
    corner_segments: int,
) -> list[tuple[float, float, float]]:
    radius = max(corner_radius, 0.0)
    if radius <= EPSILON or len(vertices) < 3:
        return vertices

    points: list[tuple[float, float, float]] = []
    count = len(vertices)
    steps = max(corner_segments, 1)
    for index, vertex in enumerate(vertices):
        previous_vertex = vertices[(index - 1) % count]
        next_vertex = vertices[(index + 1) % count]
        to_previous = _normalize((previous_vertex[0] - vertex[0], previous_vertex[1] - vertex[1]))
        to_next = _normalize((next_vertex[0] - vertex[0], next_vertex[1] - vertex[1]))
        previous_length = _length((previous_vertex[0] - vertex[0], previous_vertex[1] - vertex[1]))
        next_length = _length((next_vertex[0] - vertex[0], next_vertex[1] - vertex[1]))
        interior_angle = acos(clamp(_dot(to_previous, to_next), -1.0, 1.0))
        if interior_angle <= EPSILON:
            points.append(vertex)
            continue

        max_distance = max(min(previous_length, next_length) / 2.0 - EPSILON, 0.0)
        tangent_distance = min(radius / max(tan(interior_angle / 2.0), EPSILON), max_distance)
        if tangent_distance <= EPSILON:
            points.append(vertex)
            continue

        actual_radius = tangent_distance * tan(interior_angle / 2.0)
        bisector = _normalize((to_previous[0] + to_next[0], to_previous[1] + to_next[1]))
        center_distance = actual_radius / max(sin(interior_angle / 2.0), EPSILON)
        center = (vertex[0] + bisector[0] * center_distance, vertex[1] + bisector[1] * center_distance)
        start = (vertex[0] + to_previous[0] * tangent_distance, vertex[1] + to_previous[1] * tangent_distance)
        end = (vertex[0] + to_next[0] * tangent_distance, vertex[1] + to_next[1] * tangent_distance)
        start_angle = atan2(start[1] - center[1], start[0] - center[0])
        end_angle = atan2(end[1] - center[1], end[0] - center[0])
        sweep = _shortest_ccw_sweep(start_angle, end_angle)

        for segment in range(steps + 1):
            if points and segment == 0:
                continue
            angle = start_angle + sweep * segment / steps
            points.append((center[0] + actual_radius * cos(angle), center[1] + actual_radius * sin(angle), 0.0))
    return points


def _rounded_selected_corners(
    vertices: list[tuple[float, float, float]],
    corner_indices: list[int],
    corner_radius: float,
    corner_segments: int,
) -> list[tuple[float, float, float]]:
    radius = max(corner_radius, 0.0)
    if radius <= EPSILON or len(vertices) < 3 or not corner_indices:
        return vertices

    count = len(vertices)
    corners = sorted({index % count for index in corner_indices})
    if len(corners) < 2:
        return vertices

    corner_data = {}
    steps = max(corner_segments, 1)
    for position, index in enumerate(corners):
        previous_corner = corners[position - 1]
        next_corner = corners[(position + 1) % len(corners)]
        previous_available = _path_distance(vertices, index, previous_corner, -1)
        next_available = _path_distance(vertices, index, next_corner, 1)
        if previous_available <= EPSILON or next_available <= EPSILON:
            continue

        vertex = vertices[index]
        previous_reference = _walk_point(vertices, index, min(previous_available, radius), -1)
        next_reference = _walk_point(vertices, index, min(next_available, radius), 1)
        to_previous = _normalize((previous_reference[0] - vertex[0], previous_reference[1] - vertex[1]))
        to_next = _normalize((next_reference[0] - vertex[0], next_reference[1] - vertex[1]))
        interior_angle = acos(clamp(_dot(to_previous, to_next), -1.0, 1.0))
        if interior_angle <= EPSILON:
            continue

        max_distance = max(min(previous_available, next_available) / 2.0 - EPSILON, 0.0)
        tangent_distance = min(radius / max(tan(interior_angle / 2.0), EPSILON), max_distance)
        if tangent_distance <= EPSILON:
            continue

        actual_radius = tangent_distance * tan(interior_angle / 2.0)
        before = _walk_point(vertices, index, tangent_distance, -1)
        after = _walk_point(vertices, index, tangent_distance, 1)
        bisector = _normalize((to_previous[0] + to_next[0], to_previous[1] + to_next[1]))
        center_distance = actual_radius / max(sin(interior_angle / 2.0), EPSILON)
        center = (vertex[0] + bisector[0] * center_distance, vertex[1] + bisector[1] * center_distance)
        start_angle = atan2(before[1] - center[1], before[0] - center[0])
        end_angle = atan2(after[1] - center[1], after[0] - center[0])
        sweep = _shortest_ccw_sweep(start_angle, end_angle)
        arc = [
            (center[0] + actual_radius * cos(start_angle + sweep * segment / steps), center[1] + actual_radius * sin(start_angle + sweep * segment / steps), 0.0)
            for segment in range(steps + 1)
        ]
        corner_data[index] = {
            "arc": arc,
            "after_distance": tangent_distance,
            "before_distance": tangent_distance,
        }

    if not corner_data:
        return vertices

    rounded: list[tuple[float, float, float]] = []
    active_corners = [index for index in corners if index in corner_data]
    for position, index in enumerate(active_corners):
        arc = corner_data[index]["arc"]
        if rounded:
            rounded.extend(arc[1:])
        else:
            rounded.extend(arc)

        next_index = active_corners[(position + 1) % len(active_corners)]
        segment_points = _trimmed_segment_points(
            vertices,
            index,
            next_index,
            corner_data[index]["after_distance"],
            corner_data[next_index]["before_distance"],
        )
        rounded.extend(segment_points)

    return rounded


def _path_distance(vertices: list[tuple[float, float, float]], start_index: int, end_index: int, direction: int) -> float:
    if start_index == end_index:
        return 0.0

    count = len(vertices)
    distance = 0.0
    index = start_index
    while True:
        next_index = (index + direction) % count
        distance += _distance(vertices[index], vertices[next_index])
        index = next_index
        if index == end_index:
            return distance


def _walk_point(
    vertices: list[tuple[float, float, float]],
    start_index: int,
    distance: float,
    direction: int,
) -> tuple[float, float, float]:
    count = len(vertices)
    remaining = max(distance, 0.0)
    index = start_index
    while remaining > EPSILON:
        next_index = (index + direction) % count
        segment_length = _distance(vertices[index], vertices[next_index])
        if segment_length >= remaining:
            factor = remaining / max(segment_length, EPSILON)
            return _lerp_point(vertices[index], vertices[next_index], factor)
        remaining -= segment_length
        index = next_index
    return vertices[index]


def _trimmed_segment_points(
    vertices: list[tuple[float, float, float]],
    start_index: int,
    end_index: int,
    start_trim: float,
    end_trim: float,
) -> list[tuple[float, float, float]]:
    total_length = _path_distance(vertices, start_index, end_index, 1)
    if total_length <= start_trim + end_trim + EPSILON:
        return []

    points: list[tuple[float, float, float]] = []
    distance_from_start = 0.0
    index = start_index
    while True:
        next_index = (index + 1) % len(vertices)
        distance_from_start += _distance(vertices[index], vertices[next_index])
        if next_index == end_index:
            break
        if start_trim + EPSILON < distance_from_start < total_length - end_trim - EPSILON:
            points.append(vertices[next_index])
        index = next_index
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


def _flower(
    base_radius: float,
    petal_depth: float,
    petals: int,
    rotation: float,
    inner_tension: float,
    outer_tension: float,
    resolution: int,
) -> list[tuple[float, float, float]]:
    base = max(base_radius, EPSILON)
    depth = max(petal_depth, 0.0)
    petal_count = max(petals, 1)
    steps = max(resolution, petal_count * 8, 12)
    sample_steps = max(steps * 4, petal_count * 64)
    rot = rotation
    inner = clamp(inner_tension, 0.1, 5.0)
    outer = clamp(outer_tension, 0.1, 5.0)
    points: list[tuple[float, float, float]] = []
    for index in range(sample_steps):
        angle = TAU * index / sample_steps
        weight = 0.5 + 0.5 * cos(petal_count * angle)
        if weight < 0.5:
            weight = 0.5 - 0.5 * ((1.0 - weight * 2.0) ** inner)
        else:
            weight = 0.5 + 0.5 * (((weight - 0.5) * 2.0) ** outer)
        radius = base + depth * weight
        points.append((radius * cos(rot + angle), radius * sin(rot + angle), 0.0))
    return _resample_closed_polyline(points, steps)


def _cogwheel(
    root_radius: float,
    outer_radius: float,
    teeth: int,
    tooth_ratio: float,
    corner_radius: float,
    corner_segments: int,
    rotation: float,
) -> list[tuple[float, float, float]]:
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
    return _rounded_polygon(points, corner_radius, corner_segments)


def _pie_slice(
    radius: float,
    start_angle: float,
    sweep_angle: float,
    segments: int,
    corner_radius: float,
    corner_segments: int,
) -> list[tuple[float, float, float]]:
    steps = max(segments, 1)
    points = _arc(radius, start_angle, sweep_angle, steps)
    points.append((0.0, 0.0, 0.0))
    return _rounded_selected_corners(points, [0, steps, steps + 1], corner_radius, corner_segments)


def _ring_sector(
    outer_radius: float,
    inner_radius: float,
    start_angle: float,
    sweep_angle: float,
    inner_angle_offset: float,
    segments: int,
    corner_radius: float,
    corner_segments: int,
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
    points = outer_arc + inner_arc
    return _rounded_selected_corners(points, [0, steps, steps + 1, steps * 2 + 1], corner_radius, corner_segments)


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
