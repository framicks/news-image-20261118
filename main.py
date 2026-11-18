"""news-image-20261118: write the entry image to the output directory.

The image is a front-page summary of Wednesday 18 November 2026 world
news, stored in this repository as entry.png. This program copies it to
$MAKEFUN_OUTPUT_DIR/entry.png. It uses only the Python standard library
and needs no network. The output directory comes from the
MAKEFUN_OUTPUT_DIR environment variable and defaults to /output, the
make.fun sandbox layout.
"""

import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, destination)
    # Check the limits the competition gate enforces: at most 1 MiB and
    # at most 1024x1024 pixels.
    size = os.path.getsize(destination)
    if size > 1048576:
        print(f"entry.png is {size} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    print(f"wrote {destination} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
