# ServUO Art & Development Research
**Compiled:** 2026-03-09  
**Source:** ServUO.dev tutorials  
**Purpose:** Reference material for game development - UO emulation art pipeline, animations, maps, scripting

---

## Table of Contents
1. [Sprite/Art Creation](#sprite-art-creation)
2. [Animations - Character/Creature (Custom)](#animations---charactercreature-custom)
3. [Animations - Item Animations](#animations---item-animations)
4. [Animations - Extracting from FLC/GIF](#animations---extracting-from-flcgif)
5. [Map Tiles & Map Creation](#map-tiles--map-creation)
6. [Map Extraction - Yoinking Map Sections](#map-extraction---yoinking-map-sections)
7. [Custom Item Scripting](#custom-item-scripting)
8. [Tools & Workflow Reference](#tools--workflow-reference)
9. [File Formats Reference](#file-formats-reference)
10. [Config Files Reference](#config-files-reference)

---

## Source Tutorials Index

| # | Title | Author | Date | URL |
|---|-------|--------|------|-----|
| 1 | How to add custom animations to UO | Redmoon | Sep 24, 2021 | https://www.servuo.dev/archive/how-to-add-custom-animations-to-uo.1629/ |
| 2 | Adding Item Animations | Amadora | Nov 13, 2022 | https://www.servuo.dev/archive/adding-item-animations.1830/ |
| 3 | Custom Animations - extracting from a .flc/.gif | Redmoon | Sep 24, 2021 | https://www.servuo.dev/archive/custom-animations-extracting-from-a-flc-gif.1628/ |
| 4 | Map Tiling - Deep Dive! | Wilson | Aug 2, 2025 | https://www.servuo.dev/archive/map-tiling-deep-dive.2495/ |
| 5 | Video Tutorial - Reverse Engineering Art | otimpyre | Feb 5, 2014 | https://www.servuo.dev/archive/video-tutorial-reverse-engineering-art.91/ |
| 6 | Beginner's Guide to Creating a Basic Item Script | JBob | Feb 18, 2025 | https://www.servuo.dev/archive/beginners-guide-to-creating-a-basic-item-script.2422/ |
| 7 | How to *yoink* parts of a map | Redmoon | Sep 24, 2021 | https://www.servuo.dev/archive/how-to-yoink-parts-of-a-map.1636/ |

---

## Sprite/Art Creation

### Reverse Engineering Art (Video Tutorial)
- **Author:** otimpyre | **Date:** Feb 5, 2014 | **Rating:** 5/5 (2 reviews)
- This is a **video-only** tutorial with no text body captured.
- otimpyre is an active art resource creator with tools: Texture Pro 2.0, Auto Pavers Pro 4.0, Red Brick Deluxe, Light Stone Pavers Deluxe.
- The tutorial covers reverse-engineering UO art assets.
- **Related tools by same author:** Auto Pavers Pro 4.0 (creates tiling art sets), Texture Pro 2.0 (custom texture tool asset).

### BMP File Handling
- All UO art frames are extracted/worked with as `.bmp` files
- Background color replacement: use RGB `255,255,255` (white) OR `0,0,0` (black)
- Tolerance for color replacement: start at 30, adjust to preference
- Frame manipulation tools: Photoshop, Corel PhotoPaint, Jasc Animation Shop
- Horizontal flip: used to mirror left-side animations to create right-side (UO uses flip technique, right side not needed as unique frames)

### Art File Sizes
- For ridable creatures (sphynx, tiger class): resize to **400x400** pixels in Jasc Animation Shop
- Shrunk pet art: approximately **30x45px** BMP

---

## Animations - Character/Creature (Custom)

**Source:** Tutorial #1 - "How to add custom animations to UO" by Redmoon (Sep 24, 2021)

### Overview
Full pipeline for adding custom creature/character animations to UO. Covers low vs high creature types, frame organization, BMP-to-UOP conversion, UOP-to-VD, VD-to-MUL, and all config file edits.

### Step 1: File Organization

Organize extracted BMPs into a directory structure:

```
[AnimationName]/
  Walk/
    Down/          <- walkdown_1.bmp, walkdown_2.bmp, ...
    Down Left/     <- walkDL_1.bmp, ...
    Left/          <- walkleft_1.bmp, ...
    Up Left/       <- walkUL_1.bmp, ...
    Up/            <- walkup_1.bmp, ...
    Not Needed/    <- right-facing frames (not needed - UO mirrors left)
  Run/
    [same sub-folders]
  Idle/
    [same sub-folders]
  [etc for each animation type]
```

**Naming convention:** Rename BMPs to include animation type, direction, and sequence number  
Example: `walk32.bmp` -> `walkdown_1.bmp` (Windows auto-numbers with F2 rename + Ctrl+A)

**Direction order (UO standard):** Down, Down Left, Left, Up Left, Up  
(Right side is NOT needed - UO uses horizontal flip)

### Step 2: Low vs High Creature Decision

| Feature | Low Creature | High Creature |
|---------|-------------|---------------|
| Run animation | YES (required for mounts) | NO |
| Frames per slot | Fewer | More (up to 10 per direction) |
| Animation slot types | Fewer | More (includes Eat, Stomp, etc.) |
| Slot prefix | L: | H: |

- **People & Wearables** use P: prefix in mulpatcher

### Step 3: Frame Limits & Selection

**High creature frame limit:** 10 frames per direction per animation type  
- walkdown = max 10 frames
- walkDL = max 10 frames
- walkleft = max 10 frames
- walkUL = max 10 frames
- walkup = max 10 frames

**Tips:**
- If you lack a specific animation type (e.g., BlockRight), look at an existing creature (e.g., red dragon) and use a similar animation set
- You can mix-and-match frames from any animation type or direction
- Reverse frame order numbers for certain effects
- Test animation sequence with BMPs: use folder preview + right arrow key to scroll through frames

### Step 4: Calculations & Slot Assignment

**Tools needed for this step:**
- mulpatcher
- UO Animation Calculator
- UOAnim
- michelangelo
- UOFiddler

**Process:**

1. **mulpatcher.exe** - Open, load `anim.mul` + `anim.idx`
   - Docker window appears: all changes made "on the fly"
   - Go to "Anim" tab -> "Empty Slots"
   - Find and select an empty slot:
     - H = high level creature
     - L = low level creature
     - P = People & Wearables
   - **Note the slot number** (example used: H:0x4F = decimal 79)

2. **UO Animation Calculator** - Type decimal slot number, press Enter
   - Note the "First Animation Frame" number
   - Example: slot 79 = first animation frame **8690**

3. **UOFiddler (or breakdown.rar)** - Reference for animation type numbers
   - Standard animation type sequence: 0=Walk, 1=Idle, 2=... etc.
   - Pre-make folders named `[number]-[animation type]` (e.g., `0-Walk`, `1-Idle`)

### Step 5: BMP to UOP Conversion (UOAnim)

**Sequence order is critical:** Down, Down Left, Left, Up Left, Up

1. Open **UOAnim**, click "Add Animation"
2. Enter "First Animation Frame" number from UO Animation Calculator in "Block Number"
3. Click "Add Image" and load the **first BMP for WalkDown**
4. Continue "Add Image" for all WalkDown BMPs in order
5. Click "Add Animation" for next direction (WalkDL), set Block Number to +1
   - Example: 8690 (WalkDown) -> 8691 (WalkDL) -> 8692 (WalkLeft) -> 8693 (WalkUL) -> 8694 (WalkUp)
6. After all 5 directions complete, click "Create Patch" -> save as `0-walk.uop`
7. **Note the last block number used**
8. Close and reopen UOAnim
9. Repeat for next animation type, starting block number at last+1
   - Example: 0-walk ended at 8694, so 1-Idle starts at 8695
10. Repeat for ALL animation types and directions
11. Result: one `.uop` file per animation type (0-walk.uop, 1-idle.uop, etc.)

**WARNING:** If you make a mistake, you must start over. Be meticulous.

### Step 6: UOP to VD Conversion (Michelangelo)

1. Open **michelangelo**, click "Import"
2. Import each animation .uop in order from 0 to last number (must be sequential)
3. Optional but recommended: click "Save" and save complete animation as `AnimationName.uop` (e.g., `RoyalGriffin.uop`)
4. Click "Export" -> export to **verdata.mul**
   - To create a new verdata.mul: create a text file, rename it `verdata.mul` (delete .txt extension)
5. Close michelangelo

### Step 7: Loading VD into MUL Files (Mulpatcher)

**Open mulpatcher with these files:**
- anim.mul
- anim.idx
- (optional: verdata.mul for reference)

1. Go to "Anim" tab -> select "Full Slots"
2. Find your animation slot number (green color = your slot)
3. Click to select, right-click -> "Save to File" (name it anything, or use slot number)
4. Close mulpatcher

### Step 8: Applying to Anim Files (Mulpatcher)

**Open mulpatcher with:**
- anim.mul
- anim.idx
- tiledata.mul
- art.mul
- art.idx
- (optional: one of the other anim#.muls)

1. Go to "Anim" tab, find your animation slot number
2. Single click to select, right-click -> "Load from File"
3. Load your `YourAnimationName.vd` or `slot#.vd`

### Step 8b: Mount-Specific Steps (Only for mounts)
**Note: Only works with clients up to 7.0.8.2**

1. Go to "TileDataS" tab
2. Click "Fill Slots to 0x7FFF"
3. Find an empty slot and set:
   - **Name:** Your Animation's Name
   - **Mount AnimID:** Your animation's animation #
   - **Weight:** 1
   - **Height:** 1
   - **Quality:** 25
   - **Check:** Wearable, and Animation
   - Note: In mulpatcher, AnimID is hex #; UOFiddler uses decimal #
4. Go to "Settings" tab, click "Save" next to tiledata

**Optional - Shrunk Pet Art:**
1. Go to "ArtS" tab -> select empty slots
2. Find empty slot, right-click -> "Load from Bitmap"
3. Load the reduced BMP (~30x45px) of your new animation
4. Go to "Settings" -> save art.mul and art.idx

### Step 9: Config File Edits

All of these files need to be edited to register your new animation:

#### bodyconv.def
Tells the client where to find the animation.
```
353 -1 -1 -1 -1 #Tiger
```
Format: `[animation slot #] [anim2] [anim3] [anim4] [anim5] #[name]`
- Slot numbers correspond to anim.mul, anim2.mul, anim3.mul, anim4.mul, anim5.mul
- `-1` means "not used in this anim#.mul"
- You CAN add animations to other anim#.muls

#### Corpse.def
Tells client what death animation to use for a corpse.
```
#Tiger 353 {353} 0
```
Format: `#[name] [animation slot] {[death animation slot]} [corpse hue]`
- The 0 is corpse hue
- Not always needed but recommended to add

#### Mobtypes.txt
Sets the animation "type" category.
```
353 ANIMAL 0 #Tiger
```
- Types: `ANIMAL`, `MONSTER`, `EQUIPMENT`, etc.
- Changing ANIMAL to MONSTER changes which animation blocks are available
- Must use the same #name as bodyconv.def (exact match)

#### body.def
Sometimes needed for animation display issues.
```
#New Nightmare 354 {354} 0
```
- Not always needed; add if animation won't show up

#### Shrink.cfg (mounts only)
Links animation number to itemID for shrinking.
```
277 0x2D96
```
- 277 = animation # | 0x2D96 = itemID from tiledata.mul (hex)

### Animation Slot Numbering Notes
- In mulpatcher: AnimID is **hex**
- In UOFiddler: AnimID is **decimal**
- Block numbers increment by 1 per direction per animation type

---

## Animations - Item Animations

**Source:** Tutorial #2 - "Adding Item Animations" by Amadora (Nov 13, 2022)

### Overview
How to create animated items (like the animated Christmas hedge) using UOFiddler. Item animations use multiple sequential art IDs cycled through AnimData.

### Step-by-Step Process

**Tool required:** UOFiddler

#### Step 1: Prepare Art Frames
- Have the item art and number of frames ready
- Example: 4-frame animated hedge
  - Frame IDs: 28821, 28822, 28823, 28824 (sequential Item IDs in the Art tab)

#### Step 2: TileData Configuration
1. Go to the **TileData tab** in UOFiddler
2. Use Search to find all 4 frame items
3. Add these **tags/flags to ALL 4 items:**
   - Impassable
   - Article A
   - Animation
4. Set for each item:
   - **Weight:** 255
   - **Height:** 5 (may vary depending on animation size)

#### Step 3: AnimData Configuration
1. Go to the **AnimData tab** in UOFiddler
2. Right-click -> Add
3. Enter the **Item number of the LAST frame** you want animated
   - Example: Enter 28824 (the 4th/last hedge)
4. After adding, look to the right at the "data" section:
   - **Start Delay:** 3 (default, adjust for speed)
   - **Frame Delay:** 3 (default, adjust for speed)
5. In the "Frames" section, click the small box and add frames in sequence:
   - Add 28821, click Add
   - Add 28822, click Add
   - Add 28823, click Add
   - Add 28824, click Add
6. Click Start to preview
7. Adjust Start Delay and Frame Delay until timing is correct

#### Step 4: Save and Pack
1. Save **AnimData** tab
2. Save **Items/Art tab**
3. Save **TileData tab**
4. Go to **UO Packer tab** in UOFiddler
5. Navigate to your fiddler folder
6. Click "Pack MUL to UOP"

#### Step 5: Distribute Files
Files to copy to UO client folders:
- `Animdata.mul`
- `artlegacyMUL.uop`
- `tiledata.mul`

If multiple UO client folders:
- Put files in a folder and zip
- Unzip into first UO folder, then next, etc.

For a personal shard:
- Add to the folder your shard uses to start up
- Also add to the UO client folder used to log in

---

## Animations - Extracting from FLC/GIF

**Source:** Tutorial #3 - "Custom Animations - extracting from a .flc/.gif" by Redmoon (Sep 24, 2021)

### Overview
How to extract animation frames from other games or downloads and prepare them for use as custom UO animations.

### Tool Required
**Jasc Animation Shop** (works with both .flc and .gif formats)

### Step-by-Step Process

1. **Open the .flc** in Jasc Animation Shop

2. **Resize** the animation to **400x400 pixels**
   - This size works well for most ridable creatures (sphynx, tiger class)
   - Experiment with size to suit your needs

3. **Zoom in** - recommended 5:1 to 9:1 ratio

4. **Replace background color** with white or black:
   - Use RGB `255,255,255` (white) - author's preference
   - OR RGB `0,0,0` (black)
   - Set **tolerance to 30** to start (adjust to preference)
   - **IMPORTANT:** Select "all frames" - otherwise it only applies to one frame

5. **Clean up remaining background:**
   - Select new replacement colors using the dropper tool
   - Or use # hex values
   - Or use the color wheel
   - Use Ctrl+Z to undo mistakes

6. **Preview** using the "View Animation" button

7. **Save the modified FLC** (author overwrites original, keeping untouched copies as backup)

8. **Export frames as BMPs:**
   - Click 1st frame
   - Ctrl+A (select all frames)
   - File -> "Save Frames As"
   - **Save as .bmp with long file names**
   - Make sure ALL frames are selected (not just one)
   - Save to a named folder (e.g., "Walk" for walk animation)

9. **Result:** All animation frames extracted as individual .bmp files

### Tips
- Have a folder named for your new BMPs (helps with organization for the next steps)
- Author made a .gif tutorial video demonstrating the process
- View .gif tutorial in QuickTime to pause when needed

---

## Map Tiles & Map Creation

**Source:** Tutorial #4 - "Map Tiling - Deep Dive!" by Wilson (Aug 2, 2025)

### Overview
This tutorial is primarily a **video resource** with minimal text content. It references:
- "World Tiling - How was it done"
- Video Source: https://www.reddit.com/r/gamedev/comments/d3cd2v/anyone_know_how_the_ultima_online_terrain_effect

The video likely explains the UO terrain blending/tiling system. The UO terrain system uses overlapping tile art to create smooth transitions between terrain types (grass/dirt/water etc.), which is a signature visual feature of the game.

### UO Terrain Tiling System (Background Knowledge)
- UO uses a 2D isometric map system
- Terrain tiles are 44x44 pixels (isometric diamond shape)
- The engine blends adjacent tile types using "transition" or "overlay" tiles
- This creates smooth visual transitions between terrain types
- Map data stored in map#.mul files (map0.mul through map5.mul for different facets)

---

## Map Extraction - Yoinking Map Sections

**Source:** Tutorial #7 - "How to *yoink* parts of a map" by Redmoon (Sep 24, 2021)

### Overview
"Yoink" = to snatch or take - this tutorial covers copying sections of one UO map into another using coordinate-based extraction.

### Tools Required
- **UO Fiddler**
- **Map Extractor 1.6** (http://www.runuo.com/community/threads/map-extractor.468585/)

### Step-by-Step Process

1. **Open UO Fiddler** with Path Settings pointed to the **source map** (the one to copy FROM)

2. **Zoom to the area** you want to copy, hover on the **northwest corner** of the region
   - Write down the coordinates (X, Y)

3. **Switch UO Fiddler** Path Settings to the **destination map** (where you're placing the region)

4. **Zoom to where** you want the new area placed, hover on the **northwest corner**
   - Write down the destination coordinates (X, Y)

5. **Open Map Extractor 1.6** and configure:
   - **Source MUL Files:** Folder of the source map (map to copy FROM)
   - **Destination MUL Files:** Folder of the destination map
   - **Source Map:** Map type of the source (e.g., Felucca, Trammel, Tokuno, etc.)
   - **Destination Map:** Map where the new area will be placed
   - **Copy Portion of Map:**
     - **X:** X location of source area northwest corner
     - **Y:** Y location of source area northwest corner
     - **Width:** Source X2 minus Source X1
     - **Height:** Source Y2 minus Source Y1
   
   **Example calculation:**
   ```
   Source NW corner:      3502, 1976
   Destination NW corner: 3853, 2308
   
   Width  = 3853 - 3502 = 351
   Height = 2308 - 1976 = 332
   ```
   
   - **Destination:**
     - **X:** X location in destination map where the new area goes
     - **Y:** Y location in destination map where the new area goes

6. **Click Start**

7. **Verify in UO Fiddler** - check the destination map to make sure everything looks correct

8. **In-game verification** - log into the game and walk around the new area to double-check

---

## Custom Item Scripting

**Source:** Tutorial #6 - "Beginner's Guide to Creating a Basic Item Script" by JBob (Feb 18, 2025)

### Overview
Complete beginner tutorial for creating a C# item script in ServUO. Covers file setup, namespaces, class structure, constructors, serialization, and in-game events.

### Step 1: File Setup
- Navigate to your ServUO `Scripts/` directory
- Create a subfolder for custom scripts (e.g., `Scripts/Custom/`)
- Create file: `MyFirstItem.cs` (.cs = C# code file)
- Recommended editors: Visual Studio Code, Notepad++

### Step 2: Using Statements
```csharp
using System;       // Basic C# features (DateTime, String, Int32, etc.)
using Server;       // Core ServUO functionalities
using Server.Items; // Item class and utilities
```

### Step 3: Namespace and Class Declaration
```csharp
namespace Server.Items
{
    public class MyFirstItem : Item
    {
        // Constructors and methods go here
    }
}
```
- `namespace Server.Items` - standard container for custom items; helps ServUO locate scripts
- `public class MyFirstItem : Item` - inherits from ServUO's built-in `Item` class

### Step 4: Constructable Constructor
```csharp
[Constructable]
public MyFirstItem() : base(0x1B7)  // 0x1B7 = statue graphic
{
    Name = "My First Item";
    Hue = 1153;     // Optional: item color
    Weight = 1.0;   // Optional: item weight
}
```
- `[Constructable]` - attribute that allows in-game creation via `[/add MyFirstItem`
- `: base(0x1B7)` - calls parent constructor with Item ID (graphic)
- Common Item IDs: `0x1B7` (statue), `0x1F4` (bag), `0x0E21` (sword)
- `Hue` - color ID applied to item (many IDs available; look up hue table)
- `Name` - display name in-game
- `Weight` - item weight value

### Step 5: Serial Constructor (Load from Save)
```csharp
public MyFirstItem(Serial serial) : base(serial)
{
}
```
- Required - without this, ServUO cannot load the item from save files
- `Serial` = unique identifier for the item

### Step 6: Serialization (Save/Load Data)
```csharp
public override void Serialize(GenericWriter writer)
{
    base.Serialize(writer);
    // writer.Write(myIntField);  // Write custom fields
}

public override void Deserialize(GenericReader reader)
{
    base.Deserialize(reader);
    // myIntField = reader.ReadInt();  // Read custom fields
}
```
- `Serialize` - called on server save/shutdown
- `Deserialize` - called when loading item from save file
- Always call `base.Serialize(writer)` / `base.Deserialize(reader)` first
- To store custom data: add class-level variable (e.g., `private int m_Uses;`)
  - Write: `writer.Write(m_Uses);`
  - Read: `m_Uses = reader.ReadInt();`

### Step 7: Double-Click Handler
```csharp
public override void OnDoubleClick(Mobile from)
{
    if (!from.CanSee(this))
    {
        from.SendMessage("You can't see that.");
        return;
    }
    from.SendMessage("You double-clicked the item: " + this.Name);
}
```
- `OnDoubleClick(Mobile from)` - called whenever a player double-clicks the item
- `from` = the Mobile (player/creature) who performed the action
- `from.CanSee(this)` - visibility check
- `from.SendMessage("...")` - sends text to the player's chat

### Step 8: Complete Basic Item Script
```csharp
using System;
using Server;
using Server.Items;

namespace Server.Items
{
    public class MyFirstItem : Item
    {
        [Constructable]
        public MyFirstItem() : base(0x1B7)
        {
            Name = "My First Item";
            Hue = 1153;
            Weight = 1.0;
        }

        public MyFirstItem(Serial serial) : base(serial)
        {
        }

        public override void Serialize(GenericWriter writer)
        {
            base.Serialize(writer);
        }

        public override void Deserialize(GenericReader reader)
        {
            base.Deserialize(reader);
        }

        public override void OnDoubleClick(Mobile from)
        {
            if (!from.CanSee(this))
            {
                from.SendMessage("You can't see that.");
                return;
            }
            from.SendMessage("You double-clicked the item: " + this.Name);
        }
    }
}
```

### Step 9: Testing In-Game
1. Save file and restart ServUO server
2. Log in as GM/Admin character
3. Create item: type `[/add MyFirstItem` in chat, press Enter, target location
4. Double-click the item to test functionality

### FAQ
- **Why two constructors?** One `[Constructable]` for new items, one for loading from saves
- **Store custom data?** Add `private int m_Uses;` -> write with `writer.Write(m_Uses)`, read with `m_Uses = reader.ReadInt()`
- **Change graphic?** Change `0x1B7` to any valid Item ID
- **What is Hue?** Color applied to item; many IDs exist, look up hue table or experiment

---

## Tools & Workflow Reference

### Complete Tool List (from all tutorials)

| Tool | Purpose | Used For |
|------|---------|----------|
| **mulpatcher** | MUL file editor | Loading/saving animations to anim.mul, managing tiledata, art slots, animation slots |
| **UO Animation Calculator** | Calculate frame numbers | Converts slot # to first animation frame number |
| **UOAnim** | BMP to UOP conversion | Creates .uop animation files from BMP sequences |
| **michelangelo** | UOP to VD aggregation | Combines all animation type .uop files, exports to verdata.mul |
| **UOFiddler** | All-in-one UO file editor | AnimData, TileData, Art, Map viewing, UO Packer |
| **Jasc Animation Shop** | Animation editing | Opening FLC/GIF files, resizing, background removal, frame export |
| **Map Extractor 1.6** | Map section copying | Copies portions of one UO map into another |
| **Photoshop** | Image editing | Frame flipping, cleanup |
| **Corel PhotoPaint** | Image editing | Alternative to Photoshop for frame work |

### mulpatcher Key Features
- Loads: anim.mul, anim.idx, tiledata.mul, art.mul, art.idx, verdata.mul
- Tabs: Anim, TileDataS, ArtS, Settings
- "Empty Slots" vs "Full Slots" view toggle
- Slot color coding: green = your added animation
- Right-click options: Save to File, Load from File, Load from Bitmap
- AnimID in mulpatcher is **HEX** (vs UOFiddler which uses **decimal**)
- "Fill Slots to 0x7FFF" option in TileDataS tab

### UOFiddler Key Features
- Tabs: Art, TileData, AnimData, Map, UO Packer
- AnimData: right-click to add items, set Start Delay, Frame Delay, add Frame IDs
- UO Packer: "Pack MUL to UOP" functionality
- TileData: Search, set flags (Impassable, Article A, Animation, etc.), Weight, Height
- Path Settings: point to different UO client/map folders

### michelangelo Workflow
1. Import each .uop (animation type files) in order
2. Optional: Save combined .uop (e.g., CreatureName.uop)
3. Export to verdata.mul

### UOAnim Workflow
- "Add Animation" button = starts new animation direction (set Block Number)
- "Add Image" button = adds BMP frame to current animation
- "Create Patch" = generates .uop file
- Block numbers must be sequential and continuous across all animation types

---

## File Formats Reference

| Format | Description |
|--------|-------------|
| `.bmp` | Bitmap image - individual animation frames |
| `.flc` | FLIC animation format - source animation from other games |
| `.gif` | Animated GIF - alternative source animation format |
| `.uop` | UO Package format - compiled animation data |
| `.vd` | Verdata format - intermediate animation file |
| `.mul` | UO Multi-format - main game data files |
| `.idx` | Index file - paired with .mul files for fast access |
| `.cs` | C# source code - ServUO scripts |

### Key MUL Files

| File | Contents |
|------|----------|
| `anim.mul` / `anim.idx` | Main animation data (creatures, characters) |
| `anim2.mul` through `anim5.mul` | Additional animation banks |
| `tiledata.mul` | Tile properties/flags for all items and terrain |
| `art.mul` / `art.idx` | Art (sprites) for items |
| `artlegacyMUL.uop` | Newer UOP-format art file |
| `map0.mul` through `map5.mul` | World map data for each facet |
| `verdata.mul` | Patch/override data |
| `animdata.mul` | Item animation cycling data |

---

## Config Files Reference

These text/def files control animation behavior in ServUO:

### bodyconv.def
Maps animation slot numbers to their locations in anim#.mul files.
```
[slot#] [anim1_slot] [anim2_slot] [anim3_slot] [anim4_slot] [anim5_slot] #[name]
```
- `-1` = not in that anim file
- Example: `353 -1 -1 -1 -1 #Tiger` (only in anim.mul slot 353)

### Corpse.def
Maps animation to its corpse death animation.
```
#[name] [anim_slot] {[corpse_anim_slot]} [corpse_hue]
```
- Example: `#Tiger 353 {353} 0`

### Mobtypes.txt
Sets creature category/type for animation system.
```
[slot#] [TYPE] [?] #[name]
```
- Types: `ANIMAL`, `MONSTER`, `EQUIPMENT`
- ANIMAL vs MONSTER determines available animation blocks
- Example: `353 ANIMAL 0 #Tiger`

### body.def
Fallback/redirect for animation display.
```
#[name] [anim_slot] {[anim_slot]} [hue]
```
- Example: `#New Nightmare 354 {354} 0`

### Shrink.cfg
Links mount animation to shrunk pet item ID.
```
[anim_slot] [itemID_hex]
```
- Example: `277 0x2D96`
- 277 = animation number
- 0x2D96 = itemID in tiledata.mul

---

## Additional Notes & Gotchas

### Animation Direction System
- UO standard direction order: **Down, Down Left, Left, Up Left, Up**
- Right-facing directions NOT needed: UO engine automatically mirrors Left side
- "Not Needed" folder = storage for right-facing BMPs that will be horizontally flipped

### Client Version Compatibility
- Mount animation setup (TileDataS steps) only works with clients **up to 7.0.8.2**

### Backup Strategy
- ALWAYS keep untouched backup copies of source animations (FLC, GIF, or BMP)
- DO NOT empty recycle bin until animation is 100% confirmed complete
- Do not mix up original and working copies

### Frame Testing Without Re-exporting
- Can test BMP sequence without creating new FLC/GIF
- Enable folder image preview (right side of window)
- Click first frame, use right arrow key to scroll through frames slowly

### Item Animation Timing Parameters (AnimData)
- **Start Delay:** Controls delay before animation begins (default: 3)
- **Frame Delay:** Controls speed between frames (default: 3)
- Higher = slower; lower = faster

### Slot Numbering Systems
- mulpatcher: uses **hexadecimal** for AnimID
- UOFiddler: uses **decimal** for AnimID
- Always convert when switching between tools

### TileData Flags for Animated Items
Required flags for animated items:
- **Impassable** - can't walk through
- **Article A** - "A [item name]" grammatical prefix
- **Animation** - enables the animation cycling

### Map Facets (UO Worlds)
- Map 0: Felucca
- Map 1: Trammel
- Map 2: Ilshenar
- Map 3: Malas
- Map 4: Tokuno
- Map 5: Ter Mur

---

*End of research file. Compiled from ServUO.dev tutorials. For the most up-to-date information, refer to the original tutorial pages linked above.*
