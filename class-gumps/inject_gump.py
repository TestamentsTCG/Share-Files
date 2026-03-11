#!/usr/bin/env python
"""
inject_gump.py - Inject PNGs directly into Gumpart.mul + Gumpidx.mul
Bypasses UoFiddler entirely. gumpartLegacyMUL.uop stays as .bak forever.

Single inject:
  python inject_gump.py <gump_id> <input.png>

Batch inject (reads a text file, one "id path/to/file.png" per line):
  python inject_gump.py --batch <batchfile.txt>

Example batch file:
  42303 assassin_bg_fixed.png
  42304 assassin_btn_normal_fixed.png
  42305 assassin_btn_pressed_fixed.png

IMPORTANT: Must run as Administrator (UO dir is write-protected).
"""

import sys
import os
import struct
from PIL import Image

UO_DIR = r"C:\Program Files (x86)\Electronic Arts\Ultima Online Classic"
GUMPART_PATH = os.path.join(UO_DIR, "Gumpart.mul")
GUMPIDX_PATH = os.path.join(UO_DIR, "Gumpidx.mul")

GUMPIDX_ENTRY_SIZE = 12  # start (int32) + length (int32) + extra (int32)


def rgb_to_color16(r, g, b):
    """Convert 8-bit RGB to UO 16-bit RGB555. Returns 0 (transparent) for pure black."""
    r5 = r >> 3
    g5 = g >> 3
    b5 = b >> 3
    return (r5 << 10) | (g5 << 5) | b5


def encode_gump(img):
    """
    Encode a PIL Image (RGB mode) as Gumpart.mul binary data.
    Pure black (#000000) pixels → transparent (color=0).
    Returns (bytes, width, height).
    """
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()

    rows = []
    for y in range(height):
        row = []
        x = 0
        while x < width:
            r, g, b = pixels[x, y]
            color = rgb_to_color16(r, g, b)
            run_start = x
            x += 1
            while x < width:
                r2, g2, b2 = pixels[x, y]
                if rgb_to_color16(r2, g2, b2) != color:
                    break
                x += 1
            run = x - run_start
            # Split runs larger than 32767 (max int16) - shouldn't happen at UO sizes
            while run > 0:
                chunk = min(run, 32767)
                row.append((color, chunk))
                run -= chunk
        rows.append(row)

    # Build binary data block:
    # - Lookup table: height x int32, offsets in DWORDs from start of this gump's data
    # - Row data: (color: int16, run: int16) pairs per row

    # Lookup table occupies `height` DWORDs
    current_dword = height
    row_offsets = []
    for row in rows:
        row_offsets.append(current_dword)
        current_dword += len(row) * 2  # each pair = 2 x int16 = 4 bytes = 1 DWORD

    data = bytearray()
    for offset in row_offsets:
        data += struct.pack('<i', offset)
    for row in rows:
        for color, run in row:
            data += struct.pack('<hh', color, run)

    return bytes(data), width, height


def inject_gump(gump_id, png_path):
    """Inject a single PNG into Gumpart.mul at the given gump ID."""
    if not os.path.exists(png_path):
        print(f"  ERROR: File not found: {png_path}")
        return False

    img = Image.open(png_path)
    data, width, height = encode_gump(img)

    # Verify Gumpidx.mul is large enough to hold this entry
    idx_size = os.path.getsize(GUMPIDX_PATH)
    needed = (gump_id + 1) * GUMPIDX_ENTRY_SIZE
    if needed > idx_size:
        print(f"  ERROR: Gumpidx.mul too small ({idx_size} bytes) for gump ID {gump_id} (need {needed})")
        return False

    # Append gump data to Gumpart.mul
    gumpart_offset = os.path.getsize(GUMPART_PATH)
    with open(GUMPART_PATH, 'ab') as f:
        f.write(data)

    # Update Gumpidx.mul index entry
    # extra = (width << 16) | height  (per UO / UOFiddler convention)
    extra = (width << 16) | height
    entry = struct.pack('<iii', gumpart_offset, len(data), extra)
    with open(GUMPIDX_PATH, 'r+b') as f:
        f.seek(gump_id * GUMPIDX_ENTRY_SIZE)
        f.write(entry)

    print(f"  OK: gump {gump_id} ({width}x{height}) → offset {gumpart_offset}, {len(data)} bytes")
    return True


def inject_batch(batch_path):
    """
    Inject multiple gumps from a batch file.
    Format: one entry per line: <gump_id> <path_to_png>
    Lines starting with # are comments.
    """
    batch_dir = os.path.dirname(os.path.abspath(batch_path))
    success = 0
    fail = 0

    with open(batch_path, 'r') as f:
        lines = [l.strip() for l in f if l.strip() and not l.strip().startswith('#')]

    print(f"Batch inject: {len(lines)} entries from {batch_path}")
    for line in lines:
        parts = line.split(None, 1)
        if len(parts) != 2:
            print(f"  SKIP (bad line): {line}")
            continue
        gump_id = int(parts[0])
        png_path = parts[1]
        # Resolve relative paths relative to the batch file's directory
        if not os.path.isabs(png_path):
            png_path = os.path.join(batch_dir, png_path)
        if inject_gump(gump_id, png_path):
            success += 1
        else:
            fail += 1

    print(f"\nDone: {success} injected, {fail} failed")


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--batch':
        inject_batch(sys.argv[2])
    elif len(sys.argv) == 3:
        gump_id = int(sys.argv[1])
        inject_gump(gump_id, sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
