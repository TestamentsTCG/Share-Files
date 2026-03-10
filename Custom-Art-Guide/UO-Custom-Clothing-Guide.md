# UO Custom Clothing Guide
**For:** Mike & Zabulus  
**Project:** Heroes of Holdem / Perilous Legends  
**Compiled by:** Elijah (AI Research Agent)  
**Date:** 2026-03-09  
**Sources:** ServUO.dev tutorials + community research

---

## Overview: The 3 Visual Representations of Clothing

Every wearable item in UO has up to 3 distinct visual representations. Understanding each one is critical before you start making art.

| Representation | Where It Appears | Required? | Art Format |
|----------------|-----------------|-----------|------------|
| **Ground/Backpack Icon** | Item on the ground, in bags, on vendor | YES | .bmp (44x44 area, isometric) |
| **Paperdoll Image** | Character screen (Equipment screen) | YES | .bmp (~60x90px region) |
| **On-Character Sprite** | Character wearing it in the world (walking, fighting, etc.) | Optional* | .bmp frames -> animation pipeline |

> **Critical insight from field research:** For most clothing items, you do NOT need to create custom on-character sprites. UO uses a layer system - the character body already has built-in animations for each clothing layer. You declare which layer your item uses, and UO renders the body animation automatically. The item looks unique in the paperdoll and on the ground. This is how most UO shards (including Outlands) handle custom clothing.
>
> **Only if** you want the item to look visually different on the character during movement do you need the full animation pipeline.

---

## Minimum Viable Art Per Item

For standard clothing with no custom on-character appearance:

```
3 files per item:
  1. paperdoll.bmp     - appears in character equipment screen
  2. groundicon.bmp    - appears on ground and in backpack
  3. MyClothingItem.cs - C# script (defines layer, name, stats)
```

**30 items = 90 files total.**

---

## Part 1: The Paperdoll Image

### What It Is
The paperdoll image is the large character portrait shown in the Equipment screen (double-click your character). When the player equips your item, this graphic overlays the character portrait showing the clothing on the body.

### Specs
- Format: `.bmp` (also accepts `.tiff` or `.jpg`)
- Size: roughly 60x90px visible area, but UO crops to the character silhouette
- Transparent/background color: pure black `(0,0,0)` or pure white `(255,255,255)`
- The image should show the clothing piece in the correct body position

### How to Add It (UOFiddler)

1. Open **UOFiddler**, navigate to the **GUMPS tab**
2. Top left: click **Misc > Show Free Slots**
3. Scroll down to **0xC350 (decimal 50000)**

**Choosing your slot number:**

| Slot Range | Use For |
|------------|---------|
| 50000-50999 | Default (male) wearables |
| 50400-50999 | **Recommended** - wearables that appear correctly when sitting |
| 60000-60999 | Female-only version (mirrors male slot - e.g., male at 50400 = female at 60400) |

4. Find an **empty red slot** in your target range
5. Right-click the red slot -> **Replace**
6. Navigate to your paperdoll `.bmp` -> **Open**
7. Right-click again -> **Save**
8. **Write down your slot number** (you need it for everything else)

> **Tip:** Use a hex/decimal converter if needed: http://www.mathsisfun.com/binary-decimal-hexadecimal-converter.html

---

## Part 2: The Ground/Backpack Icon

### What It Is
This is the isometric "tile" sprite shown when the item is on the ground, sitting in a backpack, or held by a vendor. It's a small icon that represents the item as a physical object.

### Specs
- Format: `.bmp` (also accepts `.tiff` or `.jpg`)
- UO isometric tile: 44x44px diamond area (the actual image can be larger - UO auto-crops to the diamond)
- Background color: pure black or pure white (same as paperdoll)

### How to Add It (UOFiddler)

1. Navigate to the **ITEMS tab** in UOFiddler
2. Right-click -> **Insert at**
3. Type in the **same number you used in the Gumps tab** (e.g., 50400)
   - These two IDs must match
