from __future__ import annotations

from typing import List
from textwrap import indent

INDENT_TAB = " " * 4

FRONT=(0, -1, 0)
BACK=(0, 1, 0)
TOP=(0, 0, 1)
BOTTOM=(0, 0, -1)
LEFT=(-1, 0, 0)
RIGHT=(1, 0, 0)

class Point:
    x: int
    y: int
    z: int
    index: int = 1

    used: int = 0

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        Point.used += 1
        self.index = Point.used

    def __repr__(self):
        return f"#{self.index} ({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return point_str(self)


class Face:
    points: List[Point]
    normal: Point

    def __init__(self, points: List[Point], normal: Point):
        self.points = points
        self.normal = normal

    def __repr__(self):
        return f"({self.normal}) {self.points}"


def point_str(point: Point) -> str:
    return f"{point.x:.5f} {point.y:.5f} {point.z:.5f}\n"


def faces_str(faces: List[Face]) -> str:
    result = ""
    for face in faces:
        result += f"facet normal {face.normal}"
        for point in face.points:
            result += indent(f"vertex {point}", INDENT_TAB)
        result += "endfacet\n"
    return result


class State:
    faces: List[Face]
    stl_str: str
    name: str

    def __init__(self, name="test"):
        self.faces = []
        self.stl_str = ""
        self.name = name

    def update_str_state(self):
        self.stl_str = f"solid {self.name}\n"
        self.stl_str += indent(faces_str(self.faces), INDENT_TAB)
        self.stl_str += "endsolid"

    def box(self, x: int, y: int, z: int, side: int) -> State:
        return self.cuboid(x, y, z, side, side, side)

    def cuboid(
        self,
        x: int,
        y: int,
        z: int,
        w_x: int,
        w_y: int,
        w_z: int,
        g_x: int | None = None,
        g_y: int | None = None,
        g_z: int | None = None,
    ) -> State:
        if all(map(lambda x: x is not None, [g_x, g_y, g_z])):
            raise Exception(
                "Gap on one axis needs to be None (so that gap leads outside)"
            )
        self.rect(
            x, y, z,
            x+w_x, y, z+w_z,
            x, y, z+w_z,
            *FRONT
        )
        self.rect(
            x, y+w_y, z,
            x+w_x, y+w_y, z+w_z,
            x, y+w_y, z+w_z,
            *BACK
        )
        self.rect(
            x, y, z,
            x, y+w_y, z+w_z,
            x, y, z+w_z,
            *LEFT
        )
        self.rect(
            x+w_x, y, z,
            x+w_x, y+w_y, z+w_z,
            x+w_x, y+w_y, z,
            *RIGHT
        )
        self.rect(
            x, y, z+w_z,
            x+w_x, y+w_y, z+w_z,
            x, y+w_y, z+w_z,
            *TOP
        )
        self.rect(
            x, y+w_y, z,
            x+w_x, y, z,
            x, y, z,
            *BOTTOM
        )
        return self

    def rect(
        self,
        x: int,
        y: int,
        z: int,
        x2: int,
        y2: int,
        z2: int,
        x3: int,
        y3: int,
        z3: int,
        nx: int,
        ny: int,
        nz: int,
    ) -> State:
        """
        Creates rectangular face between given 3 corners, calculating 4th one
        First 2 points must cross diagonally
        """
        mid_point = [(x + x2) // 2, (y + y2) // 2, (z + z2) // 2]
        p1 = Point(x, y, z)
        p2 = Point(x2, y2, z2)
        p3 = Point(x3, y3, z3)
        p4 = Point(
            mid_point[0] - (x3 - mid_point[0]),
            mid_point[1] - (y3 - mid_point[1]),
            mid_point[2] - (z3 - mid_point[2]),
        )

        self.faces += [
            Face([p1, p4, p2], normal=Point(nx, ny, nz)),
            Face([p1, p2, p3], normal=Point(nx, ny, nz)),
        ]

        return self
