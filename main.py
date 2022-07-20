from __future__ import annotations

from typing import List
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
import sys

warnings.filterwarnings("ignore")


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

    def box(
        self, x: int, y: int, z: int, side: int, format: str = "matplotlib"
    ) -> State:
        if format == "obj":
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
        else:
            points = [
                [x, y, z],
                [x + side, y, z],
                [x + side, y + side, z],
                [x, y + side, z],
                [x, y, z],
                [x, y, z + side],
                [x + side, y, z + side],
                [x + side, y, z],
                [x + side, y, z + side],
                [x + side, y + side, z + side],
                [x + side, y + side, z],
                [x + side, y + side, z + side],
                [x, y + side, z + side],
                [x, y + side, z],
                [x, y + side, z + side],
                [x, y, z + side],
            ]
            self.points += [Point(x=j[0], y=j[1], z=j[2]) for j in points]
            return self

    def dump_axes(self):
        return [
            [point.x for point in self.points],
            [point.y for point in self.points],
            [point.z for point in self.points],
        ]


def main():

    state = State()
    if len(sys.argv) > 2 and sys.argv[1] == "obj":
        state.box(0, 0, 0, 20, "obj")
        state.box(20, 0, 0, 20, "obj")
        state.box(0, 20, 0, 20, "obj")
        state.box(0, 0, 20, 20, "obj")

        with open(sys.argv[2], "w") as f:
            f.write(state.obj_str)
    else:
        mpl.rcParams["legend.fontsize"] = 10
        fig = plt.figure()
        ax = fig.gca(projection="3d")

        state.box(0, 0, 0, 100)

        xs, ys, zs = state.dump_axes()

        ax.plot(xs, ys, zs)
        ax.legend()

        plt.show()


#
# def square(x: int, y: int, z: int, side: int, ignored_axis: str = 'z') -> Face:
#     points: List[Point] = []
#     if ignored_axis == 'y':
#         points.append(Point(x,y,z))
#         points.append(Point(x+side,y,z))
#         points.append(Point(x+side,y,z+side))
#         points.append(Point(x,y,z+side))
#         points.append(Point(x,y,z))
#     if ignored_axis == 'x':
#         points.append(Point(x,y,z))
#         points.append(Point(x,y,z+side))
#         points.append(Point(x,y+side,z+side))
#         points.append(Point(x,y+side,z))
#         points.append(Point(x,y,z))
#     else:
#         points.append(Point(x,y,z))
#         points.append(Point(x+side,y,z))
#         points.append(Point(x+side,y+side,z))
#         points.append(Point(x,y+side,z))
#         points.append(Point(x,y,z))
#
#     face = Face(points)
#     return face


if __name__ == "__main__":
    main()
