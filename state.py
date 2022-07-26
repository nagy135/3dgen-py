from __future__ import annotations

from typing import List, Set, Tuple
from textwrap import indent
import numpy as np

INDENT_TAB = " " * 4

FRONT = (0, -1, 0)
BACK = (0, 1, 0)
TOP = (0, 0, 1)
BOTTOM = (0, 0, -1)
LEFT = (-1, 0, 0)
RIGHT = (1, 0, 0)


class Point:
    x: float
    y: float
    z: float
    index: int = 1

    used: int = 0

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        Point.used += 1
        self.index = Point.used

    def __repr__(self):
        return f"#{self.index} ({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return point_str(self)


class Wall:
    faces: List[Face]
    disabled: bool

    def __init__(self, faces):
        self.faces = faces
        self.disabled = False

    def __repr__(self):
        return f"#{self.faces}"

    def disable(self):
        self.disabled = True
        for face in self.faces:
            face.disabled = True

    def get_point_set(self) -> Set[Tuple[float]]:
        s = set()
        for face in self.faces:
            for point in face.points:
                s.add((point.x, point.y, point.z))
        return s


class Face:
    points: List[Point]
    normal: Point
    disabled: bool

    def __init__(self, points: List[Point], normal: Point):
        self.points = points
        self.normal = normal
        self.disabled = False

    def get_point_set(self) -> Set[Tuple[float]]:
        s = set()
        for point in self.points:
            s.add((point.x, point.y, point.z))
        return s

    def __repr__(self):
        return f"{self.points} ({self.normal})"


def point_str(point: Point) -> str:
    return f"{point.x:.1f} {point.y:.1f} {point.z:.1f}\n"


def faces_str(faces: List[Face]) -> str:
    result = ""
    for face in faces:
        if face.disabled:
            continue
        result += f"facet normal {face.normal}"
        result += indent("outer loop\n", INDENT_TAB)
        for point in face.points:
            result += indent(f"vertex {point}", INDENT_TAB * 2)
        result += indent("endloop\n", INDENT_TAB)
        result += "endfacet\n"
    return result