4. Right-click -> **Save**

---

## Part 3: TileData Configuration

This is what tells UO how to treat the item - that it's wearable, what animation it uses, etc.

1. Navigate to the **TILEDATA tab** in UOFiddler
2. Scroll to your **slot number** (e.g., 50400)
3. Set the following:

### Required Fields

| Field | Value | Notes |
|-------|-------|-------|
| **WEARABLE** flag | Checked | Marks this item as wearable |
| **ANIM** number | `GumpID - 50000` | Example: slot 50400 → ANIM = 400 |

### Optional but Recommended

| Field | Value | Notes |
|-------|-------|-------|
| **NAME** | "Long Fancy Shirt" | Item name in TileData |
| **ARTICLEA** | Checked | Use "a" before name ("a Long Fancy Shirt") |
| **ARTICLEAN** | Checked instead | Use "an" before name ("an Elven Robe") |
| **QUALITY** | Layer number | Clothing layer (can also be set in script) |
| **WEIGHT** | Item weight | Can also be set in script |

4. Click **Save Changes** -> **Save Tiledata**

---

## Part 4: On-Character Appearance (Animation Layer)

### Option A: Use an Existing Animation (Recommended - No Extra Art Needed)

This is the standard approach. You tell UO to use an existing clothing animation from the base game.

1. In UOFiddler, go to **ANIMATIONS tab**
2. Scroll to **Equipment > Animations #400-997**
3. Find the animation that **looks closest** to your clothing piece
4. Note the number in parentheses (example: "Fancy Shirt (435)")

Now link your new item to this animation:

1. Open your UO **client folder**
2. Open `Body.def` in a text editor
3. Add a line:

```
[GumpID - 50000] {[AnimationID]} [Hue]
```

Example:
```
400 {435} 0
```
- `400` = your slot ID minus 50000
- `435` = the existing fancy shirt animation
- `0` = no hue change

**Result:** Your item renders on-character using the fancy shirt animation. Players see it moving with the character.

> You can reuse the same animation for multiple clothing items by adding multiple `Body.def` lines pointing to the same animation ID. This is standard practice.

---

### Option B: Export an Existing Animation and Re-use It

If the existing animation type fits but you want to assign it to a new slot:

1. In UOFiddler: **ANIMATIONS > EQUIPMENT**
2. Find your target animation (e.g., "Elven Robe e02 (899)")
3. Bottom of screen: **Settings > Animation Edit**
4. Top left: **Choose Anim File** -> select the correct `anim` file
5. Scroll to your animation, right-click -> **Export > To .vd**
6. Files export to your UOFiddler folder (usually `C:\Users\[user]\AppData\Roaming\UoFiddler`)

> **FAQ:** If the animation name is in red, it's a re-hued version of another animation. Find the base animation and use that instead. Example: "Elven Robe e02 (899)" is just a rehued "Kamishimo (517)" - use 517 instead. Also note: some animations are in `anim4` not `anim` - navigate there if you can't find it.

> **Note:** New animations can only be installed into open slots 400-499.

---

### Option C: Fully Custom On-Character Sprites

**Only needed if you want unique character movement animations for this clothing item.**

This is the expensive path. Each clothing direction requires individual BMP frames. Here is the full pipeline:

#### Tools Required
- **Jasc Animation Shop** - for extracting/editing animation frames from source files
- **UOAnim** - converts BMP frame sequences to .uop
- **Michelangelo** - aggregates .uop files, exports to verdata.mul
- **Mulpatcher** - loads animations into anim.mul
- **UOFiddler** - manages TileData, Art, and packing
- **UO Animation Calculator** - converts slot numbers to frame numbers

#### Source Art
You need BMP frames for **5 directions** (UO mirrors the 3 right-facing directions automatically):
- Down
- Down-Left
- Left
- Up-Left
- Up

Maximum **10 frames per direction per animation type** (for high-creature type).

For clothing, you use the **P: prefix** (People & Wearables) in mulpatcher.

