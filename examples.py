from main import State

from PIL import Image
import numpy as np

def example_gap(state: State):
    gap = 5
    u = 50
    state.cuboid(u, 0, u, u, u, u, gap, None, gap)

def example_face(state: State):
    u = 10
    state.rect(
        0, 0, 0,
        u, 0, u,
        u, 0, 0,
        0, -1, 0
    )
def window_part(state: State):
    small_arm = 10
    longer_arm = 15
    long_arm = 53
    height = 15
    gap_border_width = 1.3

    u = 2
    state.cuboid(0,u,0,u,u,height)
    state.cuboid(0,0,0,u, u, height)
    state.cuboid(u,0,0, small_arm, u, height)
    state.cuboid(u+small_arm,0,0,u, u, height)

    n = 10
    piece_width = long_arm/n
    for i in range(n):
        state.cuboid(
            u+small_arm,
            u+i*piece_width,
            0,
            u,
            piece_width,
            height,
            None,
            gap_border_width,
            gap_border_width
        )


    state.cuboid(u+small_arm,u+long_arm,0,u, u, height)
    state.cuboid(u+small_arm,u+long_arm,0,-longer_arm+u, u, height)
    state.cuboid(u+small_arm-longer_arm,long_arm+u,0,u, u, height)
    state.cuboid(u+small_arm-longer_arm,long_arm,0,u, u, height)
    state.cuboid(u+small_arm-longer_arm,long_arm-u,0,u, u, height)

def example_prism(state: State):
    u = 40
    p1 = (0, 0, u)
    p2 = (u, 0, u)
    p3 = (u, u, u)
    p4 = (0, u, u)
    p5 = (u/2, u/2, u*2)
    state.box(0,0,0, u)
    state.prism(
        *p1,
        *p2,
        *p4,
        *p5
    )
    state.prism(
        *p2,
        *p3,
        *p4,
        *p5
    )

def example_castle(state: State):
    u = 30
    gap = 3

    # BASE
    state.box(0,0,0, u)
    state.box(u,0,0, u)
    state.box(2*u,0,0, u)
    state.box(0,2*u,0, u)
    state.box(u,2*u,0, u)
    state.box(2*u,2*u,0, u)
    state.box(0,u,0, u)
    state.box(2*u,u,0, u)

    for x,y in [(0,0),(2*u,0), (2*u, 2*u), (0, 2*u)]:
        state.box(x,y,u,u)
        state.box(x,y,u*2,u)
        p1 = (x, y, u*3)
        p2 = (x+u, y, u*3)
        p3 = (x+u, y+u, u*3)
        p4 = (x, y+u, u*3)
        p5 = (x+u/2, y+u/2, u*4)
        state.prism(
            *p1,
            *p2,
            *p4,
            *p5
        )
        state.prism(
            *p2,
            *p3,
            *p4,
            *p5
        )
    state.cuboid(0,u,u, u,u,u, gap, gap, None)
    state.cuboid(u*2,u,u, u,u,u, gap, gap, None)
    state.cuboid(u,0,u, u,u,u, gap, gap, None)
    state.cuboid(u,u*2,u, u,u,u, gap, gap, None)

def example_crown(state: State):
    u = 40
    p1 = (0, 0, u)
    p2 = (u, 0, u)
    p3 = (u, u, u)
    p4 = (0, u, u)

    p5 = (0, 0, 2*u)
    p6 = (u, u, 2*u)
    state.box(0,0,0,u)
    state.prism(
        *p1,
        *p2,
        *p4,
        *p5,
    )
    state.prism(
        *p2,
        *p3,
        *p4,
        *p6,
    )

def example_box(state: State):
    u = 60
    state.cuboid(
        0, 0, 0,
        u,u,u,
        None, 10, 10
    )
    state.cuboid(
        0, 0, u,
        u,u,u,
        10, 10, None
    )
    state.box(0,u,0,u)
    state.box(0,u,u,u)

    state.box(0,-u,0,u)
    state.box(0,-u,u,u)

def image(state: State):
    path = "test.jpeg"
    image = Image.open(path).convert('RGB')
    image = np.asarray(image)
    state.grid(len(image), len(image[0]), 3, 3)
    # for [ y, row ] in enumerate( image ):
    #     print(y)
    #     for [ x, pixel ] in enumerate(row):
    #         r,g,b = int(pixel[0]), int(pixel[1]), int(pixel[2])
    #         intensity = (r+g+b)/(256*3)



def example_gap_cup(state: State):
    u = 50
    handle = 10
    handle_spread = 20

    # base
    # state.cuboid(0, 0, 0, u, u, base)

    # body
    # state.cuboid(0, 0, base, u, u, u, gap, gap, None)

    # handle {{{
    # # boxes
    state.box(u, u/2, u/2 - handle_spread/2, handle)
    state.box(u, u/2, u/2 + handle_spread/2, handle)

    state.box(u+handle, u/2, u/2 - handle_spread/2, handle)
    state.box(u+handle, u/2, u/2 + handle_spread/2, handle)
    state.box(u+handle, u/2, handle + u/2 - handle_spread/2, handle)
    # }}}
