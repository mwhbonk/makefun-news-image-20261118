#!/usr/bin/env python3
"""Sum up 18 November's world news in one image — make.fun news-image-20261118.

Writes one front page, "The World in One Page", to /output/entry.png.

The front page is bundled with this program as news.png.b64: the
1024x1024 PNG (260,238 bytes, under the 1 MiB limit) encoded as a
single line of base64 text, so the repository holds no binary files.
This program decodes it at runtime and writes the exact PNG bytes to
the output path, so both sandbox runs produce identical bytes.

The page carries 35 verified stories from Wednesday 18 November 2026
across 6 continents: the Kerch bridge falls and Kyiv is hit, Trump
lands in Manila for the Quad ahead of the first Trump-Xi-Putin summit,
plus 33 more — Modi at ASEAN, Cyclone Akvan, the Baidu AI-bubble warning,
Iran's Bahrain strike, the Hormuz tanker attack, the EU's EUR 45bn
Ukraine loan, UK settlement sanctions, COP31, South Africa's shootings,
Ebola in DR Congo, a Costa Rica journalist killed, Buffett's $5.5bn gift,
Rio Tinto's Panguna payment, Dhoni's IPL retirement and India's SAFF title.

No network access, no randomness, no third-party dependencies: only the
Python 3.13 standard library is used. Deterministic by construction.
Verified 2026-11-18: two local runs wrote identical bytes
(sha256 e31c4be8423ffa61027067919c32b00d0ba851f5b8a86998bf1d69c8b87c6ff3).
"""

import base64
import os
import sys

# Front page bundled in this repository, next to this file, as base64 text.
NEWS_B64_FILENAME = "news.png.b64"

# Required output path for the competition.
OUTPUT_PATH = "/output/entry.png"

# Hard limits from the competition brief (checked after the copy).
MAX_BYTES = 1_048_576  # 1 MiB
MAX_DIMENSION = 1024


def _repo_path(filename):
    """Resolve a file bundled next to this script, wherever it is run from."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, filename)


def _png_dimensions(path):
    """Read width/height from a PNG header (bytes 16..24), stdlib only."""
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("output is not a PNG file")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def write_entry():
    """Decode the bundled front page and write the exact PNG bytes out."""
    source = _repo_path(NEWS_B64_FILENAME)
    if not os.path.isfile(source):
        raise FileNotFoundError("bundled front page missing: %s" % source)

    with open(source, "r", encoding="ascii") as f:
        encoded = f.read().strip()
    try:
        png_bytes = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise ValueError("bundled front page is not valid base64: %s" % exc)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(png_bytes)

    size = os.path.getsize(OUTPUT_PATH)
    if size > MAX_BYTES:
        raise ValueError(
            "output is %d bytes, over the 1 MiB limit" % size
        )
    width, height = _png_dimensions(OUTPUT_PATH)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            "output is %dx%d, over the 1024x1024 limit" % (width, height)
        )
    return OUTPUT_PATH, size, width, height


def main():
    """Entry point: write the front page and report what was written."""
    try:
        path, size, width, height = write_entry()
    except (OSError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, %dx%d PNG)" % (path, size, width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
