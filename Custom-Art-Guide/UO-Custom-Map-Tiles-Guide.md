# UO Custom Map Tiles - Complete Production Guide
> Compiled: March 2026 | Source: UOFiddler source code, ServUO tutorials, CentrED# docs, ServUO community

---

## Table of Contents
1. [Technical Specs - Art.mul Format](#1-technical-specs)
2. [Complete Workflow - PNG to In-Game](#2-complete-workflow)
3. [Tools Reference](#3-tools-reference)
4. [Base UO Tile ID Reference](#4-base-uo-tile-ids)
5. [Outlands / Advanced Custom Tilesets](#5-outlands-and-advanced-tilesets)
6. [Python / C# Libraries](#6-libraries)
7. [Gaps / Unanswered Questions](#7-gaps)

---

## 1. Technical Specs

### 1.1 Art.mul File Overview

Art.mul stores all game art (terrain tiles and static object tiles). It is indexed by Artidx.mul (legacy) or artLegacyMUL.uop (High Seas+ clients).

**From UOFiddler Art.cs source (authoritative):**
```
FileIndex("Artidx.mul", "Art.mul", "artLegacyMUL.uop", 0x14000, 4, ".tga", 0x13FDC, false)
```

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Total entries | 0x14000 = **81,920** | Maximum art entries |
| Land tile range | 0x0000 - 0x3FFF | 16,384 terrain tiles |
| Static tile range | 0x4000 - 0x13FFF | 65,536 static/item tiles |
| Static ID internal offset | `item_id + 0x4000` | Static IDs are offset in the file |

**Version tiers (from IsUOAHS/GetMaxItemId):**
| Client Version | Max Item ID | idx Length |
|----------------|-------------|------------|
| Pre-Mondain's Legacy | 0x3FFF | < 0xC000 |
| Stygian Abyss | 0x7FFF | == 0xC000 |
| High Seas (UOAHS) | 0xFFDC | >= 0x13FDC |

---

### 1.2 Artidx.mul Structure

Each entry is **12 bytes**:
```
struct ArtIdxEntry {
    int32 lookup;   // Byte offset into Art.mul (-1 = empty/removed)
    int32 length;   // Length of data in bytes (0 = empty)
    int32 extra;    // Always 0 for land/static tiles
}
```

If lookup == -1, the tile is undefined. The client renders blank space or falls back.

---

### 1.3 Land Tile Format (Terrain Tiles - indices 0x0000 to 0x3FFF)

**Bitmap size: 44×44 pixels**

BUT - only the diamond-shaped pixels are stored. The full 44×44 = 1,936 pixels is NOT stored. Only the diamond pixels are written sequentially.

**Diamond layout (from LoadLand in Art.cs):**

```
Top half (rows 0-21): expanding diamond
  Row 0:  xOffset=21, xRun=2   (2 pixels at center-top)
  Row 1:  xOffset=20, xRun=4
  Row 2:  xOffset=19, xRun=6
  ...
  Row 21: xOffset=0,  xRun=44  (44 pixels at widest)

Bottom half (rows 22-43): contracting diamond
  Row 22: xOffset=0,  xRun=44
  Row 23: xOffset=1,  xRun=42
  ...
  Row 43: xOffset=21, xRun=2   (2 pixels at bottom-tip)
```

**Total pixels stored:**
- Top half: 2+4+6+...+44 = 2×(1+2+3+...+22) = 2×253 = 506 pixels
- Bottom half: 44+42+...+2 = 506 pixels
- **Total: 1,012 pixels × 2 bytes = 2,024 bytes per land tile**

**Color format: 16-bit ARGB1555**
```
Bit 15:    Alpha (1 = opaque, 0 = transparent)
Bits 10-14: Red (0-31, 5 bits)
Bits 5-9:   Green (0-31, 5 bits)
Bits 0-4:   Blue (0-31, 5 bits)
```

**File encoding:** Each pixel value is XOR'd with 0x8000 before writing:
```csharp
// Writing to file:
binmul.Write((ushort)(pixelValue ^ 0x8000));

// Reading from file:
*cur++ = (ushort)(*bdata++ | 0x8000);  // OR is equivalent to XOR here since bit was flipped
```

This means black (0x0000) becomes 0x8000 in the file. The alpha bit is stored inverted.

**Pixel data storage order:** Row by row, left-to-right within each row, only the visible diamond pixels. NOT stored as a rectangular image.

**What tools write:** UOFiddler reads a standard Bitmap (44×44, Format16bppArgb1555) and handles the diamond extraction automatically.

---

### 1.4 Static Tile Format (Statics - indices 0x4000 to 0x13FFF)

**Variable size, RLE compressed.**

**Binary layout:**
```
uint16 header_word_0;   // Ignored (often 1234 in UOFiddler-written files)
uint16 header_word_1;   // Ignored
uint16 width;           // Image width in pixels
uint16 height;          // Image height in pixels
uint16 lookup[height];  // Per-row: offset from (base + height + 4) to row data, in uint16 units
// Then row data:
for each row:
    repeat:
        uint16 xOffset;  // Horizontal skip (transparent pixels)
        uint16 xRun;     // Number of opaque pixels that follow
        if (xOffset == 0 && xRun == 0): end of row
        uint16 pixels[xRun];  // Each pixel in ARGB1555 ^ 0x8000
    until (0, 0) terminator
```

**Key differences from land tiles:**
- Variable dimensions (can be any size)
- RLE (Run-Length Encoded) - only non-transparent pixels stored
- Has a lookup table for random-access to rows
- Supports true transparency (pixels with value 0 are transparent)

**Pixel format:** Same ARGB1555 XOR 0x8000.

**Transparency:** Pixels with value == 0 (after XOR, stored as 0x0000) are transparent. When creating art for static tiles, pixels with alpha=0 become invisible in-game.

---

### 1.5 Textures.mul (for Land Tile Blending)

There is a **second art file for terrain** called Textures.mul (indexed by Texidx.mul).

- Land tile entries in TileData have a `TextureId` field
- This TextureId points to a 64×64 texture in Textures.mul
- The client uses these 64×64 textures for **smooth terrain blending** between adjacent tiles
- Without a texture map, terrain tiles show hard edges at boundaries
- Textures.mul entries are 64×64 = 4,096 pixels × 2 bytes = 8,192 bytes each (raw ARGB1555, no compression)

**Important:** For truly custom terrain, you need BOTH:
1. The 44×44 land tile art in Art.mul (what the tile looks like when flat)
2. The 64×64 texture in Textures.mul (used for smooth blending at tile edges)

If you don't provide a Textures.mul entry, terrain edges will look blocky/hard.

---

### 1.6 Map Files (map0.mul, map1.mul, etc.)

The map file stores the terrain grid. Each cell = **3 bytes**:
```
struct MapCell {
    uint16 tileId;   // Land tile ID (0x0000-0x3FFF)
    int8   altitude; // Z coordinate (-127 to 127, signed)
}
```

Map dimensions (standard):
| Map | File | Width | Height | Cells |
|-----|------|-------|--------|-------|
| Felucca/Trammel | map0.mul/map1.mul | 7168 | 4096 | 29,360,128 |
| Ilshenar | map2.mul | 2304 | 1600 | 3,686,400 |
| Malas | map3.mul | 2560 | 2048 | 5,242,880 |
| Tokuno | map4.mul | 1448 | 1448 | 2,096,704 |
| TerMur | map5.mul | 1280 | 4096 | 5,242,880 |

Map files are stored as raw blocks. Each block = 8×8 = 64 cells plus a 4-byte header:
```
struct MapBlock {
    uint32 header;        // CRC or ignored (old: always 0)
    MapCell cells[8][8];  // 64 cells, 3 bytes each = 192 bytes
}
// Total block size: 196 bytes
```

---

### 1.7 TileData.mul Structure

Controls flags and properties for every tile. Two sections: land tiles and item (static) tiles.

**Old format (pre-High Seas):**
- Land section: 512 groups × (4-byte group marker + 32 tiles × 26 bytes) = 428,032 bytes
  - Each land entry: 4-byte flags + 2-byte TextureId + 20-byte name
- Item section: many groups × (4-byte group marker + 32 tiles × 37 bytes)
  - Each item entry: 4-byte flags + various fields + 20-byte name

**New format (High Seas+, NewLandTileDataMul):**
- Flags expanded to 8 bytes (ulong/uint64)
- Otherwise same structure

**Critical land tile flags:**

| Flag | Value | Meaning |
|------|-------|---------|
| Wet | 0x80 | Tile is water (creatures with CantWalk can traverse) |
| Impassable | 0x40 | Cannot walk on |
| Surface | 0x200 | Can be walked on (most terrain) |
| Background | 0x01 | Renders behind other objects |

**For custom terrain tiles, set:**
- Walkable land: `Background | Surface` (Flags = 0x201)
- Water: `Background | Wet | Impassable` (Flags = 0xC1)
- Impassable rock: `Background | Impassable` (Flags = 0x41)

---

### 1.8 Statics Files (statics0.mul, stadif0.mul, etc.)

Static objects (trees, rocks, decorations, buildings) are placed in separate statics files.

- `statics0.mul` - static objects on Felucca
- `staidx0.mul` - index for statics0.mul
- Format: each entry = 7 bytes (x: uint16, y: uint16, z: int8, tileId: uint16)

---

## 2. Complete Workflow

### Step 1: Design Your Tile Set on Paper

Before touching any files, plan:
- List every terrain type you need (ocean, beach, grass, forest, mountain, snow, etc.)
- Decide which are TRUE TERRAIN (land tiles in map.mul) vs DECORATIVE (static tiles placed on top)
- Note: Land tiles are flat isometric diamonds. They DEFORM with altitude. If a land tile spans two altitudes, it stretches/warps. Complex art deforms badly.
- Simple solid-color or noise-based art works best for land tiles.

---

### Step 2: Draw Your Tiles

**Required art:**

**A. Land tile (44×44 art file):**
- Canvas: 44×44 pixels exactly
- Color mode: RGB, 16-bit compatible (save as 24-bit or 32-bit PNG, UOFiddler converts)
- Draw ONLY within the diamond area. The corners will be ignored/trimmed.
- Diamond area: starts 21px from left at top, expands 1px each side per row down to center, then contracts back.
- Template: Draw a diamond guide by plotting the exact pixel boundary from the Art.cs coordinates above.
- **No transparency in land tiles** - every diamond pixel must be fully opaque (alpha = 255). Transparent land pixels appear as black.
- Style: Clean, reads well at the isometric angle. Avoid fine detail (tiles are small in-game).

**B. Texture map (64×64 for Textures.mul):**
- Canvas: 64×64 pixels
- Must be rectangular/square (no alpha/transparency)
- This is a seamless/repeating version of the terrain color
- Used for smooth blending at tile boundaries
- Even a solid color works if you don't need blending

**Recommended art tools:**
| Tool | Why | Format to save |
|------|-----|----------------|
| Aseprite | Best for pixel art, handles tiny canvas well | Export as PNG |
| Photoshop | Full control, custom swatches | Export as PNG |
| GIMP | Free, can work with indexed color for heightmaps | Export as PNG |
| Krita | Good free alternative | Export as PNG |

**Color palette notes:**
- UO renders in 16-bit color. Don't use subtle gradients - they'll band heavily.
- Limit yourself to the colors actually representable in RGB555 (each channel 0-31 × 8 = 8-step increments of 8)
- If you're matching existing tile palettes, use UOFiddler to sample colors from existing tiles

**Diamond template for drawing (pixel-exact):**
```
Row 0:  cols 21-22     (2px wide)
Row 1:  cols 20-23     (4px wide)
Row 2:  cols 19-24     (6px wide)
...
Row 21: cols 0-43      (44px wide)
Row 22: cols 0-43      (44px wide)
Row 23: cols 1-42      (42px wide)
...
Row 43: cols 21-22     (2px wide)
```

---

### Step 3: Import Land Tile Art into Art.mul (via UOFiddler)

1. Launch **UOFiddler**
2. Configure paths: Tools > Settings > Set your UO client directory
3. Navigate to **"Tiles" tab** (shows land tiles) OR **"Art" tab** (shows statics)
4. For land tiles, use the **"Tiles" tab**:
   - Find the slot you want to replace or add to
   - Right-click an empty or existing slot → **"Replace"** or **"Import"**
   - Select your 44×44 PNG
   - UOFiddler auto-converts from standard PNG to the internal format
5. To ADD a new tile (not replace existing):
   - Find the first empty slot after all existing tiles
   - Right-click → "Replace" (even empty slots can be replaced)
   - Or use File > Add Land Tile
6. **CRITICAL: Note the tile ID number** - you'll need it for TileData and map editing

**UOFiddler file format support for import:**
- PNG (recommended - handles transparency correctly)
- BMP
- TGA
- Must be 44×44 for land tiles (tool may not enforce this - wrong size will corrupt)

**Saving:**
- File > Save (saves to current client directory)
- UOFiddler saves BOTH artidx.mul and art.mul simultaneously
- Always back up originals before saving

---

### Step 4: Set Up TileData Flags (via UOFiddler)

1. In UOFiddler, go to the **"TileData" tab**
2. Find your new tile ID (land tiles are in the left/land section)
3. Set properties:
   - **Name**: e.g., "custom_grass", "deep_ocean", "beach_sand"
   - **TextureId**: ID of your Textures.mul entry (set to same number or 0 if no texture)
   - **Flags**: Check the boxes for Background, Wet (water), Impassable, Surface, etc.

**Standard flag sets by terrain type:**

| Terrain | Required Flags | Hex |
|---------|----------------|-----|
| Walkable grass/dirt | Background + Surface | 0x00000201 |
| Ocean/deep water | Background + Wet + Impassable | 0x000000C1 |
| Shallow water | Background + Wet | 0x00000081 |
| Beach (walkable) | Background + Surface | 0x00000201 |
| Impassable mountain | Background + Impassable | 0x00000041 |
| Snow (walkable) | Background + Surface | 0x00000201 |
| Forest floor | Background + Surface | 0x00000201 |
| Dungeon floor | Background + Surface | 0x00000201 |

4. Save TileData changes (they save to tiledata.mul)

---

### Step 5: Add Texture to Textures.mul (via UOFiddler)

1. In UOFiddler, go to the **"Texture" tab** (or similar - "Land Textures")
2. Import your 64×64 texture image at the same ID as your land tile
3. This enables smooth blending between your tile and adjacent tiles
4. Save

**If you skip this step:** The terrain will still appear, but transitions between different terrain types will show hard diamond edges instead of smooth blends.

---

### Step 6: Edit the Map (Place Your Tiles)

**Option A: CentrED# (Recommended for large-scale editing)**

CentrED# is a client/server map editor.

1. Download from: https://kaczy93.github.io/centredsharp/#/Download/
2. Set up CentrED# Server:
   - Configure to point at your UO client data directory
   - Run the server (TCP port, default 2597)
3. Connect CentrED# Client to the server
4. Select your custom tile from the tile palette
5. Paint tiles onto the map
6. The client sends changes to the server which writes to map.mul in real time

**CentrED# key features:**
- Real-time collaborative editing
- Shows height (altitude) information
- Full land tile and static tile editing
- Undo/redo
- Large area fill tools

**Option B: MapCreator v5.0 (For large-scale procedural/image-based map generation)**

By ghostbyte420 (ServUO community)

- **Input**: Two bitmap images:
  - `Terrain.bmp` - 8-bit indexed PNG, each palette color = one terrain type
  - `Altitude.bmp` - 8-bit grayscale, pixel brightness = Z height
  - Image dimensions: typically 5120×4096 for Felucca-size maps
- **Config**: `terrain.xml` maps palette color indices to TileIDs
- **Output**: Generates map.mul automatically

```xml
<!-- terrain.xml example structure -->
<terrain>
    <tile color="0,128,0" tileId="0x004B" altitude="0" />  <!-- grass = green -->
    <tile color="0,0,255" tileId="0x00A8" altitude="-5" /> <!-- water = blue -->
    <tile color="255,220,0" tileId="0x0080" altitude="0" /> <!-- beach = yellow -->
</terrain>
```

**For custom tiles:** Add your new tile IDs to terrain.xml with corresponding colors. Then paint terrain.bmp in Photoshop with those specific palette colors.

**Option C: UOArchitect**
- GUI-based map editor
- Less widely used than CentrED# for terrain
- Better for structured/room-based content
- Look for download on ServUO forums

**Option D: Ultima Live (real-time in-game)**
- Allows live map editing while server is running
- Requires Ultima Live system on server and client
- ServUO has Ultima Live scripts available
- Players with GM access can edit map live

---

### Step 7: Server-Side Configuration

For ServUO / RunUO, the server reads client files directly. You need to:

**1. Copy modified client files to server:**
- If your server and client are separate directories, copy:
  - `Art.mul` + `Artidx.mul` (or `artLegacyMUL.uop`)
  - `Tiledata.mul`
  - `Textures.mul` + `Texidx.mul`
  - `map0.mul` (or whichever map you edited)
  - `statics0.mul` + `staidx0.mul` (if you placed statics)

**2. Server data path config (ServUO):**
```csharp
// In Scripts/Misc/DataPath.cs or server.cfg:
DataPath = "C:\\Path\\To\\UO\\Client";
```

**3. Custom map definition (if adding a new map beyond the 6 defaults):**
```csharp
// In Scripts/Misc/ServerList.cs or custom script:
Map myMap = new Map("MyMap", 6, 6, 5120, 4096, 4, MapRules.FeluccaRules);
Map.Maps[6] = myMap;
```

**4. Teleport players to new map for testing:**
```
[Admin command in-game]:
[go 1000 1000 0 MyMap
```

**5. No recompilation needed** unless you're adding a new Map object in code.

---

### Step 8: Client-Side Distribution

When you distribute your shard to players:

**Option A: Custom client patch:**
- Players replace their Art.mul, Artidx.mul, Tiledata.mul, etc.
- Ship modified client files (legal grey area with EA - only distribute your CUSTOM art, not modified EA art)

**Option B: UOP patch system:**
- Modern UO clients support .uop files
- artLegacyMUL.uop replaces art.mul + artidx.mul
- Tools like OrionUOP or UOP packing scripts can create these

**Option C: Separate client install:**
- Provide your custom client as a separate install
- All modified files pre-bundled

---

## 3. Tools Reference

### 3.1 UOFiddler

**What it is:** Primary UO art editor. The essential tool for editing Art.mul, TileData.mul, Textures.mul, Animations, Hues, Sound, and more.

**Download:** https://github.com/polserver/UOFiddler/releases  
**Website:** https://uofiddler.polserver.com/  
**Language:** C# (.NET)

**What it can do:**
- Import/export land tile art (44×44 PNG/BMP/TGA → Art.mul)
- Import/export static art (variable size PNG → Art.mul)
- Edit TileData flags and properties
- Import/export Textures.mul (64×64 terrain textures)
- View/export Animations
- Edit Hues
- Export tiles as images for reference

**Supported import formats:** PNG, BMP, TGA

**Key workflows:**
1. **Tiles tab** = Land tiles (terrain). Right-click → Replace.
2. **Art tab** = Static tiles (items, buildings, etc.). Right-click → Replace.
3. **TileData tab** = Edit flags for any tile.
4. **Texture tab** = 64×64 terrain blending textures.

**Limitations:**
- Windows only (.NET WinForms)
- No command-line interface for batch operations
- One tile at a time for custom imports (use BULKUO for batch)

---

### 3.2 CentrED# (CentrED Sharp)

**What it is:** The primary UO map editor. Client/server architecture for terrain and static placement.

**GitHub:** https://github.com/kaczy93/centredsharp  
**Download:** https://kaczy93.github.io/centredsharp/#/Download/  
**Discord:** https://discord.gg/zpNCv36fQ8  
**Language:** C# (.NET 10)  
**License:** Open source  

**What it can do:**
- Visual map editing (land tiles and statics)
- Real-time editing (changes go to map files immediately)
- Multi-user collaborative editing
- Height (altitude) editing
- Large area fill/paint tools
- Custom tile palettes (shows your custom tiles if client files are set up)

**Server setup:**
1. Run CentrED# Server, point it at your client data directory
2. Configure port (default 2597)
3. Connect CentrED# Client

**Important for custom tiles:** CentrED# reads tile art directly from Art.mul. If you've imported custom tiles into Art.mul, they will appear in CentrED# automatically. No extra configuration.

**Original CentrED:** https://git.aksdb.de/aksdb/CentrED (C++ version, older, still works but less maintained)

---

### 3.3 BULKUO

**What it is:** Command-line batch art importer/exporter for UO files. The tool for bulk operations that UOFiddler can't do efficiently.

**Forum post:** On ServUO (search "BULKUO" in the Archive tutorials by ParanoiaPhD, Sep 2023)

**What it can do:**
- Batch import many tiles at once from a folder of images
- Batch export all tiles to images
- Works with Art.mul, Textures.mul
- Command-line interface, scriptable

**Key use case for custom tilesets:**
- You have 50 custom terrain tiles → batch import all at once
- Export all existing tiles to PNG for reference
- Automate the import step in your build pipeline

**Usage pattern:**
```
# Example (exact syntax may vary by version):
bulkuo import-land --mul art.mul --idx artidx.mul --source ./my_tiles/land/ --start-id 0x1000
bulkuo export-land --mul art.mul --idx artidx.mul --dest ./exported_tiles/
```

---

### 3.4 MapCreator v5.0

**What it is:** Image-to-map compiler. Takes painted bitmaps and generates map.mul.

**Author:** ghostbyte420 (ServUO)  
**Forum:** https://www.servuo.dev/archive/mapcreator.2524/

**How it works:**
1. You paint a `Terrain.bmp` image using an 8-bit color palette
2. Each color in the palette = a specific terrain tile ID (defined in terrain.xml)
3. You paint an `Altitude.bmp` grayscale image (brightness = terrain height)
4. MapCreator converts these images to the binary map.mul format

**Image specs:**
- Size: Matches your map dimensions (e.g., 5120×4096 for full Felucca)
- Format: PNG-8 (8-bit indexed), or standard BMP
- Terrain.bmp: Flat color, each pixel = terrain type
- Altitude.bmp: Grayscale, pixel brightness maps to Z value (typically 0=sea level, white=mountain)

**Workflow with custom tiles:**
```xml
<!-- terrain.xml - add your custom tile IDs -->
<terrain>
    <!-- Built-in UO tiles -->
    <tile colorIndex="1" tileId="0x0003" />  <!-- deep water -->
    <tile colorIndex="2" tileId="0x004B" />  <!-- grass -->
    
    <!-- YOUR custom tiles -->
    <tile colorIndex="10" tileId="0x1000" />  <!-- custom ocean -->
    <tile colorIndex="11" tileId="0x1001" />  <!-- custom beach -->
    <tile colorIndex="12" tileId="0x1002" />  <!-- custom forest -->
</terrain>
```

---

### 3.5 UOArchitect

**What it is:** Map and region builder. More structured than CentrED+, used for creating specific locations/buildings.

**Status:** Available on various UO download sites. Search "UOArchitect download" or check ServUO resources section.

**What it can do:**
- Visual map editing
- Multi-tile templates (place entire rooms at once)
- Region definition
- Static placement

**Less commonly used** for terrain editing - most freeshards use CentrED# for terrain, UOArchitect for buildings.

---

### 3.6 Pandora's Box

**What it is:** Older UO world editor. Primarily for older RunUO/older versions.

**Status:** Available on UOSA, RunUO archive, and other UO tool sites.

**What it can do:**
- Map editing (older interface than CentrED)
- Static placement
- Area editing

**Recommendation:** Use CentrED# instead. Pandora's Box is largely superseded.

---

### 3.7 Tile Object Placer (TOP)

**What it is:** Tool mentioned in Vrark's reverse engineering tutorials. Used for placing tiles with precise control.

**Referenced in:** ServUO Art tutorials (Vrark's content)

**Usage:** Primarily for static tile placement workflows when you need precise placement control beyond what CentrED provides.

---

### 3.8 Ultima Live

**What it is:** System for editing UO maps in real-time while the server is running.

**GitHub:** https://github.com/UltimaLive/UltimaLive  
**What it does:**
- Live map editing without server restart
- Stream map changes to connected clients in real time
- Requires special client modification and server scripts

**Use case:** Large server teams doing iterative world building without constant restarts.

---

### 3.9 UO Landscaper / PursonalPhD's Smooth Maps

**What it is:** A workflow/toolset for creating high-quality smooth terrain maps for UO.

**From ServUO (PursonalPhD):** https://www.servuo.dev/archive/new-uol-smooth-maps.2154/

**What it includes:**
- Ready-to-render dev maps (pre-made test terrains)
- A script that teleports to 85+ different texture types instantly for testing
- Hand-made color palette with terrain colors as .aco (Photoshop swatch) file
- Custom smooth map modification techniques
- Tips for heightmap creation

**Key technique:**
1. Use Adobe Photoshop (or Elements)
2. Start in RGB mode for painting
3. Convert to Indexed Color (8-bit) for the palette-based terrain map
4. Use solid brush (NO anti-aliasing) for clean color boundaries
5. Each palette color maps to a tile ID
6. Convert altitude map separately as grayscale
7. Export both to MapCreator

**Critical tip from PursonalPhD:**
- Avoid anti-aliasing / soft brushes when painting terrain boundaries
- Gradient blending between colors creates mixed-palette pixels that MapCreator can't map to a tile ID
- Always use hard edges - the game engine handles the visual blending via Textures.mul

---

### 3.10 art2mul

**Status:** Not found as a standalone named tool. The function of converting art to .mul format is handled by UOFiddler and BULKUO. The name may refer to internal functions within these tools or a very old/obscure utility not in active use. If you encounter references to "art2mul," it likely means UOFiddler's import function or BULKUO.

---

## 4. Base UO Tile IDs

These are the standard terrain tile IDs in the original Ultima Online client files. Use UOFiddler's Tiles tab to browse these visually.

**IMPORTANT NOTE:** The best way to get exact tile IDs is to open UOFiddler, navigate to the Tiles tab, and browse visually. The IDs below are ranges based on community documentation and common knowledge from UO development - verify with UOFiddler in your specific client version.

### 4.1 Water / Ocean

| ID Range | Description |
|----------|-------------|
| 0x00A8 - 0x00AB | Deep water (4 animated frames) |
| 0x00AC | Deep water variant |
| 0x0136 - 0x013E | More water variants |
| 0x0001 - 0x0009 | Animated water tiles (some variants) |

**Key for water:** TileData flags must include `Wet` (0x80) and `Impassable` (0x40).

### 4.2 Beach / Sand

| ID Range | Description |
|----------|-------------|
| 0x0080 - 0x008F | Sand / beach variations |
| 0x0090 - 0x009F | More sand |
| 0x00AB - 0x00B0 | Sand near water edge |

### 4.3 Grass

| ID Range | Description |
|----------|-------------|
| 0x004B - 0x0058 | Green grass (main grass tiles) |
| 0x003C - 0x004A | Grass variations |
| 0x0059 - 0x0068 | More grass / light variations |

### 4.4 Dirt / Path

| ID Range | Description |
|----------|-------------|
| 0x0071 - 0x0080 | Dirt / bare earth |
| 0x0021 - 0x002A | Stone path / road |

### 4.5 Forest Floor

| ID Range | Description |
|----------|-------------|
| 0x0164 - 0x016F | Forest floor / dark ground |
| Trees are **statics**, not land tiles | Static tile IDs 0x0CE3+ (various tree types) |

### 4.6 Mountain / Rock

| ID Range | Description |
|----------|-------------|
| 0x01A8 - 0x01C0 | Mountain rock face |
| 0x01C0 - 0x01CF | More mountain |
| 0x025A - 0x027A | Rocky terrain |

**Note:** Mountain faces are mostly statics (impassable static tiles placed on map), not land tiles. The land underneath mountains is often just dirt with altitude > 0.

### 4.7 Snow

| ID Range | Description |
|----------|-------------|
| 0x011A - 0x011F | Snow covered ground |
| 0x0120 - 0x012F | More snow |

### 4.8 Dungeon / Cave

| ID Range | Description |
|----------|-------------|
| 0x01AC - 0x01C0 | Cave / dungeon floor |
| 0x019A - 0x01AC | Dark dungeon ground |

**Dungeon walls are STATICS, not land tiles.**

### 4.9 Swamp / Wet Ground

| ID Range | Description |
|----------|-------------|
| 0x00B0 - 0x00C4 | Swamp-like terrain |

### 4.10 Finding the Right IDs - Best Method

1. Open UOFiddler → Tiles tab
2. Browse visually, tiles are shown as previews
3. Click any tile to see its ID
4. Sort by ID, browse ranges
5. Note: IDs displayed in UOFiddler are decimal or hex - confirm format matches what CentrED uses

---

## 5. Outlands / Advanced Custom Tilesets

### 5.1 UO Outlands Approach

UO Outlands (https://uooutlands.com) has the most extensive custom tile library of any UO freeshard. Their world uses thousands of custom terrain and static tiles.

**What is publicly known:**
- Custom tiles are visible when playing - distinct visual style vs standard UO
- Players who have examined their client files report large numbers of custom static tiles
- Terrain still uses the standard UO land tile diamond format
- Heavy use of custom static overlays (placed on top of terrain) to achieve unique looks
- Their Art.mul is much larger than vanilla UO

**GitHub org:** https://github.com/uooutlands  
- Public repos: Forks of ClassicUO, Razor, FNA
- **No public tile art tools or packs**
- No documentation on their custom tile pipeline

**Community analysis of their approach:**
- Use high-quality isometric pixel art created professionally
- Tiles drawn to match UO's perspective and lighting direction
- Heavy static tile usage for vegetation, rocks, structures
- Some terrain tile replacements for biome-specific looks
- Client modifications distributed as a custom installer

**Their apparent pipeline (inferred):**
1. Commission or in-house pixel art in correct UO isometric style
2. Import via UOFiddler or BULKUO in batch
3. Register in TileData
4. Map built with CentrED-equivalent tools
5. Distribute as their custom client installer

### 5.2 How to Achieve Outlands-Quality Custom Tiles

**The secret is mostly art quality, not tool sophistication.**

1. **Professional isometric pixel art** - Hire an artist who understands the UO perspective
2. **Consistent lighting** - UO's light source is from the northwest (upper-left). All custom tiles should match this
3. **Match scale** - Study existing UO tiles to understand scale. Players and trees have specific pixel heights.
4. **Static layering** - The best custom biomes use terrain + multiple layers of static tiles (ground cover, vegetation, rocks) for depth
5. **Texture diversity** - Multiple variants of the same terrain type (5-8 grass variants) for natural look
6. **Transition tiles** - Create transition tiles for every pair of terrain types that will be adjacent (grass-beach, grass-forest, etc.)

### 5.3 UO Outlands Custom Map Size

Their custom world "Outlands" is a single large map. Approximate dimensions suggest it's smaller than Felucca but with much denser content. The exact specs are not publicly documented.

---

## 6. Libraries

### 6.1 C# Libraries

#### UOFiddler / Ultima SDK (Best option)
**GitHub:** https://github.com/polserver/UOFiddler  
**Namespace:** `Ultima`  
**NuGet:** Search "Ultima" or reference the UOFiddler solution

**Key classes:**
```csharp
using Ultima;

// Read a land tile as Bitmap
Bitmap landTile = Art.GetLand(0x004B);

// Read a static tile as Bitmap
Bitmap staticTile = Art.GetStatic(0x0CEB);

// Replace a land tile
Art.ReplaceLand(0x004B, myBitmap);

// Replace a static tile
Art.ReplaceStatic(0x0CEB, myBitmap);

// Save changes
Art.Save("C:\\output\\path\\");

// Read TileData
LandData landInfo = TileData.LandTable[0x004B];
string name = landInfo.Name;
TileFlag flags = landInfo.Flags;
ushort texId = landInfo.TextureId;

// Check tile flags
bool isWet = (landInfo.Flags & TileFlag.Wet) != 0;
bool isSurface = (landInfo.Flags & TileFlag.Surface) != 0;

// Configure file paths
Files.SetMulPath("C:\\UO\\Client\\");
// or
Files.SetMulPath("artidx.mul", "C:\\custom\\artidx.mul");
Files.SetMulPath("art.mul", "C:\\custom\\art.mul");
```

**Files.cs - Setting up paths:**
```csharp
// Point to client directory
Files.RootDir = "C:\\Ultima Online\\";
// Or set individual files
Files.MulPath["Art.mul"] = "C:\\UO\\Art.mul";
```

#### ClassicUO Asset Library
**GitHub:** https://github.com/ClassicUO/ClassicUO  
**Namespace:** `ClassicUO.Assets`  
**Note:** Integrated into ClassicUO; can extract the Assets project separately  

```csharp
// ClassicUO ArtLoader approach
// References their ArtLoader.cs for reading art files
```

#### ModernUO
**GitHub:** https://github.com/modernuo/ModernUO  
**Purpose:** Server-side; contains TileMatrix and map reading code  
**Less useful for art editing, more for server map access**

---

### 6.2 Python Libraries

**Situation as of 2026:** No well-maintained, widely-used Python library specifically for UO art files exists on PyPI.

**However, you can build one from the format specs.** Here's a complete Python implementation based on the Art.cs source:

```python
"""
uo_art.py - Read/write UO Art.mul and Artidx.mul in Python
Based on Art.cs from UOFiddler (polserver/UOFiddler)
"""

import struct
from PIL import Image
import numpy as np

# ARGB1555 to RGBA conversion
def argb1555_to_rgba(pixel):
    """Convert 16-bit ARGB1555 to (R, G, B, A) tuple (8-bit each)"""
    alpha = ((pixel >> 15) & 0x1) * 255
    red   = ((pixel >> 10) & 0x1F) << 3
    green = ((pixel >> 5)  & 0x1F) << 3
    blue  = ((pixel >> 0)  & 0x1F) << 3
    return (red, green, blue, alpha)

def rgba_to_argb1555(r, g, b, a=255):
    """Convert RGBA (8-bit) to 16-bit ARGB1555"""
    alpha = 1 if a > 127 else 0
    red   = (r >> 3) & 0x1F
    green = (g >> 3) & 0x1F
    blue  = (b >> 3) & 0x1F
    return (alpha << 15) | (red << 10) | (green << 5) | blue


def read_idx(idx_path):
    """Read artidx.mul, return list of (lookup, length, extra) tuples"""
    entries = []
    with open(idx_path, 'rb') as f:
        data = f.read()
    count = len(data) // 12
    for i in range(count):
        offset = i * 12
        lookup, length, extra = struct.unpack_from('<iii', data, offset)
        entries.append((lookup, length, extra))
    return entries


def read_land_tile(mul_data, lookup, length):
    """
    Read a land tile from Art.mul.
    Returns a 44x44 RGBA PIL Image, or None if empty.
    """
    if lookup < 0 or length <= 0:
        return None
    
    # Land tile: raw diamond pixels, no header
    # 1012 pixels = 2024 bytes
    pixels = struct.unpack_from(f'<{length // 2}H', mul_data, lookup)
    
    img = Image.new('RGBA', (44, 44), (0, 0, 0, 0))
    pix = img.load()
    
    pixel_idx = 0
    
    # Top half: rows 0-21, expanding
    x_offset = 21
    x_run = 2
    for row in range(22):
        for col in range(x_run):
            raw = pixels[pixel_idx] | 0x8000  # flip alpha bit back
            rgba = argb1555_to_rgba(raw)
            pix[x_offset + col, row] = rgba
            pixel_idx += 1
        x_offset -= 1
        x_run += 2
    
    # Bottom half: rows 22-43, contracting
    x_offset = 0
    x_run = 44
    for row in range(22, 44):
        for col in range(x_run):
            raw = pixels[pixel_idx] | 0x8000
            rgba = argb1555_to_rgba(raw)
            pix[x_offset + col, row] = rgba
            pixel_idx += 1
        x_offset += 1
        x_run -= 2
    
    return img


def read_static_tile(mul_data, lookup, length):
    """
    Read a static tile from Art.mul.
    Returns a PIL Image (RGBA), or None if empty.
    """
    if lookup < 0 or length <= 0:
        return None
    
    # Parse header
    pos = lookup
    # Skip 4 bytes header
    pos += 4
    
    width, height = struct.unpack_from('<HH', mul_data, pos)
    pos += 4
    
    if width <= 0 or height <= 0:
        return None
    
    # Read lookup table
    base = height + 4  # offset from start of entry (in ushort units)
    lookups = struct.unpack_from(f'<{height}H', mul_data, pos)
    pos += height * 2
    
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pix = img.load()
    
    data_start = lookup + (base * 2)  # in bytes from start of mul_data
    
    for y in range(height):
        row_pos = data_start + lookups[y] * 2
        x = 0
        while True:
            x_offset, x_run = struct.unpack_from('<HH', mul_data, row_pos)
            row_pos += 4
            if x_offset == 0 and x_run == 0:
                break
            x += x_offset
            for i in range(x_run):
                raw = struct.unpack_from('<H', mul_data, row_pos)[0]
                row_pos += 2
                raw = raw ^ 0x8000  # flip alpha
                rgba = argb1555_to_rgba(raw)
                if 0 <= x + i < width:
                    pix[x + i, y] = rgba
            x += x_run
    
    return img


class UOArt:
    """High-level interface for reading UO art files."""
    
    def __init__(self, mul_path, idx_path):
        with open(mul_path, 'rb') as f:
            self.mul_data = f.read()
        self.idx = read_idx(idx_path)
    
    def get_land(self, tile_id):
        """Get land tile (0x0000-0x3FFF) as PIL Image."""
        if tile_id < 0 or tile_id >= 0x4000:
            return None
        lookup, length, _ = self.idx[tile_id]
        return read_land_tile(self.mul_data, lookup, length)
    
    def get_static(self, tile_id):
        """Get static tile as PIL Image. tile_id is 0-based item ID."""
        idx = tile_id + 0x4000
        if idx >= len(self.idx):
            return None
        lookup, length, _ = self.idx[idx]
        return read_static_tile(self.mul_data, lookup, length)
    
    def export_all_land(self, output_dir):
        """Export all land tiles to PNG files."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        for i in range(0x4000):
            img = self.get_land(i)
            if img:
                img.save(os.path.join(output_dir, f'land_{i:04X}.png'))


# Usage example:
# art = UOArt('Art.mul', 'Artidx.mul')
# img = art.get_land(0x004B)  # Get grass tile
# img.save('grass.png')
# static = art.get_static(0x0CEB)  # Get a tree
# static.save('tree.png')
```

**Dependencies:** `Pillow` (pip install Pillow), `numpy`

#### Writing back to Art.mul (Python):

```python
def write_land_tile(img_rgba, output_stream):
    """
    Write a 44x44 RGBA PIL Image as a land tile to output_stream.
    Returns bytes written.
    """
    assert img_rgba.size == (44, 44), "Land tiles must be 44x44"
    pix = img_rgba.load()
    data = bytearray()
    
    # Top half (rows 0-21)
    x_offset = 21
    x_run = 2
    for row in range(22):
        for col in range(x_run):
            r, g, b, a = pix[x_offset + col, row]
            raw = rgba_to_argb1555(r, g, b, a)
            raw ^= 0x8000  # flip alpha for file storage
            data += struct.pack('<H', raw)
        x_offset -= 1
        x_run += 2
    
    # Bottom half (rows 22-43)
    x_offset = 0
    x_run = 44
    for row in range(22, 44):
        for col in range(x_run):
            r, g, b, a = pix[x_offset + col, row]
            raw = rgba_to_argb1555(r, g, b, a)
            raw ^= 0x8000
            data += struct.pack('<H', raw)
        x_offset += 1
        x_run -= 2
    
    output_stream.write(data)
    return len(data)
```

---

### 6.3 MapCreator Python Script (from ServUO - PursonalPhD)

The Python dungeon generator mentioned in ServUO tutorials uses a different approach:

```python
# Dungeon generation pattern (from ServUO tutorial by PursonalPhD):
# - Uses a grid-based approach
# - Generates room-based dungeon layouts
# - Writes to map via UO file format or via CentrED scripting
# - Teleport command script included for rapid testing of 85+ textures

# The teleport script pattern:
def teleport_to_texture(player, texture_id):
    # Maps texture IDs to map coordinates where they are placed
    # Allows GMs to quickly review all terrain types in-game
    pass
```

---

## 7. Gaps / Unanswered Questions

### 7.1 BULKUO Exact Syntax

- **Gap:** Could not confirm exact command-line syntax for BULKUO
- **Resolution:** Download from ServUO tutorials, check included README
- **Workaround:** UOFiddler's UI handles individual tiles; for batch, write a C# script using the Ultima SDK

### 7.2 Exact Base UO Tile IDs

- **Gap:** Tile IDs vary slightly between UO client versions (T2A, UOR, SE, ML, SA, HS)
- **Resolution:** Use UOFiddler with YOUR specific client version to browse tiles visually and record IDs
- **Best reference:** Export TileData from UOFiddler as CSV, sort by name

### 7.3 Tile Transition Art

- **Gap:** How does UO blend between different terrain types visually?
- **Answer (from research):** Two mechanisms:
  1. **Textures.mul** - 64×64 texture per land tile ID, used by the engine for smooth blending
  2. **The client engine** blends textures at boundaries automatically based on which tiles are adjacent
- **For custom tiles:** You need a Textures.mul entry for every custom land tile, or borders will look sharp

### 7.4 UOP Format (Modern Clients)

- **Gap:** Exact process for packing Art.mul into artLegacyMUL.uop
- **Known:** The .uop format is a HashPack container
- **Tools:** OrionUOP, or community UOP packing scripts
- **Recommendation for development:** Work with .mul files during development, convert to .uop for release

### 7.5 UO Outlands Custom Art Details

- **Gap:** No public documentation or tools from Outlands team
- **Resolution:** Not possible without insider access; reverse-engineer their client if needed

### 7.6 Animated Land Tiles

- **Gap:** How does water animation work in terrain tiles?
- **Known:** Water tiles use multiple land tile IDs (typically 4) that the client cycles through
- **Mechanism:** The client reads tile animation data from TileData (the Animation field in ItemData, and Animated flag)
- **For land tiles:** Water animation may be hardcoded to specific tile ID ranges or controlled via separate anim data
- **Resolution needed:** Needs testing - try replacing the existing animated water tiles (0x00A8-0x00AB) first

### 7.7 Classic vs Enhanced Client Differences

- **Gap:** Enhanced client may handle tiles differently
- **Recommendation:** Target the Classic client (ClassicUO or razor-compatible) for custom tile work - better documented and supported in the shard community

### 7.8 Textures.mul Exact Requirements

- **Gap:** Does every land tile REQUIRE a Textures.mul entry?
- **Known:** TextureId = 0 in TileData means "no texture" or "use default"
- **If TextureId = 0:** The tile still renders but may show hard edges at boundaries
- **Resolution:** Test with and without - tiles with TextureId=0 still appear but blending may look worse

### 7.9 Python UO Library on PyPI

- **Gap:** No maintained Python package on PyPI
- **Resolution:** Use the Python implementation in Section 6.2, or use the C# Ultima SDK via a .NET process

### 7.10 MapCreator v5.0 Source

- **Gap:** Couldn't locate public GitHub for MapCreator v5.0
- **Resolution:** Download from ServUO forum post by ghostbyte420

---

## Appendix A: Quick Reference - File Summary

| File | Purpose | Edit With |
|------|---------|-----------|
| Art.mul | All art (land + static tiles) | UOFiddler, BULKUO |
| Artidx.mul | Index into Art.mul | Written by UOFiddler automatically |
| artLegacyMUL.uop | Modern container for Art | UOP tools |
| Tiledata.mul | Tile flags/properties | UOFiddler TileData tab |
| map0.mul | Terrain grid (Felucca) | CentrED#, MapCreator |
| statics0.mul | Static objects (Felucca) | CentrED# |
| staidx0.mul | Index for statics0.mul | Written by CentrED# |
| Textures.mul | 64×64 terrain blend textures | UOFiddler Texture tab |
| Texidx.mul | Index for Textures.mul | Written by UOFiddler |

---

## Appendix B: Diamond Template (44×44 Grid)

```
Row  xMin  xMax  Width
 0    21    22    2
 1    20    23    4
 2    19    24    6
 3    18    25    8
 4    17    26    10
 5    16    27    12
 6    15    28    14
 7    14    29    16
 8    13    30    18
 9    12    31    20
10    11    32    22
11    10    33    24
12     9    34    26
13     8    35    28
14     7    36    30
15     6    37    32
16     5    38    34
17     4    39    36
18     3    40    38
19     2    41    40
20     1    42    42
21     0    43    44
22     0    43    44
23     1    42    42
24     2    41    40
25     3    40    38
26     4    39    36
27     5    38    34
28     6    37    32
29     7    36    30
30     8    35    28
31     9    34    26
32    10    33    24
33    11    32    22
34    12    31    20
35    13    30    18
36    14    29    16
37    15    28    14
38    16    27    12
39    17    26    10
40    18    25    8
41    19    24    6
42    20    23    4
43    21    22    2
```

Total opaque pixels: 1,012
Raw byte size in file: 2,024 bytes (1,012 × 2 bytes each)

---

## Appendix C: Priority Action List for Custom World Build

**Phase 1: Setup & Test (1 day)**
1. Install UOFiddler, point at your UO client
2. Install CentrED# server + client
3. Verify you can browse existing tiles in UOFiddler
4. Verify CentrED# connects and shows your map

**Phase 2: First Custom Tile (1-2 days)**
1. Design one land tile (e.g., custom grass) in Aseprite or Photoshop at 44×44
2. Import via UOFiddler → Tiles tab → replace an unused slot
3. Note the tile ID
4. Set TileData flags (Background + Surface)
5. Create 64×64 texture version → import to Textures.mul at same ID
6. In CentrED#, paint a small area with your tile
7. Start server, launch client, walk on it

**Phase 3: Full Biome Palette (1-2 weeks)**
1. Design all terrain types (ocean, beach, grass, forest, mountain, snow, dungeon)
2. Batch import via BULKUO or UOFiddler
3. Create transition tiles for each biome boundary
4. Set all TileData flags correctly

**Phase 4: Map Generation (1-2 days)**
1. Set up MapCreator v5.0
2. Configure terrain.xml with your tile IDs and colors
3. Paint terrain.bmp in Photoshop (one color per terrain type)
4. Paint altitude.bmp in Photoshop (grayscale for height)
5. Run MapCreator → generates map.mul
6. Load into CentrED# for fine-tuning

**Phase 5: Refinement (ongoing)**
1. Add statics (trees, rocks, vegetation) over terrain
2. Refine altitude work for mountains and coastlines
3. Add transition tiles and detail work
