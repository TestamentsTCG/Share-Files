#!/usr/bin/env python3
"""
build_gump_mul.py - Converts gumpartLegacyMUL.uop to Gumpart.mul + Gumpidx.mul
then injects custom gumps from a batch file.

Run as Administrator on the desktop PC. Usage:
  python build_gump_mul.py [--uo-dir "C:\\path"] [--batch file.txt] [--png-dir .]
"""
import struct, zlib, os, sys, argparse
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

UO_DIR_DEFAULT = r"C:\Program Files (x86)\Electronic Arts\Ultima Online Classic"
MASK = 0xFFFFFFFF

# ── Jenkins hashlittle2 (correct UO UOP hash) ─────────────────────────────────

def _rot(x, k): return ((x << k) | (x >> (32 - k))) & MASK

def _mix(a, b, c):
    a=(a-c)&MASK; a^=_rot(c,4);  c=(c+b)&MASK
    b=(b-a)&MASK; b^=_rot(a,6);  a=(a+c)&MASK
    c=(c-b)&MASK; c^=_rot(b,8);  b=(b+a)&MASK
    a=(a-c)&MASK; a^=_rot(c,16); c=(c+b)&MASK
    b=(b-a)&MASK; b^=_rot(a,19); a=(a+c)&MASK
    c=(c-b)&MASK; c^=_rot(b,4);  b=(b+a)&MASK
    return a,b,c

def _final(a, b, c):
    c^=b; c=(c-_rot(b,14))&MASK
    a^=c; a=(a-_rot(c,11))&MASK
    b^=a; b=(b-_rot(a,25))&MASK
    c^=b; c=(c-_rot(b,16))&MASK
    a^=c; a=(a-_rot(c,4))&MASK
    b^=a; b=(b-_rot(a,14))&MASK
    c^=b; c=(c-_rot(b,24))&MASK
    return a,b,c

def uop_hash(s):
    data = s.lower().encode('latin-1') if isinstance(s, str) else s
    n = len(data)
    a = b = c = (0xDEADBEEF + n) & MASK
    i = 0
    while i + 12 <= n:
        a=(a+struct.unpack_from('<I',data,i)[0])&MASK
        b=(b+struct.unpack_from('<I',data,i+4)[0])&MASK
        c=(c+struct.unpack_from('<I',data,i+8)[0])&MASK
        a,b,c=_mix(a,b,c)
        i+=12
    rem=n-i
    if rem>0:
        pad=data[i:]+b'\x00'*(12-rem)
        if rem>0:  a=(a+struct.unpack_from('<I',pad,0)[0])&MASK
        if rem>4:  b=(b+struct.unpack_from('<I',pad,4)[0])&MASK
        if rem>8:  c=(c+struct.unpack_from('<I',pad,8)[0])&MASK
    a,b,c=_final(a,b,c)
    return (b<<32)|c

PATH_FMT = "build/gumpartlegacymul/{:08d}.tga"

# ── UOP reader ────────────────────────────────────────────────────────────────

def read_uop(path):
    entries = {}
    with open(path,'rb') as f:
        f.read(4)  # magic
        version = struct.unpack('<I',f.read(4))[0]
        f.read(4)  # misc
        first = struct.unpack('<Q',f.read(8))[0]
        f.read(4)  # block_cap
        total = struct.unpack('<I',f.read(4))[0]
        print(f"  UOP v{version}: {total} declared files, first_block=0x{first:X}")
        block = first
        while block:
            f.seek(block)
            num = struct.unpack('<I',f.read(4))[0]
            nxt = struct.unpack('<Q',f.read(8))[0]
            for _ in range(num):
                doff=struct.unpack('<Q',f.read(8))[0]
                hsz=struct.unpack('<I',f.read(4))[0]
                csz=struct.unpack('<I',f.read(4))[0]
                dsz=struct.unpack('<I',f.read(4))[0]
                fhash=struct.unpack('<Q',f.read(8))[0]
                f.read(4+2)  # adler, comp_type
                if doff and csz:
                    pos=f.tell()
                    f.seek(doff+hsz)
                    raw=f.read(csz)
                    # re-read comp_type (we skipped it)
                    f.seek(pos-2)
                    ctype=struct.unpack('<H',f.read(2))[0]
                    f.seek(pos)
                    if ctype==1:
                        try: raw=zlib.decompress(raw)
                        except: pass
                    entries[fhash]=raw
            block=nxt
    print(f"  Loaded {len(entries)} entries")
    return entries


def uop_to_gump_map(entries, max_id=70000):
    gumps = {}
    for gid in range(max_id):
        h = uop_hash(PATH_FMT.format(gid))
        if h in entries:
            gumps[gid] = entries[h]
    return gumps

# ── PNG to UO gump data ───────────────────────────────────────────────────────

