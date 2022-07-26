#!/usr/bin/env python

import argparse
from examples import *
import os
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


    state = State()

    generate_logic(state)

    state.update_str_state()

    with open(args.filename, "w") as f:
        f.write(state.stl_str)

    if args.preview_mode:
        os.system(f"stlviewer {args.filename}")


def generate_logic(state: State):
    example_prism(state)


if __name__ == "__main__":
    main()