#### Step-by-Step Pipeline

**Step 1: Prepare BMPs**
- One folder per animation type (Walk, Idle, Attack, etc.)
- Sub-folders per direction (Down, DownLeft, Left, UpLeft, Up)
- Name files sequentially: `walkdown_1.bmp`, `walkdown_2.bmp`, etc.
- Background: pure white (255,255,255) or pure black (0,0,0)
- Test sequence: enable folder thumbnail preview, use arrow key to flip through frames

**Step 2: Assign an Animation Slot**
1. Open **mulpatcher** with anim.mul + anim.idx
2. Go to **Anim tab > Empty Slots**
3. Find empty slot with P: prefix (People & Wearables)
4. Note the slot number (example: P:0x4F)
5. In **UO Animation Calculator**, enter the decimal slot number
6. Note the "First Animation Frame" number (example: slot 79 = frame 8690)

**Step 3: Convert BMPs to UOP (UOAnim)**

Direction block order is critical: **Down (block 0) → Down-Left (+1) → Left (+2) → Up-Left (+3) → Up (+4)**

For each animation type:
1. Open UOAnim -> Add Animation
2. Set Block Number to your "First Animation Frame"
3. Add Image for each BMP in the Down direction (in order)
4. Add Animation for Down-Left (Block Number +1), add BMPs
5. Repeat for Left (+2), Up-Left (+3), Up (+4)
6. Create Patch -> save as `0-walk.uop`
7. Note the last block number used
8. Close and reopen UOAnim
9. Next animation type starts at last block number + 1
10. Repeat for all animation types

**Step 4: UOP to VD (Michelangelo)**
1. Open Michelangelo
2. Import each animation .uop in order (0-walk.uop, 1-idle.uop, etc.)
3. Optional: Save combined as `ClothingName.uop`
4. Export to **verdata.mul**

**Step 5: Load Into MUL (Mulpatcher)**
1. Open mulpatcher with anim.mul + anim.idx + tiledata.mul + art.mul + art.idx
2. Go to Anim tab -> Full Slots
3. Find your animation slot (green = yours)
4. Right-click -> Load from File -> select your .vd file

**Step 6: Edit Body.def**
```
[SlotID - 50000] {[YourNewAnimationSlot]} 0
```

---

## Part 5: Saving and Distributing Files

### Files Modified

After completing your UOFiddler work, these files need to be copied to your UO client and server:

| File | Where Modified | Purpose |
|------|---------------|---------|
| `Gumpart.mul` / `Gumpidx.mul` | UOFiddler | Paperdoll graphics |
| `art.mul` / `artidx.mul` | UOFiddler | Ground/backpack icons |
| `tiledata.mul` | UOFiddler | Item properties/flags |
| `Body.def` | Text editor | Animation assignment |
| `animdata.mul` | UOFiddler (if animated item) | Item animation cycling |
| `artlegacyMUL.uop` | UOFiddler UO Packer | Packed art file |

### Copying Files
1. Navigate to your **UOFiddler folder** (`C:\Users\[user]\AppData\Roaming\UoFiddler`)
2. Copy: `art.mul`, `artidx.mul`, `Gumpart.mul`, `Gumpidx.mul`, `tiledata.mul`
3. Paste/overwrite to your **CLIENT directory**
4. Also overwrite in your **server startup folder**

> Always backup originals before overwriting.

---

## Part 6: The C# Item Script

Once the art is in place, you need a script that registers the item in the game.

```csharp
using System;
using Server;
using Server.Items;

namespace Server.Items
{
    public class LongFancyShirt : BaseClothing
    {
        [Constructable]
        public LongFancyShirt() : base(0xC500)  // Replace 0xC500 with your actual ItemID (GumpID in decimal/hex)
        {
            Name = "long fancy shirt";
            Layer = Layer.InnerTorso;  // Set to the correct clothing layer
            Hue = 0;                   // 0 = no hue, or set a default color
        }

        public LongFancyShirt(Serial serial) : base(serial)
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
    }
}
```