class State:
    faces: List[Face]
    walls: List[Wall]
    stl_str: str
    name: str

    def __init__(self, name="test"):
        self.faces = []
        self.walls = []
        self.stl_str = ""
        self.name = name

    def update_str_state(self):
        self.prune_duplicate_walls()
        self.prune_duplicate_faces()
        self.stl_str = f"solid {self.name}\n"
        self.stl_str += indent(faces_str(self.faces), INDENT_TAB)
        self.stl_str += "endsolid"

    def prune_duplicate_walls(self):
        for j in range(len(self.walls)):
            for k in range(j + 1, len(self.walls)):
                if self.walls[j].get_point_set() == self.walls[k].get_point_set():
                    self.walls[k].disable()
                    self.walls[j].disable()

    def prune_duplicate_faces(self):
        for j in range(len(self.faces)):
            for k in range(j + 1, len(self.faces)):
                face1 = self.faces[j]
                face2 = self.faces[k]
                if face1.get_point_set() == face2.get_point_set():
                    if face1.normal != face2.normal:
                        face1.disabled = True
                        face2.disabled = True
                    else:
                        face2.disabled = True

    def box(self, x: float, y: float, z: float, side: float) -> State:
        return self.cuboid(x, y, z, side, side, side)

    def cuboid(
        self,
        x: float,
        y: float,
        z: float,
        w_x: float,
        w_y: float,
        w_z: float,
        g_x: float | None = None,
        g_y: float | None = None,
        g_z: float | None = None,
    ) -> State:
        if all(map(lambda x: x is not None, [g_x, g_y, g_z])):
            raise Exception(
                "Gap on one axis needs to be None (so that gap leads outside)"
            )
        if not (g_x is not None and g_z is not None):
            self.rect(x, y, z, x + w_x, y, z + w_z, x, y, z + w_z, *FRONT, True)
            self.rect(
                x,
                y + w_y,
                z,
                x + w_x,
                y + w_y,
                z + w_z,
                x + w_x,
                y + w_y,
                z,
                *BACK,
                True,
            )
        if not (g_y is not None and g_z is not None):
            self.rect(x, y, z, x, y + w_y, z + w_z, x, y + w_y, z, *LEFT, True)
            self.rect(
                x + w_x,
                y,
                z,
                x + w_x,
                y + w_y,
                z + w_z,
                x + w_x,
                y,
                z + w_z,
                *RIGHT,
                True,
            )
        if not (g_y is not None and g_x is not None):
            self.rect(
                x,
                y,
                z + w_z,
                x + w_x,
                y + w_y,
                z + w_z,
                x,
                y + w_y,
                z + w_z,
                *TOP,
                True,
            )
            self.rect(x, y + w_y, z, x + w_x, y, z, x, y, z, *BOTTOM, True)

        if all(map(lambda x: x is None, [g_x, g_y, g_z])):
            return self

        p1 = x, y, z
        p2 = x + w_x, y, z
        p3 = x, y + w_y, z
        p4 = x + w_x, y + w_y, z
        p5 = x, y, z + w_z
        p6 = x + w_x, y, z + w_z
        p7 = x, y + w_y, z + w_z
        p8 = x + w_x, y + w_y, z + w_z

        if g_z is None and g_x is not None and g_y is not None:
            p9 = x + g_x, y + g_y, z
            p10 = x + w_x - g_x, y + g_y, z
            p11 = x + g_x, y + w_y - g_y, z
            p12 = x + w_x - g_x, y + w_y - g_y, z
            p13 = x + g_x, y + g_y, z + w_z
            p14 = x + w_x - g_x, y + g_y, z + w_z
            p15 = x + g_x, y + w_y - g_y, z + w_z
            p16 = x + w_x - g_x, y + w_y - g_y, z + w_z

            # BOTTOM
            self.triangle(*p11, *p3, *p12, *BOTTOM)
            self.triangle(*p3, *p4, *p12, *BOTTOM)
            self.triangle(*p4, *p10, *p12, *BOTTOM)
            self.triangle(*p4, *p2, *p10, *BOTTOM)
            self.triangle(*p2, *p9, *p10, *BOTTOM)
            self.triangle(*p2, *p1, *p9, *BOTTOM)
            self.triangle(*p1, *p11, *p9, *BOTTOM)
            self.triangle(*p1, *p3, *p11, *BOTTOM)

            # TOP
            self.triangle(*p5, *p14, *p13, *TOP)
            self.triangle(*p5, *p6, *p14, *TOP)
            self.triangle(*p6, *p16, *p14, *TOP)
            self.triangle(*p6, *p8, *p16, *TOP)
            self.triangle(*p8, *p15, *p16, *TOP)
            self.triangle(*p8, *p7, *p15, *TOP)
            self.triangle(*p7, *p13, *p15, *TOP)
            self.triangle(*p7, *p5, *p13, *TOP)

            # INNER
            self.rect(*p9, *p15, *p13, *RIGHT)
            self.rect(*p12, *p14, *p16, *LEFT)
            self.rect(*p11, *p16, *p15, *FRONT)
            self.rect(*p10, *p13, *p14, *BACK)

        if g_x is None and g_y is not None and g_z is not None:
            p9 = x, y + g_y, z + g_z
            p10 = x, y + g_y, z + w_z - g_z
            p11 = x, y + w_y - g_y, z + g_z
            p12 = x, y + w_y - g_y, z + w_z - g_z
            p13 = x + w_x, y + g_y, z + g_z
            p14 = x + w_x, y + g_y, z + w_z - g_z
            p15 = x + w_x, y + w_y - g_y, z + g_z
            p16 = x + w_x, y + w_y - g_y, z + w_z - g_z

            # LEFT
            self.triangle(*p3, *p9, *p11, *LEFT)
            self.triangle(*p3, *p1, *p9, *LEFT)
            self.triangle(*p1, *p10, *p9, *LEFT)
            self.triangle(*p1, *p5, *p10, *LEFT)
            self.triangle(*p5, *p12, *p10, *LEFT)
            self.triangle(*p5, *p7, *p12, *LEFT)
            self.triangle(*p7, *p11, *p12, *LEFT)
            self.triangle(*p7, *p3, *p11, *LEFT)

            # RIGHT
            self.triangle(*p2, *p15, *p13, *RIGHT)
            self.triangle(*p2, *p4, *p15, *RIGHT)
            self.triangle(*p4, *p16, *p15, *RIGHT)
            self.triangle(*p4, *p8, *p16, *RIGHT)
            self.triangle(*p8, *p14, *p16, *RIGHT)
            self.triangle(*p8, *p6, *p14, *RIGHT)
            self.triangle(*p6, *p13, *p14, *RIGHT)
            self.triangle(*p6, *p2, *p13, *RIGHT)

            # INNER
            self.rect(*p9, *p14, *p10, *BACK)
            self.rect(*p11, *p16, *p12, *FRONT)
            self.rect(*p9, *p15, *p11, *TOP)
            self.rect(*p12, *p14, *p16, *BOTTOM)

        return self

    def triangle(
        self,
        x: float,
        y: float,
        z: float,
        x2: float,
        y2: float,
        z2: float,
        x3: float,
        y3: float,
        z3: float,
        nx: float,
        ny: float,
        nz: float,
    ) -> State:
        p1 = Point(x, y, z)
        p2 = Point(x2, y2, z2)
        p3 = Point(x3, y3, z3)
        face = Face([p1, p2, p3], normal=Point(nx, ny, nz))

        self.faces.append(face)
        return self

    def prism(
        self,
        x1: float,
        y1: float,
        z1: float,
        x2: float,
        y2: float,
        z2: float,
        x3: float,
        y3: float,
        z3: float,
        x4: float,
        y4: float,
        z4: float,
    ) -> State:
        """
        Creates prism using first 3 points as base and 4th as its peak (up or down)
        """

        UPSIDE_DOWN = True if (z3 < z1) else False

        BASE_NORMAL = BOTTOM if not UPSIDE_DOWN else TOP

        self.triangle(x1, y1, z1, x2, y2, z2, x3, y3, z3, *BASE_NORMAL)

        p1 = (x1, y1, z1)
        p2 = (x2, y2, z2)
        p3 = (x3, y3, z3)
        p4 = (x4, y4, z4)
        for first, second, third in [
            (p1, p2, p4),
            (p2, p3, p4),
            (p3, p1, p4),
        ]:
            vectA = (second[0] - first[0], second[1] - first[1], second[2] - first[2])
            vectB = (third[0] - first[0], third[1] - first[1], third[2] - first[2])
            self.triangle(*first, *second, *third, *np.cross(vectA, vectB))

        return self

    def rect(
        self,
        x: float,
        y: float,
        z: float,
        x2: float,
        y2: float,
        z2: float,
        x3: float,
        y3: float,
        z3: float,
        nx: float,
        ny: float,
        nz: float,
        create_wall=False,
    ) -> State:
        """
        Creates rectangular face between given 3 corners, calculating 4th one
        First 2 points must cross diagonally
        """
        mid_point = [(x + x2) / 2, (y + y2) / 2, (z + z2) / 2]
        p1 = Point(x, y, z)
        p2 = Point(x2, y2, z2)
        p3 = Point(x3, y3, z3)
        p4 = Point(
            mid_point[0] - (x3 - mid_point[0]),
            mid_point[1] - (y3 - mid_point[1]),
            mid_point[2] - (z3 - mid_point[2]),
        )

        f1 = Face([p1, p4, p2], normal=Point(nx, ny, nz))
        f2 = Face([p1, p2, p3], normal=Point(nx, ny, nz))

        if create_wall:
            self.walls.append(Wall([f1, f2]))
        self.faces += [f1, f2]

        return self
