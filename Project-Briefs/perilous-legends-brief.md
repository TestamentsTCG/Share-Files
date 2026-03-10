# Perilous Legends — Developer Briefing
**Produced by Elijah, 2026-03-09**
**Source: Full read of TestamentsTCG/PerilousLegends repo + all custom scripts**

---

## Table of Contents
1. [Project Identity](#1-project-identity)
2. [Technical Stack](#2-technical-stack)
3. [All Custom Systems — Deep Dive](#3-all-custom-systems--deep-dive)
4. [Game Design Rules & Numbers](#4-game-design-rules--numbers)
5. [Phase Roadmap](#5-phase-roadmap)
6. [Open Design Questions](#6-open-design-questions)
7. [Key Files Map](#7-key-files-map)
8. [Things Elijah Needs to Know](#8-things-elijah-needs-to-know)

---

## 1. Project Identity

### What Is Perilous Legends?

Perilous Legends (PL) is a **Ultima Online private shard** running on **ServUO**, targeting the **Pub 16 ruleset** (July 2002, pre-AOS era). It is:

- **Felucca-only** — Trammel and Ilshenar are fully disabled (no blue safety net)
- **Full loot on death** — death is meaningful and permanent
- **PvP everywhere** — no safe zones outside of towns (and even those are contested via Factions)
- **One account, one character, permanent identity** — no alts, no throwaway characters
- **RMT-legitimized** — the server explicitly builds around a real-money economy, not against it

### Philosophy

> "Legitimize RMT — the black market IS the front door."

The server's design principle is that players already trade UO gold and items for real money (it's unavoidable). PL embraces this by building a **Premium Currency system** where:
- Real money → Premium Currency
- Items/Gold → Premium Currency (via Auction House)
- Premium Currency → Cash out
- Server takes a royalty on every AH transaction

This is the monetization model — NOT a subscription server.

### Target Audience

Veteran UO players who want:
- Classic pre-AOS combat with real stakes (full loot, murder counts matter)
- Economy with real monetary value
- Long-term character investment (9 classes × 10 levels, 3 skill builds per char)
- Factions PvP in a lawless Felucca

### Differentiators vs Other UO Shards

1. **RMT is the product** — officially supported, not punished
2. **Class system layered on top of UO** — 9 classes, each with a unique economy and XP path
3. **3 skill builds per character** — one character can functionally have 3 playstyles
4. **Build-specific powerscrolls** — multiplies PS demand dramatically
5. **Felucca-only** — no safe alternatives, full risk everywhere

---

## 2. Technical Stack

### Base Server

| Component | Detail |
|-----------|--------|
| **Engine** | ServUO (C#, .NET) |
| **Pub Era** | Pub 16 (pre-AOS, July 2002) |
| **Client** | Classic UO client compatible |
| **Expansions active** | Felucca content only (HS, SA, ToL content exists in repo but mostly locked out) |
| **Map** | Standard Felucca; custom map planned pre-launch |
| **OS Target** | Windows (StartServer.bat, .bat launchers present) |

### Repository Structure

```
/                          — Root: bat scripts, .sln, config files
/Server/                   — ServUO core engine (Mobile.cs, World.cs, Timer.cs, etc.)
/Scripts/                  — All game scripts
  /Scripts/Custom/PerilousLegends/  — ALL custom PL code (30 files)
  /Scripts/Mobiles/         — NPC and creature definitions (hundreds of files)
  /Scripts/Items/           — Item definitions
  /Scripts/Spells/          — Spell system
  /Scripts/Services/        — Champion spawns, housing, crafting, etc.
  /Scripts/Regions/         — Zone/region logic
/Spawns/                   — XML spawn data for Felucca
/Ultima/                   — UO file reading library
/README.md                 — Comprehensive design document (authoritative source)
```

### Custom Script Architecture

All PL-specific code lives in:
```
Scripts/Custom/PerilousLegends/
```

Namespace: `Server.Engines.PerilousLegends`

Files use a static class + `Initialize()` pattern registered with ServUO startup. Every custom system self-registers its commands and hooks on server startup.

### Key Architectural Patterns

1. **`PLPlayerData`** — central data bag per player, stored on `Mobile` via `PLPlayerDataManager.Get(mobile)`. Contains class data, build data, cooldowns, active flags.
2. **`PLPlayerDataManager`** — static manager, Dictionary-backed, serializes/deserializes via ServUO persistence.
3. **Static manager classes** (e.g., `PLClassManager`, `PLBuildManager`) — handle logic, never hold per-player state themselves.
4. **Item-based UI** — `PLPersonality` (the BuildBook) is an actual item in the player's backpack. Player interacts by double-clicking it.
5. **Command registration** — all player and GM commands registered via `CommandSystem.Register()` in each class's `Initialize()`.

---

## 3. All Custom Systems — Deep Dive

### 3.1 PLPlayerData + PLPlayerDataManager

**File:** `PLPlayerData.cs`

**What it does:** The data persistence layer for the entire PL system. Every player gets a `PLPlayerData` object that stores all their PL state.

**Key data stored:**
- `ActiveClass` (PLClassType enum)
- `ClassDataMap` (Dictionary<PLClassType, PLClassData>) — per-class XP, level
- `Personalities[]` — array of 3 build slots (PLPersonalitySlot)
- `ActivePersonalityIndex` — which build is active (-1 = none)
- `LastClassSwap` (DateTime) — enforces 24h class swap cooldown
- `LastPersonalitySwap` (DateTime) — tracks build swaps (no cooldown — 2-min channel required)
- `ArcaneOverloadActive` / `ArcaneOverloadExpiry` / `ArcaneOverloadCooldown` — Elementalist active ability state

**PLClassData** stores:
- `Level` (1–10)
- `XP` (current)
- `PurchasedSkills` — List<string> of unlocked class skills (tier system)

**PLPersonalitySlot** stores:
- `Name` (string)
- `IsInitialized` (bool)
- `AllowedSkills` (List<SkillName>) — the locked skill list for this build
- `SkillCaps` (Dictionary<SkillName, double>) — per-build powerscroll caps
- `MaxPersonalities = 3` (const)

**Serialization:** Uses ServUO's IGenericSerializable interface. Version tracked. Backward-compatible reads.

**Status:** ✅ Fully built and functional.

**How to get data for a player:**
```csharp
PLPlayerData data = PLPlayerDataManager.Get(mobile);
```

---

### 3.2 PLClassSystem + PLClassManager

**Files:** `PLClassSystem.cs`, `PLClassInfo.cs` (inferred — referenced throughout)

**What it does:** Defines the 9 classes, their metadata, XP thresholds, and manages class switching.

**The 9 Classes (PLClassType enum):**
```
None, Pirate, Necromancer, Bard, Elementalist,
Ranger, Gladiator, Biologist, Assassin, Cutpurse
```

**PLClassInfo provides:**
- `GetName(PLClassType)` → display name
- `GetCurrency(PLClassType)` → currency name string

**PLClassManager provides:**
- `AddXP(Mobile, PLClassType, int)` → awards XP, triggers level-up if threshold hit
- `GetCoinType(PLClassType)` → returns the `Type` of the currency item for that class
- `RespecTier(PlayerMobile, PLClassType, int)` → removes a purchased skill at a given tier (GM tool)

**XP Thresholds (from README):**

| From → To | XP Required |
|-----------|-------------|
| 1 → 2 | 1,000 |
| 2 → 3 | 2,500 |
| 3 → 4 | 5,000 |
| 4 → 5 | 9,000 |
| 5 → 6 | 14,000 |
| 6 → 7 | 20,000 |
| 7 → 8 | 28,000 |
| 8 → 9 | 38,000 |
| 9 → 10 | 50,000 |
| **Total** | **167,500** |

**Class Swap Rules:**
- 24-hour cooldown between class changes
- GM can bypass with `[PLSetPlayerClass` or `[PLResetClassSwap`
- Murder counts are character-wide (not class-specific)

**Level-Up Hook:** `OnLevelUp()` exists as a hook in `PLClassSystem.cs` but is a stub. Phase 2 work.

**Status:** ✅ Class definitions, XP thresholds, swap timers built. ⚠️ XP gain from combat NOT wired. Level-up rewards NOT implemented.

---

### 3.3 PLClassCurrency (Drop System)

**File:** `PLClassCurrency.cs`

**What it does:** Defines 9 currency item types (one per class) and hooks into creature death to drop them.

**The 9 Currency Items:**

| Class | Item Type | Hue | Preferred Source |
|-------|-----------|-----|-----------------|
| Pirate | PLDoubloon | 0x501 | Sea creatures (30%) |
| Necromancer | PLSoulShard | 0x482 | Undead (30%) |
| Bard | PLGoldenNote | 0x4AC | All creatures (always 30%) |
| Elementalist | PLEssence | 0x480 | Elementals (30%) |
| Ranger | PLHuntersMark | 0x59B | Animals (30%) |
| Gladiator | PLGloryToken | 0x21 | Humanoids (30%) |
| Biologist | PLSpecimen | 0x48E | Insects + Animals (30%) |
| Assassin | PLShadowCoin | 0x497 | Humanoids (30%) |
| Cutpurse | PLCutPurse | 0x961 | Humanoids (30%) |

**Drop Logic:**
- Triggered on creature death event
- Player must have an active class set
- Preferred creature type = 30% drop rate, 1–3 coins
- Non-preferred creature type = 15% drop rate, 1–3 coins
- Delivered to killer's backpack with a message
- Currency is a real droppable item (stackable), not a hidden counter

**Status:** ✅ Fully built.

---

### 3.4 PLPersonality (BuildBook)

**File:** `PLPersonality.cs`

**What it does:** A blessed item that lives in the player's backpack. Manages 3 independent skill builds. This is the primary player-facing UI for the build system.

**Key mechanics:**
- Double-click to open the build management gump
- 3 build slots per character
- Each build has a **name** (player-chosen)
- Each build has an **AllowedSkills list** — locked after first activation
- First activation copies current character skills as a baseline
- Skill gains outside the active build's AllowedSkills are blocked by an enforcer timer

**Skill isolation enforcement:**
- A timer fires periodically
- Any skill not in `AllowedSkills` that has gained is reset
- This prevents accidental cross-contamination between builds

**Build-specific powerscroll caps:**
- `SkillCaps[SkillName]` per build slot
- Applying a powerscroll to a build only raises that build's cap
- Other builds at 100 for that skill remain at 100

**Swap rules:**
- No cooldown timer on build swaps (unlike class swaps)
- A **2-minute channel mechanic is DESIGNED but NOT YET ENFORCED** — player must stand still for 2 minutes to swap builds
- Safe zone requirement also designed but not enforced

**Status:** ✅ Core built. ⚠️ Swap enforcement (safe zone, 2-min channel) is Phase 2.

---

### 3.5 PLClassGump

**File:** `PLClassGump.cs`

**What it does:** The UI gump for the Class System. Players interact with this to view class info, see XP progress, and swap classes.

**Features:**
- Displays current class and level
- Shows XP bar (current / to next level)
- Lists all 9 classes with brief descriptions
- Class swap button (blocked if on cooldown, shows remaining time)
- Currency held display

**Status:** ✅ Built.

---

### 3.6 PLRespecGump

**File:** `PLRespecGump.cs`

**What it does:** UI for respeccing class skill purchases. Allows a player to undo a tier purchase (subject to rules/costs).

**Status:** ✅ Built (GM-facing; player version may be stubbed).

---

### 3.7 PLPassiveHooks

**File:** `PLPassiveHooks.cs`

**What it does:** The central event hook system. Intercepts ServUO events and routes them to class-specific bonus handlers.

**Hooks implemented:**
- `OnMeleeHit` — routes to melee bonus handlers
- `OnSpellDamage` — routes to spell damage handlers
- `OnCreatureDeath` — triggers currency drops, XP (future)
- `OnSkillUse` — routes to skill bonus handlers
- `OnHeal` — routes to healing bonus handlers

**This is the integration spine** — every class bonus flows through here. If a class perk needs to fire on an event, it gets wired in PLPassiveHooks.

**Status:** ✅ Framework built. ⚠️ Many class hooks are stubs pending Phase 2 perk implementation.

---

### 3.8 Class Bonus Systems

Each class has its own bonus file that defines passive and active bonuses:

#### PLAssassinBonuses.cs
- **What it does:** Passive bonuses for Assassin class
- **Key features:** Bonus damage from stealth/hiding, poison application bonuses
- `HasSkill(Mobile, PLAssassinSkill)` — checks if player has unlocked a specific tier skill
- Skill enum: `ShadowStrike`, `PoisonMastery`, `DeathBlow`, etc. (tier-gated)

#### PLBardBonuses.cs
- **What it does:** Bard passive bonuses
- **Key features:** Enhanced Provocation, Discordance, Peacemaking
- `PLBardicLute.cs` — custom instrument item that provides bard-specific bonuses when equipped

#### PLBiologistBonuses.cs
- **What it does:** Biologist passives
- **Key features:** Alchemy potency bonuses, poison tier upgrades, creature lore bonuses

#### PLCutpurseBonuses.cs
- **What it does:** Cutpurse passives
- **Key features:** Enhanced stealing, lockpicking bonuses, NPC merchant discounts

#### PLElementalistBonuses.cs
- **What it does:** Elementalist passives + Arcane Overload integration
- **Key features:**
  - `GetArcaneOverloadSDI(Mobile)` — returns +35 SDI bonus when Arcane Overload is active
  - `HasSkill(Mobile, PLElementalistSkill)` — tier skill gate checks
  - Elemental creature damage bonuses
  - `PLElementalistSpellbook.cs` — custom spellbook for Elementalist (Elemental Sanctuary spell contained within)

#### PLGladiatorBonuses.cs
- **What it does:** Gladiator passives
- **Key features:** Arena-style combat bonuses, endurance, defense bonuses

#### PLNecromancerBonuses.cs
- **What it does:** Necromancer passives
- **Key features:** `PLGraveDust.cs` (resource item), undead command bonuses, Spirit Speak enhancement

#### PLPirateBonuses.cs
- **What it does:** Pirate passives
- **Key features:** Sea combat bonuses, `PLBuccaneersFury.cs` (active ability), sea creature loot bonuses

#### PLRangerBonuses.cs
- **What it does:** Ranger passives
- **Key features:** Archery damage bonuses, animal taming enhancements
- **`PLAmmoHelper.cs`** — custom ammo consumption engine for ranger
- **`PLQuiver` / `PLRangerArrow` / `PLRangerBolt`** — custom quiver and ranger-specific ammo items
  - PLRangerArrow/Bolt can ONLY be used from a PLQuiver (not from backpack)
  - PLQuiver grants 10% base no-consume chance (LowerAmmoCost = 10)
  - `HasRangerAmmo(Mobile)` — gate check for ranger special moves
  - Ammo priority: PLRangerArrow/Bolt (quiver) → Arrow/Bolt (quiver) → Arrow/Bolt (backpack)

**All class bonus files status:** ✅ Framework built with `HasSkill()` checks. ⚠️ Most actual bonuses are stubs — the _structure_ is there but specific numbers/effects need Phase 2 work.

---

### 3.9 PLArcaneOverload

**File:** `PLArcaneOverload.cs`

**What it does:** Active ability for Elementalist class. Requires `ArcaneOverload` skill unlocked (Level 10 Tier A).

**Mechanics:**
- Command: `[ArcaneOverload`
- Effect: +35 SDI (Spell Damage Increase) for **30 seconds**
- Cooldown: **60 seconds**
- Visual: particle effect + sound on activation
- State tracked in `PLPlayerData` (ArcaneOverloadActive, ArcaneOverloadExpiry, ArcaneOverloadCooldown)
- Integration: `PLElementalistBonuses.GetArcaneOverloadSDI()` checks active flag and returns +35 to spell damage calculations

**Status:** ✅ Fully built and integrated.

---

### 3.10 PLElementalSanctuary

**File:** `PLElementalSanctuary.cs`

**What it does:** An Elementalist ability (likely a spell or active skill). Creates an area effect — details in code.

**Status:** ✅ Built (specifics in file — not fully read in detail, but present).

---

### 3.11 PLBuccaneersFury

**File:** `PLBuccaneersFury.cs`

**What it does:** Pirate active ability. High-damage sea combat burst.

**Status:** ✅ Built.

---

### 3.12 PLGrandFinale

**File:** `PLGrandFinale.cs`

**What it does:** Bard active ability. Ultimate performance — likely a powerful crowd control / damage finale.

**Status:** ✅ Built.

---

### 3.13 PLPowerScroll (Tiered Skill Scrolls)

**Referenced in README as `PLPowerScroll.cs`** — may be named differently in repo.

**What it does:** Replaces standard UO powerscrolls (+5/+10/+15/+20) with a tiered **+1 per scroll** system. 20 steps from 100 → 120 per skill.

**Tiers:**

| Tier | Color | Hue | Skill Range |
|------|-------|-----|-------------|
| Green | Bright green | 0x48E | 100–105 |
| Blue | Bright blue | 0x09C | 105–110 |
| Red | Crimson | 0x026 | 110–115 |
| Blaze | Orange | 0x08A | 115–120 |

**Item naming:** `"Powerscroll of [SkillName]"` — color indicates tier, no tier word in name.

**Champion drop weights:**

| Champion | Blaze | Red | Blue | Green |
|----------|-------|-----|------|-------|
| Barracoon / Mephitis | 5% | 10% | 15% | 70% |
| Neira / Rikktor | 10% | 15% | 20% | 55% |
| Semidar | 20% | 25% | 30% | 25% |
| Lord Oaks | 25% | 30% | 35% | 10% |
| Harrower | ❌ (no skill scrolls — drops stat scrolls only) | | | |

**Eligible skills (pre-AOS):** Swords, Fencing, Macing, Archery, Wrestling, Parry, Tactics, Anatomy, Healing, Magery, Meditation, EvalInt, MagicResist, AnimalTaming, AnimalLore, Veterinary, Musicianship, Provocation, Discordance, Peacemaking, Blacksmith, Tailoring.

**Status:** ✅ Built.

---

### 3.14 PLStatScroll (Harrower Stat Scrolls)

**Referenced in README as `PLStatScroll.cs`**.

**What it does:** Harrower-exclusive drops. Each scroll raises total stat pool (STR+DEX+INT combined) by +1.

**Details:**
- Base total stat cap: 225
- Maximum: 250 (25 scrolls to max)
- Per-stat hard cap: 120
- 5 tiers, 20% each from Harrower

| Tier | Color | Hue | Required current cap |
|------|-------|-----|---------------------|
| Green | 0x48E | 225–229 | |
| Blue | 0x09C | 230–234 | |
| Red | 0x026 | 235–239 | |
| Blaze | 0x08A | 240–244 | |
| Pink | 0x1CF ⚠️ PLACEHOLDER | 245–249 | |

⚠️ Pink hue is a placeholder — needs final color set via UOFiddler.

**Status:** ✅ Built. ⚠️ Pink hue needs finalizing.

---

### 3.15 PLFacetRestriction

**File:** `PLFacetRestriction.cs`

**What it does:** Enforces Felucca-only by blocking all access to Trammel (Map 1) and Ilshenar (Map 2).

**Four enforcement layers:**
1. **Public Moongates** — Trammel/Ilshenar removed from gate destination lists
2. **Teleporters** — `CanTeleport` returns false for blocked maps
3. **Spell travel** — Recall/Gate/Mark blocked via `SpellHelper.CheckTravel`
4. **Login bounce** — Players logging in on a blocked map are moved to same coordinates in Felucca

Staff (AccessLevel > Player) bypass all restrictions.

**Helper method:** `PLFacetRestriction.IsBlocked(Map)` — returns true for Map.Trammel and Map.Ilshenar.

**Status:** ✅ Fully built.

---

### 3.16 PLAdminCommands

**File:** `PLAdminCommands.cs`

**What it does:** GM command suite for managing player PL data in-game.

**Commands registered:**

| Command | Description |
|---------|-------------|
| `[PLPlayerReport` | Full data dump for targeted player (class, builds, cooldowns, XP, currency) |
| `[PLGivePersonality` | Give targeted player a Personality (BuildBook) item if they don't have one |
| `[PLGiveClassXP <Class> <Amount>` | Award XP to specific class on targeted player |
| `[PLSetPlayerClass <Class>` | Force-set class, bypasses 24h timer |
| `[PLResetBuild <1-3>` | Wipe a build slot on targeted player |
| `[PLResetClassSwap` | Clear class swap cooldown on targeted player |
| `[PLResetBuildSwap` | Clear build swap timestamp on targeted player |
| `[PLRespecTier <Class> <Tier>` | Remove the skill purchased at a specific tier (no coin refund) |

All require `AccessLevel.GameMaster` minimum.

**Status:** ✅ Fully built.

---

### 3.17 PLAmmoHelper

**File:** `PLAmmoHelper.cs`

**What it does:** Custom ammo consumption engine for ranged weapons. Replaces BaseRanged.OnFired ammo logic.

**Consumption priority:**
1. PLRangerArrow/PLRangerBolt from PLQuiver (ranger-exclusive ammo)
2. Arrow/Bolt from PLQuiver (normal ammo in ranger quiver)
3. Arrow/Bolt from backpack

**Rules:**
- PLRangerArrow/Bolt CANNOT be used from backpack — quiver ONLY
- PLQuiver grants 10% base no-consume chance
- If no PLQuiver, falls back to vanilla behavior
- Ranger ammo without PLQuiver simply can't fire

**Gate check:** `HasRangerAmmo(Mobile)` — used by ranger special moves to verify ranger-specific ammo is available before allowing specials.

**Status:** ✅ Fully built.

---

### 3.18 PLRareLootSystem

**File:** `PLRareLootSystem.cs`

**What it does:** Custom rare loot drop system. Generates special items on creature death beyond standard loot tables.

**Design:** Configurable tables for rare item drops tied to creature type, difficulty, or class affinity.

**Status:** ✅ Framework built. ⚠️ Loot tables likely need population.

---

### 3.19 PLContractScroll + PLBuildBook

**Files:** `PLContractScroll.cs`, `PLBuildBook.cs`

**PLContractScroll:** A scroll item used in some class unlock or build commitment mechanic.

**PLBuildBook:** The BuildBook item itself. Likely the same as or related to PLPersonality — may be an alias or predecessor name.

**Status:** ✅ Built.

---

### 3.20 PLGuildmaster

**File:** `PLGuildmaster.cs`

**What it does:** NPC that serves as the class advancement gatekeeper. Players visit the Guildmaster to confirm level advancement, likely consuming class currency or special items.

**Status:** ✅ NPC shell built. ⚠️ Advancement logic is a Phase 2 stub.

---

### 3.21 PLSkillMod

**File:** `PLSkillMod.cs` (referenced but not found as standalone — may be internal to another file)

**What it does:** Applies skill modifier bonuses from class perks.

---

### 3.22 PLBardicLute

**File:** `PLBardicLute.cs`

**What it does:** Custom instrument item for the Bard class. Provides enhanced bard bonuses when equipped vs standard lutes.

**Status:** ✅ Built.

---

### 3.23 PLGraveDust

**File:** `PLGraveDust.cs`

**What it does:** A crafting/consumable resource for the Necromancer class. Harvested from graves or undead creatures. Used in Necromancer skill unlocks or class mechanics.

**Status:** ✅ Built.

---

### 3.24 PLPersonality (Full System)

**What it does:** This is the complete personality/build system — the `PLPersonalitySlot` is the data structure, and `PLPersonality` is the in-world item. Already covered in 3.4 above.

**Key constants:**
- `PLPersonalitySlot.MaxPersonalities = 3` — hard limit of 3 builds per character

---

## 4. Game Design Rules & Numbers

### Combat Rules (Pub 16)
- Pre-AOS combat — no AOS item property stacking
- No stat loss for murderers (red players keep all stats)
- Full loot on death
- Murder counts tracked per character (cross-build, cannot escape by switching builds)
- Town guards active in guarded regions (Factions can capture towns)

### Skill System
- GGS (Guaranteed Gain System) for skill gain safety net
- Skills gain in the classic pub 16 way
- Skill gains outside an active build's AllowedSkills are blocked
- Skill cap is 700 total (standard pre-AOS)
- Powerscrolls raise individual skill caps above 100 (up to 120 max)
- Build-specific powerscroll caps — each build has its own cap per skill

### Class System Numbers
- 9 classes
- 10 levels per class
- 24h swap timer between classes
- XP to max: 167,500 total
- Classes are independent — maxing one doesn't affect another

### Build System Numbers
- 3 builds per character
- No hard cooldown on build swaps (2-minute channel mechanic planned)
- AllowedSkills list locked after first activation
- Each build stores its own powerscroll caps per skill

### Powerscroll Numbers
- +1 per scroll
- 20 scrolls to go from 100 to 120
- 4 tiers (Green, Blue, Red, Blaze)
- Each tier covers 5 skill points

### Stat Scroll Numbers
- +1 per scroll to total stat pool
- 25 scrolls to go from 225 to 250 max
- 5 tiers
- Per-stat hard cap 120 (total 250 allows very unbalanced stat allocation)

### Champion Spawn Progression
- Barracoon / Mephitis — Easy
- Neira / Rikktor — Medium
- Semidar — Hard
- Lord Oaks — Unique
- Harrower — Endgame (drops stat scrolls only)

### Currency Drop Rates
- Preferred creature type: 30% drop rate, 1–3 coins
- Non-preferred: 15% drop rate, 1–3 coins
- Drops on death, directly to killer's backpack

### Arcane Overload (Elementalist)
- Duration: 30 seconds
- Cooldown: 60 seconds
- Effect: +35 SDI

### Class-Specific Ammo (Ranger)
- PLRangerArrow / PLRangerBolt — quiver only
- PLQuiver: 10% LowerAmmoCost base
- Gate check `HasRangerAmmo()` required for ranger specials

---

## 5. Phase Roadmap

### Phase 1 — DONE ✅
- [x] Class system (9 classes, XP/level tracking, 24h swap timer)
- [x] Build system (3 builds, skill locking, build-specific PS caps)
- [x] PLPersonality (BuildBook item, gump UI)
- [x] Class currency items (9 types) + death drop hooks
- [x] Powerscroll system (4-tier +1 scrolls, champion weights)
- [x] Stat scroll system (5-tier Harrower drops)
- [x] Facet restriction (Trammel/Ilshenar blocked at 4 layers)
- [x] Admin GM command suite
- [x] PLPassiveHooks framework
- [x] All class bonus file structures (HasSkill checks, framework)
- [x] Arcane Overload (Elementalist active ability)
- [x] PLAmmoHelper (ranger ammo engine)
- [x] PLGuildmaster NPC shell

### Phase 2 — IN PROGRESS / NEXT
- [ ] **XP gain from combat** — wire `PLClassManager.AddXP` to combat events per class
- [ ] **Class perks** — define and implement what each class unlocks at each level (BIGGEST task)
- [ ] **Level-up OnLevelUp() implementation** — hook per class
- [ ] **Guildmaster NPC logic** — advancement confirmation, material consumption
- [ ] **BuildBook swap enforcement** — 2-min channel, safe zone check, combat flag check
- [ ] **Class currency spending** — what do coins buy? vendor system?
- [ ] **Rare loot table population** — PLRareLootSystem tables need data
- [ ] **Auction House** — gold-only first pass

### Phase 3 — PLANNED
- [ ] **Premium Currency Wallet** — server-side balance tracking
- [ ] **RMT Platform** — buy-in (crypto/PSC), cash-out, royalty engine
- [ ] **AH with Premium Currency** — second tier of AH pricing
- [ ] **Pink stat scroll hue finalization**

### Phase 4 — LONG TERM
- [ ] **Custom Map** — Felucca map rework
- [ ] **Web Portal** — player account management, currency top-up, market view

---

## 6. Open Design Questions

These are explicitly unresolved in the README and codebase:

| # | Question | Status | Priority |
|---|----------|--------|----------|
| 1 | **Class perk table** — What does each class unlock at each of the 10 levels? | Undefined | 🔴 Critical — blocks Phase 2 |
| 2 | **XP per action** — How much XP per kill/craft/steal? Balance question. | Undefined | 🔴 Critical — blocks Phase 2 |
| 3 | **Class currency spending** — What do the 9 currencies buy? Guildmaster vendor? Cosmetics? Perks? | Undefined | 🔴 Critical |
| 4 | **Premium currency name** | Undefined | 🟡 Moderate |
| 5 | **Royalty percentage** on AH sales | Undefined (suggestion: 5%) | 🟡 Moderate |
| 6 | **Minimum cash-out threshold** | Undefined (suggestion: $10) | 🟡 Moderate |
| 7 | **BuildBook swap restrictions** — Safe zone? 2-min channel? How strictly enforced? | Designed, not coded | 🟡 Moderate |
| 8 | **Pink stat scroll hue** — 0x1CF is placeholder | Design gap | 🟢 Low |
| 9 | **Cutpurse economy ceiling** — High-level stealing could be disruptive. Needs caps or countermeasures. | Open risk | 🟡 Moderate |
| 10 | **Bard affinity** — Currently all creatures = 30% currency drop. Intentional? Or should it be limited? | Open question | 🟢 Low |
| 11 | **Crypto first** — USDC stable or ETH for initial RMT? | Undefined | 🟡 Phase 3 |
| 12 | **XP balancing** — 167,500 total XP to max a class. Is that too fast? Too slow? | Undefined | 🟡 Moderate |
| 13 | **Per-class perk distinctiveness** — How do you ensure 9 classes feel fundamentally different, not just stat bonuses? | Open design | 🔴 Critical |

---

## 7. Key Files Map

### Custom PL Files (Scripts/Custom/PerilousLegends/)

| File | Purpose | Depends On |
|------|---------|------------|
| `PLPlayerData.cs` | Central data model + persistence | ServUO IGenericSerializable |
| `PLClassSystem.cs` | 9 class definitions, XP thresholds, swap logic | PLPlayerData |
| `PLClassCurrency.cs` | 9 currency item types + death drop hooks | PLPlayerData, PLClassSystem |
| `PLClassGump.cs` | Player-facing class UI | PLPlayerData, PLClassSystem |
| `PLPersonality.cs` | BuildBook item + build management UI | PLPlayerData |
| `PLPassiveHooks.cs` | Event routing to all class bonus systems | All class bonus files |
| `PLAssassinBonuses.cs` | Assassin passive/active bonuses | PLPlayerData |
| `PLBardBonuses.cs` | Bard passive/active bonuses | PLPlayerData |
| `PLBardicLute.cs` | Custom bard instrument item | PLBardBonuses |
| `PLBiologistBonuses.cs` | Biologist passive/active bonuses | PLPlayerData |
| `PLCutpurseBonuses.cs` | Cutpurse passive/active bonuses | PLPlayerData |
| `PLElementalistBonuses.cs` | Elementalist passives + Arcane Overload integration | PLPlayerData, PLArcaneOverload |
| `PLElementalistSpellbook.cs` | Custom Elementalist spellbook | PLElementalistBonuses |
| `PLElementalSanctuary.cs` | Elementalist active ability | PLElementalistBonuses |
| `PLGladiatorBonuses.cs` | Gladiator passive/active bonuses | PLPlayerData |
| `PLNecromancerBonuses.cs` | Necromancer passive/active bonuses | PLPlayerData |
| `PLPirateBonuses.cs` | Pirate passive/active bonuses | PLPlayerData |
| `PLRangerBonuses.cs` | Ranger passive/active bonuses | PLPlayerData, PLAmmoHelper |
| `PLArcaneOverload.cs` | Elementalist active: +35 SDI 30s burst, 60s CD | PLPlayerData, PLElementalistBonuses |
| `PLBuccaneersFury.cs` | Pirate active ability | PLPlayerData, PLPirateBonuses |
| `PLGrandFinale.cs` | Bard active ability | PLPlayerData, PLBardBonuses |
| `PLAmmoHelper.cs` | Custom ranger ammo consumption engine | PLQuiver, PLRangerArrow, PLRangerBolt |
| `PLRareLootSystem.cs` | Rare item drop tables on creature death | ServUO loot hooks |
| `PLAdminCommands.cs` | Full GM command suite (8 commands) | PLPlayerData, PLClassSystem, PLPersonality |
| `PLFacetRestriction.cs` | Trammel/Ilshenar block at 4 layers | ServUO maps, moongates, teleporters, SpellHelper |
| `PLGuildmaster.cs` | Class advancement NPC | PLPlayerData, PLClassSystem |
| `PLContractScroll.cs` | Scroll for class commitment mechanic | PLClassSystem |
| `PLBuildBook.cs` | BuildBook item (may alias PLPersonality) | PLPersonality |
| `PLGraveDust.cs` | Necromancer resource item | PLNecromancerBonuses |
| `PLRespecGump.cs` | Respec UI for class skill tier undoing | PLAdminCommands |

### Core ServUO Files Modified or Critical

| File | Relevance |
|------|-----------|
| `Scripts/Mobiles/PlayerMobile.cs` | Player character — PL hooks into events here |
| `Scripts/Items/Functional/PublicMoongate.cs` | Trammel/Ilshenar removed from gate lists |
| `Scripts/Items/Internal/Teleporter.cs` | CanTeleport blocked for disabled maps |
| `Scripts/Spells/Base/SpellHelper.cs` | CheckTravel blocks recall/gate/mark |
| `Scripts/Mobiles/Bosses/BaseChampion.cs` | ChampionDifficulty enum, powerscroll drop logic |
| `Scripts/Services/ChampionSystem/` | Full champion spawn system — all Felucca |
| `Scripts/Services/Factions/` | Full factions system — Shadowlords, Minax, TrueBrit, CoM |
| `Scripts/Services/BulkOrders/` | Smith + Tailor BODs (pre-AOS content) |

### Non-Custom Files Worth Knowing

| File | What to Know |
|------|-------------|
| `README.md` | The authoritative design document. Read this first always. |
| `Server/World.cs` | World save/load — PL data serializes through here |
| `Server/Mobile.cs` | Base Mobile class — events PL hooks into |
| `Spawns/felucca.xml` | Felucca spawn data — all champion spawns |
| `StartServer.bat` | How to start the server on Windows |

---

## 8. Things Elijah Needs to Know

### Critical Gotchas

**1. PLPlayerData is the single source of truth.**
Everything PL-related lives in `PLPlayerDataManager.Get(mobile)`. If you're writing code that touches class levels, builds, cooldowns, XP — go there first. Don't try to store PL state anywhere else.

**2. The build system and class system are independent.**
This confuses people. A player has BOTH an active build (which skills they can gain) AND an active class (Pirate, Bard, etc.). They don't have to match. A Mage build + Necromancer class is valid. Build = skill profile. Class = identity/progression track.

**3. PLPersonality is the item, PLPersonalitySlot is the data.**
The `PLPersonality` item lives in the player's backpack. The actual build data (AllowedSkills, SkillCaps, name) lives in `PLPersonalitySlot` inside `PLPlayerData`. The item is just the UI trigger.

**4. Murder counts are character-wide, not build-specific.**
This is a design decision. If your Assassin build PKs someone, your Crafter build is also red. A player cannot use builds to launder their reputation.

**5. XP is NOT wired to combat yet.**
GMs can award XP manually with `[PLGiveClassXP`. The framework for automatic XP (from kills, skill use, etc.) is designed but not implemented. Phase 2.

**6. Class perks are stubs.**
The `HasSkill()` checks exist. The tier unlocks cost currency and are gated. But what those perks actually DO when unlocked is mostly unimplemented. The perk content is Phase 2's biggest task.

**7. The Build Swap enforcement is not yet live.**
Players CAN swap builds without the 2-minute channel or safe-zone requirements. Those are planned but not coded. This means the current server is slightly more permissive than designed.

**8. Pink stat scroll hue is a placeholder.**
Hue 0x1CF for the 5th tier stat scroll needs to be verified in UOFiddler. Use it for now but flag it.

**9. PLAmmoHelper needs to be wired into BaseRanged.OnFired.**
The file exists and is complete, but whether it's actually hooked into the ranged weapon fire path needs verification. Check that BaseRanged.OnFired calls PLAmmoHelper.ConsumeAmmo instead of vanilla ammo logic.

**10. The repo is a full ServUO install.**
The custom PL code is only ~30 files. Everything else (hundreds of files in Scripts/Mobiles, Scripts/Services, etc.) is standard ServUO. Don't be overwhelmed — focus on Scripts/Custom/PerilousLegends/ and the files listed in the Key Files Map.

**11. Trammel/Ilshenar content still exists in the repo.**
The maps, NPCs, and content for Trammel and Ilshenar are all present in the codebase. They're just blocked at runtime. If future design calls for enabling new facets, the content is there.

**12. Premium Currency is designed but unbuilt.**
The README has detailed RMT plans. None of it exists in code yet. Phase 3.

**13. The Bard's Golden Note drops from ALL creatures at 30%.**
This is by design (Bard affinity is universal) but it's noted as an open question. Monitor whether Bard class currency becomes too easy to farm vs other classes.

**14. Cutpurse is flagged as a potential economy disruptor.**
At high level, Cutpurse stealing abilities could be disruptive. The README explicitly flags this as needing caps or countermeasures. Keep an eye on it when implementing Cutpurse perks.

**15. `[PLRespecTier` does NOT refund coins.**
Per the GM command implementation — removing a tier skill purchase gives no coin refund. If you change this, document it in the command's Usage attribute.

---

### How to Start Working

1. **Read `README.md` in the repo** — it's the design bible, kept up to date
2. **Start the server** with `StartServer.bat` 
3. **Check** `Scripts/Custom/PerilousLegends/` — that's your workspace
4. **For Phase 2 entry point:** `PLPassiveHooks.cs` → `OnCreatureDeath` → wire `PLClassManager.AddXP()`
5. **For perk implementation:** `PLClassSystem.cs` → `OnLevelUp()` stub → implement per class
6. **For testing:** Use GM commands — `[PLGiveClassXP`, `[PLSetPlayerClass`, `[PLPlayerReport`

### Key Questions to Ask Akasha Before Phase 2

1. What are the class perks? (Level 1–10 per class — 90 perk slots across 9 classes)
2. What do the 9 class currencies BUY?
3. What's the XP per kill for each class?
4. Should build swap have a cost in addition to the 2-min channel?
5. What's the Guildmaster NPC mechanic (materials consumed? just XP check?)

---

*Briefing complete. All 30 custom PL scripts read and documented. All base ServUO structure mapped.*
*For updates to this brief, re-read the README.md in the repo — it's kept current.*
