from typing import Union, List
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
    points: List[Point]
    def __init__(self, points: List[Point]):
        self.points = points

def main():

    if len(sys.argv) > 2 and sys.argv[1] == 'obj':
        obj_str = box(0,0,0, 100, 'obj')

        square(0, 0, 0, 100)

        with open(sys.argv[2], 'w') as f:
            f.write(str(obj_str))
    else:
        mpl.rcParams['legend.fontsize'] = 10

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        xs, ys, zs = box(0,0,0, 100)

        ax.plot(xs, ys, zs)
        ax.legend()

        plt.show()

def box(x: int, y: int, z: int, side: int, format: str = 'matplotlib') -> Union[List[List[int]], str]:
    if format == 'obj':
        x1_str = f"{x:.5f}"
        y1_str = f"{y:.5f}"
        z1_str = f"{z:.5f}"
        z2_str = f"{z+side:.5f}"
        x2_str = f"{x+side:.5f}"
        y2_str = f"{y+side:.5f}"
        obj_str =  f'''mtllib master.mtl
v {x1_str} {y1_str} {z1_str}
v {x2_str} {y1_str} {z1_str}
v {x2_str} {y2_str} {z1_str}
v {x1_str} {y2_str} {z1_str}

v {x1_str} {y1_str} {z2_str}
v {x2_str} {y1_str} {z2_str}
v {x2_str} {y2_str} {z2_str}
v {x1_str} {y2_str} {z2_str}

f 1 2 3 4
f 5 6 7 8

f 1 2 6 5
f 3 4 8 7

f 2 3 7 6
f 4 1 5 8

usemtl wood
'''
        return obj_str
    else:
        points =  [
            [x,y,z],
            [x+side,y,z],
            [x+side,y+side,z],
            [x,y+side,z],
            [x,y,z],
            [x,y,z+side],
            [x+side,y,z+side],
            [x+side,y,z],
            [x+side,y,z+side],
            [x+side,y+side,z+side],
            [x+side,y+side,z],
            [x+side,y+side,z+side],
            [x,y+side,z+side],
            [x,y+side,z],
            [x,y+side,z+side],
            [x,y,z+side],
        ]
        return [
            [x[0] for x in points],
            [x[1] for x in points],
            [x[2] for x in points],
        ]

def square(x: int, y: int, z: int, side: int, ignored_axis: str = 'z') -> List[Point]:
    '''
    returns {
        xs: list of numbers for x dimension
        ys: list of numbers for y dimension
        zs: list of numbers for z dimension
    }
    '''

    points: List[Point] = []
    if ignored_axis == 'y':
        points.append(Point(x,y,z))
        points.append(Point(x+side,y,z))
        points.append(Point(x+side,y,z+side))
        points.append(Point(x,y,z+side))
        points.append(Point(x,y,z))
    if ignored_axis == 'x':
        points.append(Point(x,y,z))
        points.append(Point(x,y,z+side))
        points.append(Point(x,y+side,z+side))
        points.append(Point(x,y+side,z))
        points.append(Point(x,y,z))
    else:
        points.append(Point(x,y,z))
        points.append(Point(x+side,y,z))
        points.append(Point(x+side,y+side,z))
        points.append(Point(x,y+side,z))
        points.append(Point(x,y,z))

    print(points)
    return points

    # return [
    #     [x[0] for x in points],
    #     [x[1] for x in points],
    #     [x[2] for x in points],
    # ]

if __name__ == '__main__':
    main()