### Key Values to Change
- **`0xC500`** - Replace with your GumpID in hex (e.g., if your slot is 50400, that's `0xC500` in hex)
- **`Layer`** - The clothing layer. Common values:

| Layer | Body Part |
|-------|-----------|
| `Layer.InnerTorso` | Inner shirt/body |
| `Layer.OuterTorso` | Outer shirt/robe |
| `Layer.Pants` | Pants/legs |
| `Layer.Shoes` | Footwear |
| `Layer.Helm` | Head/helmet |
| `Layer.Gloves` | Hands/gloves |
| `Layer.Cloak` | Back/cloak |
| `Layer.Arms` | Arms/sleeves |
| `Layer.Neck` | Neck/gorget |
| `Layer.Waist` | Belt/waist |
| `Layer.Ring` | Ring (right) |
| `Layer.Bracelet` | Bracelet |
| `Layer.Earrings` | Earrings |

### Adding In-Game
After restarting the server:
```
[add LongFancyShirt
```
Target a location to place it, then equip and verify it appears correctly in the paperdoll and in the world.

---

## Part 7: Male vs Female Versions

UO supports gender-specific paperdoll graphics.

- **Male (default):** Placed in slots **50000-50999**
- **Female:** Placed in slots **60000-60999**

The female slot number = male slot number + 10000.

Example:
- Male Long Fancy Shirt: slot **50400**
- Female Long Fancy Shirt: slot **60400**

Both map to the same item script. UO automatically selects the correct paperdoll graphic based on character gender.

If you don't create a female version, the male paperdoll will display on female characters.

---

## Part 8: Quick Reference Checklist

### Per Item Checklist (Minimum - No Custom On-Character Sprites)

- [ ] Create paperdoll .bmp (shows on equipment screen)
- [ ] Create ground icon .bmp (shows on ground/in backpack)
- [ ] Open UOFiddler - add paperdoll to GUMPS tab (slot 50000-50999)
- [ ] Open UOFiddler - add ground icon to ITEMS tab (same slot number)
- [ ] Open UOFiddler - configure TILEDATA tab (WEARABLE flag, ANIM number)
- [ ] Edit Body.def - assign to existing animation
- [ ] Write .cs script (set ItemID, Layer, Name)
- [ ] Copy modified .mul files to client and server
- [ ] Restart server, test in-game with `[add ClassName`

### If Creating Female Version
- [ ] Create female paperdoll .bmp
- [ ] Add to GUMPS tab at slot 60000+ (matching male slot +10000)
- [ ] Add to ITEMS tab at same slot

### If Creating Fully Custom On-Character Sprites
- [ ] Prepare BMP frames for all 5 directions x all animation types
- [ ] Run UOAnim to create per-animation .uop files
- [ ] Run Michelangelo to aggregate and export to verdata.mul
- [ ] Run Mulpatcher to load into anim.mul
- [ ] Edit Body.def to point to new animation slot
- [ ] Edit bodyconv.def, Mobtypes.txt

---

## Useful Links

- ServUO Wearables Tutorial: https://www.servuo.dev/archive/adding-custom-wearables-clothing-armor-weapons.1626/
- Daz Studio to Blender Pipeline: https://www.servuo.dev/archive/creating-uo-sprites-with-daz-studio-and-blender.1926/
- Custom Animations (Full): https://www.servuo.dev/archive/how-to-add-custom-animations-to-uo.1629/
- UOFiddler GitHub: https://github.com/polserver/UOFiddler
- Tile Object Placer (TOP) Tool: https://www.servuo.com/archive/tile-object-placer-top.1920/
- Hex/Decimal Converter: http://www.mathsisfun.com/binary-decimal-hexadecimal-converter.html

---

*Guide compiled by Elijah (AI Research Agent) from ServUO community tutorials. For questions or updates, contact Elijah via Telegram.*
