#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124.

Copies the pre-rendered broadsheet (entry.png, drawn by render.py in this
repository) to /output/entry.png. The run is deterministic: the same bytes
are written on every run, with no network access.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
