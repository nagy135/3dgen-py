#!/usr/bin/env python

from __future__ import annotations

from typing import List, Set
import argparse
from pyrender import start


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


class Face:
    point_indexes: List[int]

    def __init__(self, point_indexes: List[int]):
        self.point_indexes = point_indexes

    def __repr__(self):
        return f"{self.point_indexes}"


def points_str(points: List[Point]) -> str:
    result = ""
    for point in points:
        result += f"v {point.x:.5f} {point.y:.5f} {point.z:.5f}\n"
    return result


def faces_str(faces: List[Face]) -> str:
    result = ""
    for face in faces:
        result += "f " + " ".join([str(i) for i in face.point_indexes]) + "\n"
    return result


class State:
    points: List[Point]
    faces: List[Face]
    obj_str: str

    def __init__(self):
        self.points = []
        self.faces = []
        self.obj_str = "mtllib master.mtl\n\n"

    def write_obj_str(self):
        self.obj_str += points_str(self.points)
        self.obj_str += faces_str(self.faces)

    def remove_duplicate_faces(self):
        duplicate_face_indexes: Set[int] = set()
        for j in range(len(self.faces)):
            for k in range(j + 1, len(self.faces)):
                face = self.faces[j]
                face2 = self.faces[k]

                points = list(
                    filter(lambda x: x.index in face.point_indexes, self.points)
                )
                points2 = list(
                    filter(lambda x: x.index in face2.point_indexes, self.points)
                )

                first = [
                    point.x + point.y * 1000 + point.z * 1000000 for point in points
                ]
                second = [
                    point.x + point.y * 1000 + point.z * 1000000 for point in points2
                ]

                if set(first) == set(second):
                    duplicate_face_indexes.add(k)
                    duplicate_face_indexes.add(j)

        new_faces = []
        for index in range(len(self.faces)):
            if index not in duplicate_face_indexes:
                new_faces.append(self.faces[index])
        self.faces = new_faces

    def box(self, x: int, y: int, z: int, side: int) -> State:
        return self.cuboid(x, y, z, side, side, side)

    def cuboid(self, x: int, y: int, z: int, w_x: int, w_y: int, w_z: int) -> State:
        coordinates = [
            [x, y, z],
            [x + w_x, y, z],
            [x, y + w_y, z],
            [x + w_x, y + w_y, z],
            [x, y, z + w_z],
            [x + w_x, y, z + w_z],
            [x, y + w_y, z + w_z],
            [x + w_x, y + w_y, z + w_z],
        ]

        points = [Point(x=j[0], y=j[1], z=j[2]) for j in coordinates]
        offset = len(self.points)
        faces = [
            Face([offset + 1, offset + 2, offset + 4, offset + 3]),
            Face([offset + 5, offset + 6, offset + 8, offset + 7]),
            Face([offset + 1, offset + 3, offset + 7, offset + 5]),
            Face([offset + 2, offset + 4, offset + 8, offset + 6]),
            Face([offset + 1, offset + 2, offset + 6, offset + 5]),
            Face([offset + 3, offset + 4, offset + 8, offset + 7]),
        ]
        self.points += points
        self.faces += faces

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
    ) -> State:
        '''
        Creates rectangular face between given 3 corners, calculating 4th one
        First 2 points must cross diagonally
        '''
        mid_point = [(x + x2) / 2, (y + y2) / 2, (z + z2) / 2]
        coordinates = [
            [x, y, z],
            [
                mid_point[0] - (x3 - mid_point[0]),
                mid_point[1] - (y3 - mid_point[1]),
                mid_point[2] - (z3 - mid_point[2]),
            ],
            [x2, y2, z2],
            [x3, y3, z3],
        ]

        points = [Point(x=j[0], y=j[1], z=j[2]) for j in coordinates]
        offset = len(self.points)

        faces = [
            Face([offset + 1, offset + 2, offset + 3, offset + 4]),
        ]
        self.points += points
        self.faces += faces

        return self


def main():
    parser = argparse.ArgumentParser(description="Generates obj files from code")

    parser.add_argument(
        "filename", metavar="filename", type=str, help="file to output .obj to"
    )

    parser.add_argument(
        "--preview",
        "-p",
        dest="preview_mode",
        action="store_const",
        const=True,
        default=False,
        help="preview after generate",
    )
    args = parser.parse_args()

    if args.preview_mode:
        print("OPEN PREVIEW")

    state = State()

    generate_logic(state)

    state.remove_duplicate_faces()
    state.write_obj_str()

    with open(args.filename, "w") as f:
        f.write(state.obj_str)

    if args.preview_mode:
        start(args.filename)


def generate_logic(state: State):
    example_predefined_points(state)
    pass

def example_predefined_points(state: State):
    u = 28

    p1 = [0,0,0]
    p2 = [u,0,0]
    p3 = [2*u,0,0]
    p4 = [3*u,0,0]
    p5 = [0,u,0]
    p6 = [u,u,0]
    p7 = [2*u,u,0]
    p8 = [3*u,u,0]

    p9 = [u, 0, u]
    p10 = [2*u, 0, u]
    p11 = [2*u, u, u]
    p12 = [u, u, u]

    p13 = [0,0,2*u]
    p14 = [u,0,2*u]
    p15 = [2*u,0,2*u]
    p16 = [3*u,0,2*u]
    p17 = [0,u,2*u]
    p18 = [u,u,2*u]
    p19 = [2*u,u,2*u]
    p20 = [3*u,u,2*u]

    # p21 = [u+u/3, u/3, u]
    # p22 = [2*u-u/3, u/3, u]
    # p23 = [2*u-u/3, 2*u/3, u]
    # p24 = [u+u/3, 2*u/3, u]
    #
    # p25 = [u+u/3, u/3, 2*u]
    # p26 = [2*u-u/3, u/3, 2*u]
    # p27 = [2*u-u/3, 2*u/3, 2*u]
    # p28 = [u+u/3, 2*u/3, 2*u]

    state.rect(*p14, *p17, *p18)
    state.rect(*p1, *p17, *p5)
    state.rect(*p4, *p20, *p8)
    state.rect(*p15, *p20, *p19)
    state.rect(*p9, *p18, *p14)
    state.rect(*p10, *p19, *p11)
    state.rect(*p9, *p11, *p12)
    state.rect(*p1, *p14, *p13)
    state.rect(*p3, *p16, *p4)
    state.rect(*p2, *p10, *p9)
    state.rect(*p5, *p18, *p6)
    state.rect(*p7, *p20, *p19)
    state.rect(*p6, *p11, *p7)
    state.rect(*p1, *p8, *p4)

def example_boxy_s(state: State):
    side = 2
    state.box(0, 0, 0, side)
    state.box(0, 0, side, side)
    state.box(side, 0, 0, side)
    state.box(side * 2, 0, 0, side)
    state.cuboid(side * 2, 0, side, side, side, side * 3)
    state.box(side * 2, 0, side * 4, side)
    state.box(side * 3, 0, side * 4, side)
    state.box(side * 4, 0, side * 4, side)
    state.box(side * 4, 0, side * 3, side)
    state.rect(
        side * 4, 0, side*3,
        side * 4, 0, 0,
        side * 7, 0, 0,
    )


if __name__ == "__main__":
    main()
