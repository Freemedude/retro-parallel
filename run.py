#!/usr/bin/env python

import src.game
import sys
import os

# call the "main" function if running this script

# Packing requires aseprite on the path!
def pack():
    in_dir = os.path.join("data", "animations")
    out_dir = os.path.join(in_dir, "out")
    os.system(f"aseprite -b {in_dir}{os.sep}*.aseprite --sheet-pack --ignore-empty --split-layers --sheet {out_dir}{os.sep}texture-atlas.png --data {out_dir}{os.sep}texture-atlas.json")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "pack":
        pack()
    src.game.main()


if __name__ == "__main__":
    main()    

