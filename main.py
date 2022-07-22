#!/usr/bin/env python

from __future__ import annotations

from typing import List, Set
import argparse
from pyrender import start
from examples import *


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
        print(f"point: {len(self.points)}, faces: {len(self.faces)}")
        self.obj_str += points_str(self.points)
        self.obj_str += faces_str(self.faces)

    def remove_duplicate_points(self):
        duplicate_point_indexes: Set[int] = set()
        for j in range(len(self.points)):
            if j in duplicate_point_indexes:
                continue
            first_point = self.points[j]
            first = first_point.x + first_point.y * 1000 + first_point.z * 1000000

            for k in range(j + 1, len(self.points)):
                if k in duplicate_point_indexes:
                    continue
                second_point = self.points[k]
                second = (
                    second_point.x + second_point.y * 1000 + second_point.z * 1000000
                )

                if first == second:
                    duplicate_point_indexes.add(second_point.index)
                    for face in self.faces:
                        if second_point.index in face.point_indexes:
                            index_index = face.point_indexes.index(second_point.index)
                            print("on pos", index_index)
                            print("face", face.point_indexes)
                            print("from", second_point.index)
                            print("to", first_point.index)
                            face.point_indexes[index_index] = first_point.index
                            print("after face", face.point_indexes)

        # print('before', len(self.points))
        # new_points = [p for p in self.points if p.index not in duplicate_point_indexes]
        # print('after', len(new_points))
        # self.points = new_points

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
        # assert (
        #     len(list(filter(lambda x: x is not None, [g_x, g_y, g_z]))) == 2
        # ), "Expected 2 gap params"

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
        self.points += points

        bottom = [offset + 1, offset + 2, offset + 4, offset + 3]
        top = [offset + 5, offset + 6, offset + 8, offset + 7]
        left = [offset + 1, offset + 3, offset + 7, offset + 5]
        right = [offset + 2, offset + 4, offset + 8, offset + 6]
        front = [offset + 1, offset + 2, offset + 6, offset + 5]
        back = [offset + 3, offset + 4, offset + 8, offset + 7]

        faces: List[Face] = []

        if g_x is None and g_y is None and g_z is None:
            faces = [Face(x) for x in [front, back, left, right, top, bottom]]
        elif g_x is None:
            if g_y is not None and g_z is not None:
                faces = [Face(x) for x in [top, bottom, front, back]]
                for x_offset in [x, x + w_x]:
                    self.rect(
                        x_offset, y, z, x_offset, y + g_y, z + g_z, x_offset, y + g_y, z
                    )
                    self.rect(
                        x_offset,
                        y,
                        z + g_z,
                        x_offset,
                        y + g_y,
                        z + w_z - g_z,
                        x_offset,
                        y + g_y,
                        z + g_z,
                    )
                    self.rect(
                        x_offset,
                        y,
                        z + w_z - g_z,
                        x_offset,
                        y + g_y,
                        z + w_z,
                        x_offset,
                        y + g_y,
                        z + w_z - g_z,
                    )

                    self.rect(
                        x_offset,
                        y + w_y - g_y,
                        z,
                        x_offset,
                        y + w_y,
                        z + g_z,
                        x_offset,
                        y + w_y,
                        z,
                    )
                    self.rect(
                        x_offset,
                        y + w_y - g_y,
                        z + g_z,
                        x_offset,
                        y + w_y,
                        z + w_z - g_z,
                        x_offset,
                        y + w_y,
                        z + g_z,
                    )
                    self.rect(
                        x_offset,
                        y + w_y - g_y,
                        z + w_z - g_z,
                        x_offset,
                        y + w_y,
                        z + w_z,
                        x_offset,
                        y + w_y,
                        z + w_z - g_z,
                    )

                    self.rect(
                        x_offset,
                        y + g_y,
                        z,
                        x_offset,
                        y + w_y - g_y,
                        z + g_z,
                        x_offset,
                        y + w_y - g_y,
                        z,
                    )
                    self.rect(
                        x_offset,
                        y + g_y,
                        z + w_z - g_z,
                        x_offset,
                        y + w_y - g_y,
                        z + w_z,
                        x_offset,
                        y + w_y - g_y,
                        z + w_z - g_z,
                    )
                self.rect(
                    x,
                    y + g_y,
                    z + g_z,
                    x + w_x,
                    y + w_y - g_y,
                    z + g_z,
                    x,
                    y + w_y - g_y,
                    z + g_z,
                )
                self.rect(
                    x,
                    y + g_y,
                    z + w_z - g_z,
                    x + w_x,
                    y + w_y - g_y,
                    z + w_z - g_z,
                    x,
                    y + w_y - g_y,
                    z + w_z - g_z,
                )

                self.rect(
                    x,
                    y + g_y,
                    z + g_z,
                    x + w_x,
                    y + g_y,
                    z + w_z - g_z,
                    x + w_x,
                    y + g_y,
                    z + g_z,
                )
                self.rect(
                    x,
                    y + w_y - g_y,
                    z + g_z,
                    x + w_x,
                    y + w_y - g_y,
                    z + w_z - g_z,
                    x + w_x,
                    y + w_y - g_y,
                    z + g_z,
                )

        elif g_y is None:
            faces = [Face(x) for x in [top, bottom, left, right]]
            if g_x is not None and g_z is not None:
                for y_offset in [y, y + w_y]:
                    self.rect(
                        x, y_offset, z, x + g_x, y_offset, z + g_z, x + g_x, y_offset, z
                    )
                    self.rect(
                        x,
                        y_offset,
                        z + g_z,
                        x + g_x,
                        y_offset,
                        z + w_z - g_z,
                        x + g_x,
                        y_offset,
                        z + g_z,
                    )
                    self.rect(
                        x,
                        y_offset,
                        z + w_z - g_z,
                        x + g_x,
                        y_offset,
                        z + w_z,
                        x + g_x,
                        y_offset,
                        z + w_z - g_z,
                    )

                    self.rect(
                        x + w_x - g_x,
                        y_offset,
                        z,
                        x + w_x,
                        y_offset,
                        z + g_z,
                        x + w_x,
                        y_offset,
                        z,
                    )
                    self.rect(
                        x + w_x - g_x,
                        y_offset,
                        z + g_z,
                        x + w_x,
                        y_offset,
                        z + w_z - g_z,
                        x + w_x,
                        y_offset,
                        z + g_z,
                    )
                    self.rect(
                        x + w_x - g_x,
                        y_offset,
                        z + w_z - g_z,
                        x + w_x,
                        y_offset,
                        z + w_z,
                        x + w_x,
                        y_offset,
                        z + w_z - g_z,
                    )

                    self.rect(
                        x + g_x,
                        y_offset,
                        z,
                        x + w_x - g_x,
                        y_offset,
                        z + g_z,
                        x + w_x - g_x,
                        y_offset,
                        z,
                    )
                    self.rect(
                        x + g_x,
                        y_offset,
                        z + w_z - g_z,
                        x + w_x - g_x,
                        y_offset,
                        z + w_z,
                        x + w_x - g_x,
                        y_offset,
                        z + w_z - g_z,
                    )
                self.rect(
                    x + g_x,
                    y,
                    z + g_z,
                    x + w_x - g_x,
                    y + w_y,
                    z + g_z,
                    x + g_x,
                    y + w_y,
                    z + g_z,
                )
                self.rect(
                    x + g_x,
                    y,
                    z + w_z - g_z,
                    x + w_x - g_x,
                    y + w_y,
                    z + w_z - g_z,
                    x + g_x,
                    y + w_y,
                    z + w_z - g_z,
                )

                self.rect(
                    x + g_x,
                    y,
                    z + g_z,
                    x + g_x,
                    y + w_y,
                    z + w_z - g_z,
                    x + g_x,
                    y + w_y,
                    z + g_z,
                )
                self.rect(
                    x + w_x - g_x,
                    y,
                    z + g_z,
                    x + w_x - g_x,
                    y + w_y,
                    z + w_z - g_z,
                    x + w_x - g_x,
                    y + w_y,
                    z + g_z,
                )
        elif g_z is None:
            faces = [Face(x) for x in [front, back, left, right]]
            if g_x is not None and g_y is not None:
                for z_offset in [z, z + w_z]:
                    self.rect(
                        x, y, z_offset, x + g_x, y + g_y, z_offset, x, y + g_y, z_offset
                    )
                    self.rect(
                        x,
                        y + g_y,
                        z_offset,
                        x + g_x,
                        y + w_y - g_y,
                        z_offset,
                        x,
                        y + w_y - g_y,
                        z_offset,
                    )
                    self.rect(
                        x,
                        y + w_y - g_y,
                        z_offset,
                        x + g_x,
                        y + w_y,
                        z_offset,
                        x,
                        y + w_y,
                        z_offset,
                    )

                    self.rect(
                        x + w_x - g_x,
                        y,
                        z_offset,
                        x + w_x,
                        y + g_y,
                        z_offset,
                        x + w_x - g_x,
                        y + g_y,
                        z_offset,
                    )
                    self.rect(
                        x + w_x - g_x,
                        y + g_y,
                        z_offset,
                        x + w_x,
                        y + w_y - g_y,
                        z_offset,
                        x + w_x - g_x,
                        y + w_y - g_y,
                        z_offset,
                    )
                    self.rect(
                        x + w_x - g_x,
                        y + w_y - g_y,
                        z_offset,
                        x + w_x,
                        y + w_y,
                        z_offset,
                        x + w_x - g_x,
                        y + w_y,
                        z_offset,
                    )

                    self.rect(
                        x + g_x,
                        y,
                        z_offset,
                        x + w_x - g_x,
                        y + g_y,
                        z_offset,
                        x + g_x,
                        y + g_y,
                        z_offset,
                    )
                    self.rect(
                        x + g_x,
                        y + w_y - g_y,
                        z_offset,
                        x + w_x - g_x,
                        y + w_y,
                        z_offset,
                        x + g_x,
                        y + w_y,
                        z_offset,
                    )
                self.rect(
                    x + g_x,
                    y + g_y,
                    z,
                    x + w_x - g_x,
                    y + g_y,
                    z + w_z,
                    x + g_x,
                    y + g_y,
                    z + w_z,
                )
                self.rect(
                    x + g_x,
                    y + w_y - g_y,
                    z,
                    x + w_x - g_x,
                    y + w_y - g_y,
                    z + w_z,
                    x + g_x,
                    y + w_y - g_y,
                    z + w_z,
                )

                self.rect(
                    x + g_x,
                    y + g_y,
                    z,
                    x + g_x,
                    y + w_y - g_y,
                    z + w_z,
                    x + g_x,
                    y + g_y,
                    z + w_z,
                )
                self.rect(
                    x + w_x - g_x,
                    y + g_y,
                    z,
                    x + w_x - g_x,
                    y + w_y - g_y,
                    z + w_z,
                    x + w_x - g_x,
                    y + g_y,
                    z + w_z,
                )

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
        """
        Creates rectangular face between given 3 corners, calculating 4th one
        First 2 points must cross diagonally
        """
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
    state.remove_duplicate_points()
    state.write_obj_str()

    with open(args.filename, "w") as f:
        f.write(state.obj_str)

    if args.preview_mode:
        start(args.filename)


def generate_logic(state: State):
    example_gap(state)


if __name__ == "__main__":
    main()
