from typing import Dict, List
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

def main():

    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    xs, ys, zs = box(0,0,0, 100)

    ax.plot(xs, ys, zs)
    ax.legend()

    plt.show()

def box(x: int, y: int, z: int, side: int) -> List[List[int]]:
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

def concat_3d(head: List[List[int]], tail: List[List[int]]) -> List[List[int]]:
    return [
        head[0] + tail[0],
        head[1] + tail[1],
        head[2] + tail[2],
    ]
    

def square(x: int, y: int, z: int, side: int, ignored_axis: str = 'z') -> List[List[int]]:
    '''
    returns {
        xs: list of numbers for x dimension
        ys: list of numbers for y dimension
        zs: list of numbers for z dimension
    }
    '''

    points: List[List[int]] = []
    if ignored_axis == 'y':
        points: List[List[int]] = []
        points.append([x,y,z])
        points.append([x+side,y,z])
        points.append([x+side,y,z+side])
        points.append([x,y,z+side])
        points.append([x,y,z])
    if ignored_axis == 'x':
        points: List[List[int]] = []
        points.append([x,y,z])
        points.append([x,y,z+side])
        points.append([x,y+side,z+side])
        points.append([x,y+side,z])
        points.append([x,y,z])
    else:
        points.append([x,y,z])
        points.append([x+side,y,z])
        points.append([x+side,y+side,z])
        points.append([x,y+side,z])
        points.append([x,y,z])


    return [
        [x[0] for x in points],
        [x[1] for x in points],
        [x[2] for x in points],
    ]

if __name__ == '__main__':
    main()
