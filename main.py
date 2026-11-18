#!/usr/bin/env python3
"""Copy the front-page image for 18 November 2026 to the output directory.

The image lives next to this script as ``entry.png``. This program checks
that it really is a PNG of the expected size, then copies it unchanged to
``$MAKEFUN_OUTPUT_DIR/entry.png`` (``/output`` when the variable is unset).
Only the Python standard library is used and nothing is fetched over the
network, so running it twice always yields the same bytes.
"""

import os
import shutil
import struct
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
MAX_BYTES = 1_048_576


def fail(message):
    """Print an error to stderr and exit with a non-zero status."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_header(path):
    """Return the (width, height) stored in the PNG IHDR chunk."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        fail(f"{path} is not a PNG file (bad magic bytes)")
    chunk_length = struct.unpack(">I", head[8:12])[0]
    chunk_type = head[12:16]
    if chunk_type != b"IHDR" or chunk_length != 13:
        fail(f"{path} has no valid IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def check_trailer(path):
    """Confirm the file ends with a proper PNG IEND chunk."""
    with open(path, "rb") as handle:
        handle.seek(-12, os.SEEK_END)
        tail = handle.read(12)
    if len(tail) != 12 or tail[4:8] != b"IEND":
        fail(f"{path} is missing its IEND trailer chunk")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    destination = os.path.join(output_dir, "entry.png")

    if not os.path.isfile(source):
        fail(f"source image not found: {source}")

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        fail(
            f"{source} is {size} bytes, over the {MAX_BYTES} byte limit"
        )

    width, height = read_header(source)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        fail(
            f"image is {width}x{height}, over the "
            f"{MAX_WIDTH}x{MAX_HEIGHT} limit"
        )
    check_trailer(source)

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, destination)
    copied = os.path.getsize(destination)
    print(f"wrote {destination} ({copied} bytes)")


if __name__ == "__main__":
    main()
