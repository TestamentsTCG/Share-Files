# ServUO Art & Animation Research

**Date:** 2026-03-09  
**Focus:** Artwork creation, modification, animation for clothing, map tiles, custom items

## Problem Encountered

Most detailed ServUO tutorials require account registration:
- "Creating UO sprites with Daz Studio and Blender" (5-star rated, 8.6k views) - LOCKED
- "Adding Custom Wearables (clothing, armor, weapons)" - LOCKED  
- Other high-value art tutorials - LOCKED

## What's Accessible

### ServUO Tutorials Page Structure
98 tutorials in the Tutorials category, organized by prefix:
- **Art** - Sprite creation, wearables, animations
- **Code** - Scripting, systems
- **Audio** - Sound modding
- **Animations** - Custom animation implementation
- **Gumps** - UI elements
- **Maps** - Map tiling and terrain
- **Misc** - General guides

### Key Art Tutorials Identified (登录墙後面)

**Top Priority - Clothing & Wearables:**
1. **Adding Custom Wearables (clothing, armor, weapons)** by Safera  
   - Sep 24, 2021  
   - Covers: How to add new wearables using UOFiddler
   
2. **Creating UO sprites with Daz Studio and Blender** by Vrark  
   - Apr 1, 2023  
   - 5.00 stars, 3 ratings, 8,633 views
   - Tags: art, blender, daz studio, rendered sprites, sprites, tutorials
   - Workflow: Daz Studio → Blender → Fiddler
   - **FEATURED TUTORIAL**

**Animations:**
3. **How to add custom animations to UO** by Redmoon  
   - Sep 24, 2021  
   - 5.00 star rating
   
4. **My finished animations - combined** by Vrark  
   - Collection of finished animations
   
5. **Animated runestone** by Vrark  
   - Animated static runestone example

**Map Tiling:**
6. **Map Tiling - Deep Dive!** by Wilson  
   - Aug 2, 2025  
   - How map tiling is constructed

7. **New UOL Smooth Maps** by ParanoiaPhD  
   - Mar 20, 2024  
   - Quick map creation tool/tutorial

**Art Tools & Techniques:**
8. **BULKUO - The ultimate tool for batching uo art!** by ParanoiaPhD  
   - Sep 6, 2023  
   - Mass export/import of UO art

9. **Video Tutorial - Reverse Engineering Art** by otimpyre  
   - Feb 5, 2014  
   - Conversion of existing art to work with UO
   - 5.00 star rating

10. **Vrark's GIF tools**  
    - Tool for creating/processing .gif files for UO

## Tools Referenced

### UOFiddler
- GitHub: https://github.com/polserver/UOFiddler
- Description: View and alter almost every UO 2D client file
- Requirements: .NET Desktop Runtime 8.0.x (or .NET 7.0.x for older versions)
- Minimum: Windows 10
- License: Beerware
- Wiki: Minimal content (nearly empty)

### Other Tools Mentioned
- **Daz Studio** - 3D character/object creation
- **Blender** - 3D modeling and rendering
- **Centred** - UO development tool (Discord channel exists)
- **UOArchitect** - Map/world building
- **Fiddler** - The primary art import/export tool

## Next Steps

### Option 1: Register ServUO Account
Register at https://www.servuo.dev/register/ to access full tutorials. Account appears free.

### Option 2: Alternative Research Paths
1. Join ServUO Discord (662 members shown) - may have public channels with info
2. Check YouTube for "UOFiddler tutorial", "ServUO custom clothing", "UO sprite creation"
3. Look for archived RunUO forum content (RunUO was predecessor to ServUO)
4. Check POL Discord (mentioned in UOFiddler repo) for tool-specific guidance

### Option 3: Direct Documentation Dive
- Clone UOFiddler source and read code/comments
- Examine ServUO source for art-related classes and comments
- Reverse-engineer from existing UO art files

## Key Questions Still Unanswered

1. **File formats:** What exact format are UO sprites, animations, tiles?
2. **ID assignment:** How are new art IDs assigned without conflicts?
3. **Animation frames:** Frame count, timing, layer structure?
4. **Wearable layers:** How do clothing layers work with character paperdolls?
5. **Map tile structure:** Tile dimensions, z-layering, transitions?
6. **Client compatibility:** Do custom assets work with ClassicUO, official client, both?

## Recommendation

**Immediate:** Register a ServUO account to unlock the full tutorial library. The Vrark Daz→Blender workflow and Safera wearables guide are exactly what we need for clothing/item creation.

**Medium-term:** Join the ServUO Discord and POL Discord for real-time community support while implementing.
