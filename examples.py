from main import State

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



def example_gap_cup(state: State):
    u = 50
    base = 40
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


def example_predefined_points(state: State):
    u = 28

    p1 = [0, 0, 0]
    p2 = [u, 0, 0]
    p3 = [2 * u, 0, 0]
    p4 = [3 * u, 0, 0]
    p5 = [0, u, 0]
    p6 = [u, u, 0]
    p7 = [2 * u, u, 0]
    p8 = [3 * u, u, 0]

    p9 = [u, 0, u]
    p10 = [2 * u, 0, u]
    p11 = [2 * u, u, u]
    p12 = [u, u, u]

    p13 = [0, 0, 2 * u]
    p14 = [u, 0, 2 * u]
    p15 = [2 * u, 0, 2 * u]
    p16 = [3 * u, 0, 2 * u]
    p17 = [0, u, 2 * u]
    p18 = [u, u, 2 * u]
    p19 = [2 * u, u, 2 * u]
    p20 = [3 * u, u, 2 * u]

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
        side * 4,
        0,
        side * 3,
        side * 4,
        0,
        0,
        side * 7,
        0,
        0,
    )
