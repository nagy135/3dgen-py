#!/usr/bin/env python

import argparse
from pyrender import start
from examples import *
from state import State

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

    state.update_str_state()

    with open(args.filename, "w") as f:
        f.write(state.stl_str)

    if args.preview_mode:
        start(args.filename)


def generate_logic(state: State):
    example_face(state)


if __name__ == "__main__":
    main()
