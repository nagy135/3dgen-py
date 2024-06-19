from __future__ import annotations

from typing import List, Set
import sys

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

                first = [point.x + point.y * 1000 + point.z * 1000000 for point in points]
                second = [point.x + point.y * 1000 + point.z * 1000000 for point in points2]

                if set(first) == set(second):
                    duplicate_face_indexes.add(k)

        print("dupl", duplicate_face_indexes)
        new_faces = []
        for index in range(len(self.faces)):
            if index not in duplicate_face_indexes:
                new_faces.append(self.faces[index])
        self.faces = new_faces

    def box(
        self, x: int, y: int, z: int, side: int
    ) -> State:
        coordinates = [
            [x, y, z],
            [x + side, y, z],
            [x, y + side, z],
            [x + side, y + side, z],
            [x, y, z + side],
            [x + side, y, z + side],
            [x, y + side, z + side],
            [x + side, y + side, z + side],
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

        self.obj_str += points_str(points)
        self.obj_str += faces_str(faces)

        return self

def main():

    state = State()
    side = 20
    x_offset = 0
    z_offset = 0
    for _ in range(1, 7):
        state.box(x_offset, 0, z_offset, side)
        x_offset += side
        state.box(x_offset, 0, z_offset, side)
        z_offset += side
        state.box(x_offset, 0, z_offset, side)
        z_offset += side

    state.remove_duplicate_faces()

    with open(sys.argv[1], "w") as f:
        f.write(state.obj_str)

if __name__ == "__main__":
    main()
