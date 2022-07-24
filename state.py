from __future__ import annotations

from typing import List, Set, Tuple
from textwrap import indent

INDENT_TAB = " " * 4

FRONT=(0, -1, 0)
BACK=(0, 1, 0)
TOP=(0, 0, 1)
BOTTOM=(0, 0, -1)
LEFT=(-1, 0, 0)
RIGHT=(1, 0, 0)

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
            result += indent(f"vertex {point}", INDENT_TAB*2)
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
        self.stl_str = f"solid {self.name}\n"
        self.stl_str += indent(faces_str(self.faces), INDENT_TAB)
        self.stl_str += "endsolid"

    def prune_duplicate_walls(self):
        print('before', len(self.walls))

        for j in range(len(self.walls)):
            for k in range(j+1, len(self.walls)):
                if self.walls[j].get_point_set() == self.walls[k].get_point_set():
                    self.walls[k].disable()
                    self.walls[j].disable()

        print('after', len([x for x in self.walls if not x.disabled]))

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
        self.rect(
            x, y, z,
            x+w_x, y, z+w_z,
            x, y, z+w_z,
            *FRONT,
            True
        )
        self.rect(
            x, y+w_y, z,
            x+w_x, y+w_y, z+w_z,
            x, y+w_y, z+w_z,
            *BACK,
            True
        )
        self.rect(
            x, y, z,
            x, y+w_y, z+w_z,
            x, y, z+w_z,
            *LEFT,
            True
        )
        self.rect(
            x+w_x, y, z,
            x+w_x, y+w_y, z+w_z,
            x+w_x, y+w_y, z,
            *RIGHT,
            True
        )
        self.rect(
            x, y, z+w_z,
            x+w_x, y+w_y, z+w_z,
            x, y+w_y, z+w_z,
            *TOP,
            True
        )
        self.rect(
            x, y+w_y, z,
            x+w_x, y, z,
            x, y, z,
            *BOTTOM,
            True
        )
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
        create_wall = False
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
            self.walls.append(Wall([f1,f2]))
        self.faces += [
            f1,
            f2
        ]

        return self