def png_to_uo_gump(png_path):
    """Convert PNG (black = transparent) to UO gump.mul binary format."""
    img = Image.open(png_path).convert('RGBA')
    w, h = img.size
    pix = list(img.getdata())
    rows=[]
    for y in range(h):
        row=[]
        for x in range(w):
            r,g,b,a=pix[y*w+x]
            if a<128 or (r==0 and g==0 and b==0):
                row.append(0)
            else:
                p=((r>>3)<<10)|((g>>3)<<5)|(b>>3)
                row.append((p|0x8000) if p else 0x0421)
        rows.append(row)
    # row offset table (in uint16 words from start of pixel data)
    pixel=bytearray()
    offs=[]
    off=0
    for row in rows:
        offs.append(off)
        pixel+=struct.pack(f'<{len(row)}H',*row)
        off+=len(row)
    return w, h, struct.pack(f'<{h}I',*offs)+bytes(pixel)

# ── Build ─────────────────────────────────────────────────────────────────────

def build(uop_path, mul_path, idx_path, custom_gumps):
    print(f"\nReading {uop_path}...")
    raw = read_uop(uop_path)

    print("Matching hashes to gump IDs...")
    gump_data = uop_to_gump_map(raw)
    print(f"  Matched {len(gump_data)} vanilla gumps (IDs 0-{max(gump_data)})") if gump_data else None

    if not gump_data:
        print("FATAL: No gumps matched. Aborting.")
        sys.exit(1)

    all_ids = list(gump_data.keys()) + [g[0] for g in custom_gumps]
    max_id = max(all_ids) + 1
    idx = [(0xFFFFFFFF,0,0)] * max_id

    print(f"\nWriting Gumpart.mul ({max_id} max ID)...")
    written = 0
    with open(mul_path,'wb') as f:
        for gid in sorted(gump_data.keys()):
            off = f.tell()
            f.write(gump_data[gid])
            idx[gid] = (off, len(gump_data[gid]), 0)
            written += 1

        if custom_gumps:
            if not HAS_PIL:
                print("ERROR: Pillow needed for PNG injection. Run: python -m pip install pillow")
            else:
                print(f"Injecting {len(custom_gumps)} custom gumps...")
                for gid, png in custom_gumps:
                    try:
                        w,h,data=png_to_uo_gump(png)
                        off=f.tell()
                        f.write(data)
                        while len(idx)<=gid: idx.append((0xFFFFFFFF,0,0))
                        idx[gid]=(off,len(data),0)
                        print(f"  OK [{gid}]: {os.path.basename(png)} {w}x{h} -> @{off}, {len(data)}B")
                        written+=1
                    except Exception as e:
                        print(f"  ERR [{gid}]: {e}")

    print(f"Writing Gumpidx.mul ({len(idx)} entries)...")
    with open(idx_path,'wb') as f:
        for o,l,e in idx:
            f.write(struct.pack('<III',o,l,e))

    print(f"\nDone! {written} gumps written.")
    print(f"  Gumpart.mul : {os.path.getsize(mul_path):>12,} bytes")
    print(f"  Gumpidx.mul : {os.path.getsize(idx_path):>12,} bytes")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap=argparse.ArgumentParser(description='Build Gumpart.mul+Gumpidx.mul from UOP + inject custom gumps')
    ap.add_argument('--uo-dir', default=UO_DIR_DEFAULT)
    ap.add_argument('--output-dir', default=None, help='Write .mul files here instead of --uo-dir (for testing)')
    ap.add_argument('--batch', default='all_classes_gumps.txt')
    ap.add_argument('--png-dir', default='.')
    args=ap.parse_args()

    uo=Path(args.uo_dir)
    uop=uo/'gumpartLegacyMUL.uop'
    if not uop.exists():
        bak=uo/'gumpartLegacyMUL.uop.bak'
        if bak.exists(): uop=bak
        else: sys.exit(f"Cannot find {uop}")

    custom=[]
    bp=Path(args.batch)
    if bp.exists():
        pd=Path(args.png_dir)
        for line in bp.read_text().splitlines():
            line=line.strip()
            if not line or line.startswith('#'): continue
            parts=line.split(None,1)
            if len(parts)==2:
                gid,png=int(parts[0]),pd/parts[1]
                if png.exists(): custom.append((gid,str(png)))
                else: print(f"  SKIP: {png}")
        print(f"Batch: {len(custom)} custom gumps from {bp}")

    out = Path(args.output_dir) if args.output_dir else uo
    out.mkdir(parents=True, exist_ok=True)
    mul=out/'Gumpart.mul'
    idx=out/'Gumpidx.mul'
    build(str(uop), str(mul), str(idx), custom)

    # Rename .uop -> .bak so ClassicUO reads .mul
    active=uo/'gumpartLegacyMUL.uop'
    if active.exists() and str(uop)!=str(active.with_suffix('.uop.bak')):
        try:
            active.rename(active.with_suffix('.uop.bak'))
            print("  .uop -> .uop.bak (ClassicUO will use .mul now)")
        except Exception as e:
            print(f"  Could not rename .uop (rename manually): {e}")

if __name__ == '__main__':
    main()
