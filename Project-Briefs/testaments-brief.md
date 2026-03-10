# Testaments TCG — Project Briefing
*Compiled by Elijah | Source: TestamentsTCG/Testaments GitHub repo | Date: 2026-03-09*
*Every file in the repo was read. This is a production briefing.*

---

## TABLE OF CONTENTS
1. Project Identity
2. Game Mechanics — Full Rules
3. Card System — Types, Stats, Data Format
4. Launch Set: Moses vs Pharaoh — Complete Card Reference
5. David Set — What Exists
6. Future Heroes & Enemies
7. Art Direction — Visual System
8. Technical — Unity Implementation
9. Design Philosophy
10. Simulation Results — Balance Data
11. Current Status
12. Open Questions
13. Key Files Map
14. Things Elijah Needs to Know

---

## 1. PROJECT IDENTITY

**Name:** Testaments TCG
**Tagline:** A Biblical Digital Trading Card Game
**Genre:** 1v1 Competitive Digital Trading Card Game
**Platform:** Mobile-first (iOS App Store + Google Play Store)
**Engine:** Unity (LTS)
**Lead Designer:** Akasha
**Technical Lead:** Enoch
**No blockchain elements** — pure mobile game
**GDD Version:** 0.6 (Pre-production)
**Status:** Pre-production — game design and art direction phase

### Core Concept
One player embodies a Biblical Hero Avatar (e.g., Moses) racing to complete a 4-stage Prophecy. The other player is the adversarial force (e.g., Pharaoh) trying to corrupt, delay, and prevent the Hero from completing their destiny.

**Victory is not through elimination. It is through narrative completion.**

### Target Audience
- Fans of MTG, Hearthstone, Legends of Runeterra
- Christian/Biblical audience (faith-based market)
- Players who want spiritual/thematic depth in their games
- Mobile TCG players

### Differentiators
- **Biblical narrative structure** as the win condition (Prophecy system)
- **No life totals** — objective-based victory
- **Asymmetric factions** with mirrored thematic terminology (Faith/Dominion, Prayer/Ritual, Sanctuary/Stronghold)
- **12-round hard cap** creates genuine timer pressure
- **Persistent resources** that don't reset between turns
- **Morale as burst mechanic** (temporary resource, always spent first)
- **Respectful narrative** — no parody, not doctrinally prescriptive
- **Launch set** uses the Moses vs Pharaoh story — universally recognized

---

## 2. GAME MECHANICS — FULL RULES

*(Source: GDD.md + Rules Canon v1.0 — chatgpt-exports/02)*

### Win Conditions
- **Hero wins:** Complete Prophecy Stage IV at any time
- **Enemy wins:** Prevent Stage IV completion through end of Round 12

### Game Length
Maximum **12 Rounds**. One Round = one Hero turn + one Enemy turn.

### Resource Systems

#### Faith (Hero) / Dominion (Enemy)
- Function identically — only thematically different names
- **Persistent:** does NOT reset at end of turn
- Baseline generation: +1 per turn (Start Phase)
- **Max non-Morale generation per turn: 7**
- **Max stored persistent resource: 15**
- Cannot go below 0

#### Morale (Temporary Resource)
- Added to total resource pool
- Always spent **before** persistent resource
- No generation cap, no storage cap
- **Expires at End of Turn**
- Display: Yellow when Morale included, White when persistent only
- Does NOT count toward the 7/turn or 15-storage caps

### Turn Structure
1. **Start Phase** — Refresh Formation (all units become In Formation) + generate +1 Faith/Dominion
2. **Tithe Phase** — Resolve all "At the start of your turn" effects (Sanctuaries, Relics, Covenants, Curses, Avatar Passive)
3. **Draw Phase** — Draw 2 cards
4. **Main Phase** — Play Units/Relics/Sanctuaries/Covenants/Prayers, activate ONE Avatar ability, declare attacks, play Interventions (in any order)
5. **Discard Phase** — Discard down to 7 cards
6. **End of Turn** — Morale expires, end-of-turn effects resolve

### Starting Hand & First Player
- Starting hand size: 5 cards each
- First player: Dice roll (simulations use coin flip)
- **Going-second bonus:** The player who goes second draws 1 additional card (6 cards total). [NOTE: original design was +2/7 cards; changed to +1/6 during balance testing — not yet confirmed by Akasha]

### Deck Construction
- **Deck size:** 45 cards
- **Copy limit:** Max 3 of any non-Unique card
- **Unique cards:** Max 1 copy per deck
- **Sanctuaries/Strongholds:** All are Unique; max 1 copy of each per deck
- **Card pools:** Generic Hero pool + Avatar-specific locked pool (Hero decks only); Generic Enemy pool + Enemy-specific locked pool (Enemy decks only)

### Formation System
- **In Formation:** Began turn under your control OR has Zealot. Can attack.
- **Out of Formation:** Entered play this turn without Zealot, OR already attacked this turn. Cannot attack.
- **Zealot keyword:** Unit enters play In Formation (Haste equivalent)
- Formation resets at Start Phase

### Combat System
- Attacker chooses target — **no blocking step**
- If defender controls Units → only Units can be targeted
- If no Units → can attack Avatar or Relics
- Sanctuaries/Strongholds **cannot be attacked**
- Damage is simultaneous (default)
- **Damage persists between turns** (critical — units do NOT heal between rounds)
- **Ranged:** Ranged unit deals damage first; if target would die, target doesn't deal damage back

### Avatar Damage
- Avatar does NOT deal damage back when attacked
- Damage dealt to Avatar reduces defending player's **persistent** Faith/Dominion by that amount
- Morale cannot be removed this way
- Resource cannot go below 0; excess damage ignored

### Relic Rules
- May be attacked only if defending player controls no Units
- Do not deal damage back (unless stated)
- To destroy a Relic: deal damage equal to its **cost** in a **single turn**
- **Relic damage does NOT persist between turns** (exception to normal damage persistence)
- Destroyed Relics go to Crypt

### Sanctuary / Stronghold Rules
- Cannot be attacked
- Destroyed only by card effects
- Max **1** played per turn
- Max **2** in play simultaneously
- Effects begin **next turn** (delayed activation)
- If a third would enter, choose one to destroy

### Prophecy System
- Each Hero has ONE Prophecy card with 4 sequential stages (I → IV)
- To advance a stage: 0 Corruption + pay Faith cost + meet any additional requirement
- **Corruption:** No cap; blocks advancement; does NOT auto-lose
- Corruption does not reset between stages (must be 0 to advance)
- Stage advancement is attempted during Main Phase; costs are paid instantly and cannot be interrupted

### Stack & Timing
- Only **Interventions** use the stack
- Costs are paid instantly and cannot be interrupted, prevented, or refunded
- Only **effects** can be responded to with Interventions
- Stack resolves Last-In, First-Out
- Interventions may only be played during Main Phases

### Crypt
The discard pile. Destroyed and discarded cards go here.

### Simultaneous Win Condition Rule
If Stage IV completes on the same moment Round 12 ends, the active player's condition resolves first (Moses wins).

---

## 3. CARD SYSTEM

### Card Types

| Type | Faction | Description |
|------|---------|-------------|
| **Unit** | Both | Attack and defend. Power/Endurance stats. |
| **Relic** | Both | Persistent artifacts. All Unique by card type (not printed). Attackable under specific conditions. |
| **Sanctuary** | Hero | Horizontal location; cannot be attacked. All Unique. |
| **Stronghold** | Enemy | Mirror of Sanctuary. All Unique. |
| **Prayer** | Hero | Sorcery-speed spell (Main Phase only). |
| **Ritual** | Enemy | Mirror of Prayer. |
| **Covenant** | Hero | Persistent enchantment-style card. Horizontal. Not attackable. |
| **Curse** | Enemy | Mirror of Covenant. |
| **Intervention** | Both | Instant-speed response card. Uses the stack. |
| **Avatar** | Both | Starts in play. Not played from hand. Loyalty Counter system. |
| **Prophecy** | Hero | 4-stage win condition card. Starts in play. |

### Faction Terminology Mirror (Thematically distinct, mechanically identical)

| Hero Term | Enemy Term |
|-----------|------------|
| Faith | Dominion |
| Sanctuary | Stronghold |
| Prayer | Ritual |
| Covenant | Curse |

### Card Stats
- **Units:** Cost (Faith/Dominion), Power (attack), Endurance (health)
- **Avatars:** Loyalty Counter system (+1, -1/-2/-3, -5 abilities), Passive ability
- **Sanctuaries/Strongholds:** No cost (played for free — rules not explicit, may need clarification)
- **Prayers/Rituals/Interventions:** Cost (Faith/Dominion), effect text
- **Relics:** Cost (Faith/Dominion), persistent effect text
- **Covenants/Curses:** Cost (Faith/Dominion), ongoing effect text

### Unique Rule
Unique = represents a named person, named place, or named singular item.
- Max 1 copy per deck
- Max 1 in play under your control at a time (replacement rule: new copy replaces old, old is destroyed)
- Both players may each control one copy of the same Unique simultaneously
- **All Sanctuaries/Strongholds are Unique by default**
- **All Relics are Unique by card type** (not printed on card)
- Martyr does NOT trigger from Unique replacement (not "destruction")

### JSON Data Format (from moses-set.json)
```json
{
  "id": "hero-unit-001",
  "name": "Levite Guardian",
  "faction": "hero",
  "type": "unit",
  "cost": 2,
  "resource": "faith",
  "power": 1,
  "endurance": 3,
  "keywords": [],
  "text": "...",
  "flavor": "...",
  "artStatus": "illustrated",
  "unique": false
}
```
Avatars additionally have: `loyaltySystem: true`, `passive`, `abilities[]`

---

## 4. LAUNCH SET: MOSES vs PHARAOH — COMPLETE CARD REFERENCE

*Source: cards/data/moses-set.md and moses-set.json*
*All 10 Unit cards illustrated. All 9+9 Prayer/Ritual cards illustrated. Avatars illustrated.*
*Relics NOT YET illustrated (0/5 Moses, 0/4 Pharaoh).*

> **ACTIVE BALANCE TEST (as of 2026-03-04, NOT yet confirmed by Akasha)**
> - Let My People Go: Remove 1 Corruption / Draw 2 Cards (was: Remove 2 / Draw 1)
> - I AM WHO I AM: 5 Faith (was 4)
> - Blessed Spring: Cap 2 Corruption/turn (was 1)
> - Prophecy Stage III: Enemy controls 0 Units (was 0 or 1)
> - Pithom: Add 2 Corruption flat (was: 1 + conditional 1)
> - High Overseer: 4 Dominion (was 5)
> - Hardened Heart: 3 Dominion (was 4)
> - Pharaoh Avatar -3: Add 2 Corruption (was 1)
> - Going-Second Bonus: Draw +1 card/6 total (was +2/7)

### MOSES AVATAR

**Moses — "Moses the Deliverer"**
- Art: ✅ Illustrated
- Passive: Whenever you remove a Corruption token from the active Prophecy, gain 2 Morale.
- +1: Meditate 3 (look at top 3 cards, keep 1, rest to bottom in random order)
- -1: Remove 1 Corruption from the active Prophecy.
- -5: Deal 2 damage to all Enemy Units.

### MOSES PROPHECY (Locked 2026-03-03)

| Stage | Name | Faith Cost | Requirement |
|-------|------|-----------|-------------|
| I | The Plagues | 2 Faith | At least 2 Enemy Units destroyed this game. If not, cost is 4 Faith instead. |
| II | Exodus | 4 Faith | Control at least 1 Sanctuary, 1 Relic, and 1 Unit. |
| III | Parting the Red Sea | 6 Faith | Control 2+ Units AND Enemy controls 0 Units. |
| IV | The Promised Land | 8 Faith | Enemy Avatar has 0 Dominion. |

### MOSES UNITS (All ✅ Illustrated)

| Name | Cost | Power | Endurance | Keywords | Text |
|------|------|-------|-----------|----------|------|
| Levite Guardian | 2F | 1 | 3 | — | Enter: remove 1 Corruption from Prophecy. |
| Hebrew Elder | 3F | 0 | 4 | — | First time each turn an enemy Unit is destroyed: gain 1 Faith. Damage reduced by 1. |
| Exodus Defender | 3F | 1 | 4 | Ranged | Gets +1 Power while Prophecy has 0 Corruption. |
| Bezalel, Son of Uri | 4F | 3 | 3 | Unique | Gets +1/+1 per Sanctuary you control. |
| Angel of the Lord | 6F | 5 | 7 | Unique, Zealot | (No text) |

### MOSES SANCTUARIES (All ✅ Illustrated)

| Name | Text |
|------|------|
| Mount Sinai | At start of turn: Remove 1 Corruption. If removed, gain 1 Morale. |
| The Red Sea | At start of turn: Gain 1 Faith. If you control ≤2 Units, gain 1 Morale. |
| Manna Fields | At start of turn: Look at top card of deck. May put on bottom. |
| Goshen Refuge | At start of turn: Heal 1 damage from each Unit you control. If healed 2+, gain 1 Morale. |

### MOSES PRAYERS (All ✅ Illustrated)

| Name | Cost | Text |
|------|------|------|
| The Burning Bush | 1F | Look at top 3 cards. Keep 1, rest to bottom in random order. |
| Plague of Frogs | 2F | Deal 1 damage to each Enemy Unit. |
| Let My People Go | 3F | [BALANCE TEST: Remove 1 Corruption / Draw 2 Cards] (Prev: Remove 2 / Draw 1) |
| Manna from Heaven | 3F | Draw 2 cards then discard 1. Gain 2 Morale. |
| Passover | 3F | Prevent next 2 damage to each Unit you control this turn. Remove 1 Corruption. |
| Plague of Darkness | 4F | Enemy cannot play non-Unit cards until start of your next turn. Gain 2 Morale. |
| I AM WHO I AM | 4F-5F | Remove all Corruption from Prophecy. Gain 1 Morale. |
| Plague of Locusts | XF | Create X/2 (rounded down) 1/1 Locust tokens. |
| Parting the Red Sea | 6F | Unique. Destroy all Enemy Units. |

### MOSES COVENANTS (All ✅ Illustrated)

| Name | Cost | Text |
|------|------|------|
| The Exodus | 2F | Units you control have Zealot if you have 5+ Faith. |
| Passover Mark | 3F | Enemy Units get -1 Power. |
| Deliverance | 1F | Prevent the first damage your Avatar takes each turn. |
| Protection | 3F | Enemy Units with >2 Power must pay 1 Dominion to attack. |

### MOSES RELICS (✅ Designed, 🔲 Not yet illustrated)

| Name | Cost | Text |
|------|------|------|
| Staff of Moses | 3F | Tithe: Gain 1 Faith. Whenever you play a Prayer: gain 1 Morale. |
| Blessed Spring | 3F | Tithe: If Prophecy has 0 Corruption, draw 1 card. Enemy card effects can't add more than [1/2] Corruption per turn. |
| Stone Tablets | 4F | Sanctuaries can't be destroyed. Sanctuary effects doubled. |
| The Ark of the Covenant | 6F | Tithe: Remove 1 Corruption + gain 1 Morale. Units get +1/+0. |

*(Note: JSON also lists The Burning Bush as Relic — a 2F version that gives 1 Morale/turn. Moses-set.md lists 5 Relics including Bronze Serpent. JSON and MD are not perfectly synced — Bronze Serpent appears in JSON as a Relic.)*

### MOSES INTERVENTIONS

| Name | Cost | Text |
|------|------|------|
| Divine Protection | 1F | Heal 2 or prevent next 2 damage to target Unit or Avatar. |
| Inspired Courage | 1F | Target Unit gets +2/+2 until end of turn. |
| Purge | 2F | Remove 1 Corruption from Prophecy. |
| Demystify | 3F | Destroy target Curse or Relic. |

---

### PHARAOH AVATAR

**Pharaoh — "Lord of Egypt"**
- Art: ✅ Illustrated
- Passive: At the start of your turn, add 1 Corruption token to the active Prophecy.
- +1: Create a 2/1 Taskmaster.
- -3: Add [1/2] Corruption to the active Prophecy. (Balance test: 2)
- -5: Moses loses 2 Faith and you gain 2 Dominion.

### PHARAOH UNITS (All ✅ Illustrated)

| Name | Cost | Power | Endurance | Keywords | Text |
|------|------|-------|-----------|----------|------|
| Egyptian Taskmaster | 1D | 2 | 1 | — | When this unit deals Avatar damage: add 1 Corruption. |
| Royal Guard | 2D | 1 | 2 | — | Gets +1/+1 while you control a Stronghold. |
| Pharaoh's Magician | 3D | 1 | 3 | — | If Moses had a Unit die this turn: add 1 Corruption. |
| Chariot Rider | 4D | 4 | 2 | Zealot | (No text) |
| High Overseer | [4D/5D] | 4 | 6 | Unique | Pithom and Labor Camp Strongholds trigger twice. |

### PHARAOH STRONGHOLDS (All ✅ Illustrated)

| Name | Text |
|------|------|
| Pithom | At start of turn: Add [2] Corruption. [Balance test: flat 2 vs. 1 + conditional 1 if opponent has 5+ Faith] |
| Temple of Ra | At start of turn: Gain 1 Dominion. If you control a Relic, gain 1 more. |
| Labor Camp | At start of turn: Create 1/1 Laborer. If it dies this turn: add 1 Corruption. |
| The Nile River | First time per turn opponent loses Faith from Avatar damage: gain 1 Dominion. If only Stronghold: gain 2 instead. |

### PHARAOH RITUALS (All ✅ Illustrated)

| Name | Cost | Text |
|------|------|------|
| Supplication | 1D | Gain 3 Morale. |
| Pharaoh's Edict | 2D | Draw 2, discard 2. Add 1 Corruption. |
| Forced Labor | 2D | Target player discards 1 at random. Gain 1 Morale. |
| Decimate | 2D | Opponent sacrifices a Unit they control. |
| Give Chase! | 3D | Units gain +2 Power and Martyr until end of turn. |
| Charge! | 3D | Units gain Zealot and "Avatar damage = +1 Corruption" until end of turn. |
| Hardened Heart | [3D/4D] | Until start of your next turn, Corruption cannot be cleansed. |
| Rank and File | 4D | Create three 1/1 Soldier tokens with Zealot. |
| Massacre | 6D | Destroy all Units (both sides). |

### PHARAOH CURSES (All ✅ Illustrated)

| Name | Cost | Text |
|------|------|------|
| Pestilence | 2D | At start of your turn: Deal 1 damage to a random Unit Moses controls. |
| Darkness | 3D | Moses may only play 1 Unit per turn. |
| Bondage | 4D | Units Moses plays cost +1 Faith. |
| Bloody Delta | 5D | Whenever opponent gains Morale, they gain 1 less. |

### PHARAOH RELICS (✅ Designed, 🔲 Not yet illustrated)

| Name | Cost | Text |
|------|------|------|
| Idol of Ra | 3D | Tithe: Gain 1 Dominion. If Temple of Ra in play: gain 2 instead. |
| Pharaoh's Scepter | 3D | Tithe: Gain 1 Morale. First time per turn you add Corruption: gain 1 more Morale. |
| Khopesh of Retribution | 4D | Tithe: Target Unit gets +1/+0. When that Unit deals Avatar damage: gain 2 Morale. |
| Pharaoh's Headdress / Crown of the Pharaohs | 5D-6D | Units get +1/+1. Tithe: If 3+ Units, add 1 Corruption. |

### PHARAOH INTERVENTIONS

| Name | Cost | Text |
|------|------|------|
| Plague Boils | 1D | Target Unit gets -1/-1. |
| Raze | 4D | Destroy target Sanctuary or Covenant. |
| Corruption Syphon | 2D | Remove X Corruption. Target Unit gets +X/+X until end of turn. |
| Dominion over All | 1D | Gain X+1 Dominion, where X = Corruption tokens on Prophecy. |

### NEUTRAL CARDS (Draft — Pending Akasha Review)

**Neutral Hero Units:**
- Desert Wanderer 2F, 2/2 — Enter: if no cards in hand, draw 1.
- Shield Bearer 2F, 1/3 — Adjacent units take 1 less combat damage.
- Wilderness Scout 3F, 2/2 Ranged — On damage to a Unit: look at top 2, put 1 on bottom.

**Neutral Hero Relics:**
- Desert Oasis 2F — Tithe: +1 Morale. If no Units: +2 Morale.
- Tent of Meeting 3F, Unique — Tithe: If Prophecy has 0 Corruption, draw 1.

**Neutral Hero Interventions:**
- Divine Protection 2F — Prevent next 3 damage to target friendly Unit.
- Righteous Fury 2F — Target friendly Unit gets +2 Power EOT. If it destroys an enemy: gain 1 Morale.

**Neutral Enemy Units:**
- Desert Bandit 1D, 2/1 — (No text)
- Hired Mercenary 3D, 3/2 — Enter: add 1 Corruption.
- Pagan Priest 2D, 1/3 — Tithe: If no Strongholds, gain 1 Morale.

**Neutral Enemy Relics:**
- Idol of Gold 2D — Tithe: +1 Morale. If Moses's Prophecy has 0 Corruption: +2 Morale.
- Dark Altar 3D, Unique — Tithe: Add 1 Corruption.

**Neutral Enemy Interventions:**
- Ambush 2D — Target Enemy Unit (Moses-controlled) loses Formation.
- Treachery 3D — Counter target Prayer.

---

## 5. DAVID SET — WHAT EXISTS

*Source: cards/data/david-set.md*

Only Avatar cards designed and illustrated. The rest of the set (Units, Prayers/Prayers, Relics, Sanctuaries/Strongholds, Prophecy) is NOT yet designed.

### David Avatar — "David the Shepherd"
- Art: ✅ Illustrated
- Passive: First time each turn an Enemy Unit with 2+ Power dies: gain 1 Faith.
- +1: Create a 1/1 Shepherd.
- -2: Choose one of your Units. It gains +1 Power this turn and Duels target Enemy Unit.
- -5: Units you control gain +1 Power and Martyr until end of turn.
- Flavor: "You come against me with sword and spear and javelin, but I come against you in the name of the Lord Almighty."

### Philistine Army Avatar — "Enemy of Israel"
- Art: ✅ Illustrated
- Passive: Units you control with 4+ Power have Intimidate.
- +1: Create a 2/2 Philistine Warrior.
- -3: Add 1 Corruption to the active Prophecy.
- -5: Summon Goliath, Philistine Champion (Unique). [Stats not yet designed]
- Flavor: "A champion named Goliath, who was from Gath, came out of the Philistine camp. His height was six cubits and a span."

### New Keywords Introduced (David Set, Locked 2026-02-26)

**DUEL**
> "Target unit you control and target enemy unit deal damage equal to their Power to each other."
- Not an attack — bypasses Intimidate and Formation restrictions
- Cannot target Anointed units
- Both units deal damage simultaneously
- Triggered by ability, not by combat declaration

**INTIMIDATE**
> "Units with 2 or less Power cannot attack this unit."
- Power checked at moment of attack declaration
- Bypassed by Duel entirely
- Does not affect card effects targeting units
- Philistine Army passive grants Intimidate to all friendly units with 4+ Power

---

## 6. FUTURE HEROES & ENEMIES

*Source: chatgpt-exports/04-design-space-raw.md (design chat)*

These are designed at the Avatar/concept level. Cards not designed yet.

| Hero | Archetype | Enemy | Enemy Counter-Style |
|------|-----------|-------|---------------------|
| Moses | Control | Pharaoh | Escalation/Corruption |
| David | Tempo | Philistines | Power Threshold |
| Noah | Builder | Corrupted World | Swarm Corruption |
| Paul | Combo | Roman Empire | Tax Suppression |
| Daniel | Resilience | Babylon | Authority Edict |

### Noah
- Secondary resource: Wood (tracked counter type)
- Passive: When Enemy Unit is destroyed, gain 1 Wood
- Prophecy: Stage IV costs 10 Wood in addition to Faith
- Corrupted World Passive: If 3+ Units in play, add 1 Corruption at start of turn

### Paul
- Passive: May activate one additional ability per turn
- Roman Empire Passive: First additional ability opponent activates each turn costs 1 more
- Prophecy: Stage IV = resolve 3 Interventions in a single turn

### Daniel
- Passive: First time each turn you would lose Faith from Avatar damage, prevent it
- Babylon Passive: If opponent has 3+ Faith stored at start of their turn, add 1 Corruption

**Expansion potential beyond launch:** Old Testament Set, New Testament Set, Prophets Set, Judges Set, Kings Set, Apocalyptic Set.

---

## 7. ART DIRECTION

*Source: chatgpt-exports/03, 05, 06*

### Global Style
- **Semi-realistic painterly illustration** — real-world anatomy, historically grounded materials
- Visible brush texture in cloth and environment
- No hyper-polished digital fantasy sheen
- Materials feel tangible (linen creases, bronze patina, stone erosion, leather wear)

### Lighting Doctrine
- **Hero cards:** Warm directional sunlight, golden hour, ambient fill, subtle volumetric beams. Light feels inviting.
- **Enemy cards:** Overhead harsh sun OR torch-lit interiors, high contrast shadows, sharp edge highlights. Light feels exposing and unforgiving.
- No colored magical lighting (except extremely subtle ritual distortion for Pharaoh's Magician)
- Lighting direction: top-left; shadows: bottom-right

### Color Palettes
- **Hero:** Warm ochre, desert beige, soft sky blue, muted bronze, linen white (moderate saturation, no neon)
- **Enemy:** Burnished gold, oxidized bronze, black basalt, deep red earth, torch orange (stronger contrast, deeper shadows)

### Flesh Tone Guidelines
- Hebrews: Levantine / Near Eastern tones
- Egyptians: North African tones
- No modern stylized color shifts

### What to Avoid (All Pieces)
- Floating debris, dramatic particle storms, anime speed lines
- Heavy bloom, oversharpened edges, unnatural lens flares
- Text overlays, symbols floating in air, glowing eyes
- MMO-pristine armor

### Camera Rules
- Mid-shot or slight low-angle
- Character occupies 60-70% of vertical frame
- Head clearly separated from background
- Background depth but not detail overload
- Never crop top, left, right; may crop slightly below knees

### Card Frame System

**Unit Cards (Vertical)**
| Zone | % of Card Height |
|------|-----------------|
| Top Border + Cost Circle | ~10% |
| Art Window | ~50% |
| Nameplate Bar | ~8% |
| Rules + Flavor Text Box | ~35-38% |
| Stat Icons (overlay) | Bottom margin |

- Hero frame: Warm gold metallic trim, sandstone inner panel, blue faction circle top-left
- Enemy frame: Dark bronze/blackened metal, dark stone inner panel, crimson faction circle top-left
- Power icon: Ruby/amber gemstone bottom-left
- Endurance icon: Steel/iron shield bottom-right

**Sanctuary/Stronghold Cards (HORIZONTAL)**
- Landscape orientation
- Art window: 66% (top 2/3)
- Rules text: 25% (middle)
- Nameplate: 8% (bottom strip)
- Hero: Sandstone/gold, deep royal blue circle
- Enemy: Granite/brass, dark crimson circle
- Unique indicator: Small gold seal in lower-right of art frame

**Typography**
- Primary font reference: Cinzel Bold (free Google Font — identical to Trajan Pro)
- Hero title: Carved gold text
- Enemy title: Dark hammered metal text
- Rules text: Warm parchment-stone tone

**AI Generation Pipeline**
- All card art: AI-generated transparent PNGs
- Character art: Separate transparent character PNG
- Background: Separate AI-generated scene PNG
- Text: Separate transparent PNG layers generated via locked prompts
- Assembly: Photoshop layer compositing
- Locked prompts documented in chatgpt-exports/03

### Card Art Production Status (Moses Set)

| Category | Status |
|----------|--------|
| 5 Moses Units | ✅ All illustrated |
| 4 Moses Sanctuaries | ✅ All illustrated |
| 9 Moses Prayers | ✅ All illustrated |
| Moses Relics (4-5 cards) | 🔲 None illustrated |
| Moses Avatar | ✅ Illustrated |
| Moses Prophecy | 🔲 Not illustrated |
| 5 Pharaoh Units | ✅ All illustrated |
| 4 Pharaoh Strongholds | ✅ All illustrated |
| 9 Pharaoh Rituals | ✅ All illustrated |
| Pharaoh Relics (4 cards) | 🔲 None illustrated |
| Pharaoh Avatar | ✅ Illustrated |
| David Avatar | ✅ Illustrated |
| Philistine Army Avatar | ✅ Illustrated |
| Neutral Cards | 🔲 None illustrated |

### Per-Unit Art Direction (Moses Set — Key Notes)

**Angel of the Lord:** Tall imposing figure, bronze armor with Hebrew motifs, large realistic feathered wings (weight and shadow, not anime), white-gold sword with no energy flares, descending or standing with authority. Represents the Pillar of Flame. Expression: serene, divine authority — not rage.

**Chariot Rider:** Egyptian war chariot, two horses anatomically correct, bronze armor, charging forward. Diagonal thrust composition.

**Bezalel, Son of Uri:** Craftsman-warrior. Divine inspiration implied through light and composition, NOT glowing aura. Bronze tools historically plausible.

**Hebrew Elder:** Elderly man, white beard, linen robes, staff. NO magical energy. Wisdom through presence.

**High Overseer of Pithom:** Power conveyed through height, scale, architecture, shadow — NOT magical aura. Standing elevated over workers.

---

## 8. TECHNICAL — UNITY IMPLEMENTATION

*Source: unity/README.md, unity/BOARD_PRESENTATION.md*

### Stack
- **Engine:** Unity (LTS)
- **Platform:** iOS + Android
- **Unity project:** Not yet started (planned once design phase complete)

### Board Presentation Design (Locked 2026-02-24)
Units on the battlefield display as **character art sprites**, NOT card images.
- Card frame and text are hidden during normal play
- Character art stands on the board as a living presence
- Hover (desktop) or tap-and-hold (mobile) reveals full card view

**Board state per Unit:**
- Character art (full-body transparent PNG)
- Power badge (gem icon, bottom-left)
- Endurance badge (shield icon, bottom-right)
- Damage counter (red number badge when damaged)
- Status overlays

**Status Visual States:**
| State | Visual Treatment |
|-------|-----------------|
| In Formation | Full brightness |
| Out of Formation | Desaturated/darkened overlay |
| Anointed | Subtle gold outline glow |
| Persecuted (with damage) | Faint worn/battle-damaged overlay |
| Damaged | Red damage counter badge |
| Relentless (active chain) | Brief motion trail on attack animation |

**Card Preview (tap-and-hold):**
- Full card animates into view (~0.15s tween)
- Shows: frame, art, name, type, rules text, flavor, stats
- Dismisses on release / mouse-out
- Does not interrupt game state

### Prefab Structure (Planned)
```
Unit_Prefab
├── BoardView (default active)
│   ├── CharacterSprite (SpriteRenderer)
│   ├── PowerBadge (UI overlay)
│   ├── EnduranceBadge (UI overlay)
│   ├── DamageCounter (UI overlay)
│   └── StatusEffectLayer (material/shader overlay)
└── CardPreview (default inactive)
    ├── CardRenderer (populated from CardData ScriptableObject)
    └── AnimationController (tween in/out)
```

**Mobile Gesture Handling:**
- Tap (<200ms) = Select unit / confirm action
- Hold (>200ms) = Show card preview
- Release = Dismiss preview
- Drag = Declare attack (if In Formation)

### Animation Approach

**v1.0 Launch — Unity Tween Animation (DOTween)**
All implementable by AI agents. No Spine rigging or 3D modeling required.

| Animation | Behavior | Implementation |
|-----------|----------|----------------|
| Idle | Subtle breathing bob | Looping Y tween, ~4px, 2s cycle |
| Attack | Quick forward lunge + snap back | Position tween toward target |
| Hit Reaction | Red flash when taking damage | Color tween white → red → white |
| Death | Fall and fade out | Rotation + alpha fade |
| Summoned | Scale up from 0 | Scale tween 0 → 1.1 → 1.0 |
| Martyr Trigger | Gold pulse before death | Color flash (gold) before death |
| Anointed Glow | Persistent gold outline | Shader outline, pulsing opacity |

**v1.1 Post-Launch — Spine 2D**
- Requires hiring a Spine rigger
- Estimated cost: $1,500-2,000 USD for all 10 launch characters
- Legends of Runeterra quality movement

**v2.0+ Future — Full 3D**
- Requires dedicated 3D artist
- Blender → Unity pipeline
- Clash of Clans visual quality
- ChatGPT illustrations serve as reference art for 3D modelers

### Reference Games
- Slay the Spire — v1.0 animation reference
- Legends of Runeterra — v1.1 animation target
- Clash of Clans / Clash Royale — v2.0 vision
- Hearthstone — board card preview behavior

### Art Requirements for Unity
- Character art: transparent PNG, clear silhouette at 150-200px mobile scale
- Distinctive silhouette per unit (players identify units by silhouette before reading names)
- 300 DPI minimum, CMYK ready for print assets

---

## 9. DESIGN PHILOSOPHY

*Source: GDD.md, chatgpt-exports/01, 04*

### Core Principles (Locked)
1. Persistent resource tension — resources don't reset; every Faith spent is meaningful
2. Morale-based burst turns — temporary resource enables powerful turns without base inflation
3. Infrastructure vulnerability — Relics are attackable, creating board complexity
4. Formation-based tactical combat — attacking has a cost (unit goes Out of Formation)
5. Objective-driven victory through Prophecy — not elimination, narrative completion
6. Limited instant-speed interaction — only Interventions use the stack; simplicity by design
7. Fixed 12-Round escalation — creates genuine timer pressure every game
8. Logical-world Uniqueness — not rarity-based; Unique because the thing is unique in the world
9. Competitive deck construction with faction-locked pools
10. Respectful biblical narrative — no parody, not doctrinally prescriptive

### What Makes This Different
- **No life totals.** No HP bar. The win condition is completing a story, not killing an opponent.
- **The enemy doesn't need to "win" proactively.** Pharaoh just needs to run out the clock. This creates asymmetric but balanced gameplay.
- **Persistent damage.** Wounded units stay wounded. Attrition is real.
- **Theme mirrors mechanics.** Faith/Dominion, Prayer/Ritual, Sanctuary/Stronghold — the language of faith and the language of power are distinct even when rules are the same.
- **Every set tells a specific biblical story.** Moses vs Pharaoh. David vs Philistines. The game IS the story.

### Multiplayer Design Note
Original concept was 2-3 Heroes vs 1 Opposition. The 1v1 model was selected for Version 1 for balance, pacing, and demo simplicity. Co-op modes (2 Heroes vs 1 Enemy) are planned as advanced mode.

### The Akasha Principle
From the original design chat: *"Frame as a 'Biblical Narrative Strategy Game.' Avoid combat between biblical heroes. Avoid parody tone. Focus on strategic storytelling."*

---

## 10. SIMULATION RESULTS — BALANCE DATA

*Source: simulations/results/ — 24 batches of 5 games each = 120 base games. Plus Coordinator A (games 71-95) and Coordinator B (games 96-120) for additional 50 games.*

### Base Simulation Summary (Batches 1-24, Games 1-120, Base Rules)
- **Total games:** 120
- **Moses wins:** 67 (55.8%)
- **Pharaoh wins:** 53 (44.2%)
- **Average winning round:** ~11.0 (most games go to Round 11-12)

### Balance Test Results (Coordinator Reports, applying temp changes from 2026-03-04)
- **Coordinator A (Games 71-95):** Moses 14 wins, Pharaoh 11 wins (56% Moses)
- **Coordinator B (Games 96-120):** Moses 11 wins, Pharaoh 14 wins (44% Moses) — Pharaoh favored under temp changes

### Key Balance Findings

**Moses wins via:** Prophecy Stage IV completion, usually Rounds 9-12. The path is narrow but swift when it opens: board-wipe (Parting the Red Sea) → Stage III → drain Pharaoh Avatar to 0 Dominion for Stage IV.

**Pharaoh wins via:** Round 12 timeout attrition. Zero Pharaoh victories came from "killing" Moses — it's always about Corruption accumulation and board denial keeping Moses below Stage III.

**Critical cards:**
- **Parting the Red Sea** (6F): Moses's signature board wipe. Near-mandatory to meet Stage III (0 enemy units). When Moses wins, this card is almost always involved.
- **Stone Tablets + Mount Sinai combo:** Doubled Sanctuary tithe removes 2 Corruption/turn — exactly counters Pithom's 2/turn. When Moses draws both, wins come 2 rounds early (Rounds 9-10).
- **Pithom + High Overseer:** Premier Pharaoh combo. High Overseer doubles Pithom triggers. At 4 Dominion cost (balance test), can enter Round 4-5, generating +4 Corruption per tithe. Devastating.
- **Blessed Spring:** Corruption cap (1-2/turn). Moses's primary Corruption rate limiter against Pithom.
- **Hardened Heart:** Timing matters enormously. Played just before Moses's turn = prevents all cleansing for a critical round. At 3D (cheaper), accessible 1 round earlier.

**Going-second penalty:** Moses going second (6-card hand) wins only 33% of those games vs 54% when going first. The reduced hand disadvantages Moses specifically because the corruption-removal + board-wipe + prophecy-advancement combo requires specific cards.

**Stage wall pattern:** When Pharaoh wins, Moses consistently reaches Stage III but cannot complete Stage IV within 12 rounds. Stage I/II walls are created by Darkness+Bondage denial combos.

**No infinite loops possible** (confirmed by ChatGPT rules audit). No resource spirals. Mechanics are internally consistent.

---

## 11. KEYWORDS — COMPLETE REFERENCE

*(Locked 2026-02-26 — all keywords in canonical state)*

| Keyword | Text | First Seen | Status |
|---------|------|------------|--------|
| **Zealot** | Enters play In Formation (Haste) | Moses set | ✅ Locked |
| **Ranged** | Deals damage first; if target would die, no return damage | Moses set | ✅ Locked |
| **Unique** | Max 1 per deck, max 1 in play; replacement rule | Moses set | ✅ Locked |
| **Martyr** | When this unit dies, gain 1 Morale | Moses set | ✅ Locked |
| **Anointed** | Cannot be target of opponent's card effects | Moses set | ✅ Locked |
| **Persecuted** | While this unit has damage on it, gets +1/+1 | Moses set | ✅ Locked |
| **Relentless** | If destroys a Unit in combat, regains Formation and may attack again | Moses set | ✅ Locked |
| **Duel** | Both units deal Power damage to each other; not an attack, bypasses Intimidate | David set | ✅ Locked |
| **Intimidate** | Units with 2 or less Power cannot attack this unit | David set | ✅ Locked |

**Ability Shorthand (Not keywords, but locked):**
- **Meditate X:** Look at top X cards. Keep 1, rest to bottom in random order.

---

## 12. CURRENT STATUS

### What Exists
- ✅ Game Design Document v0.6 (complete, GDD.md)
- ✅ Rules Canon v1.0 (locked, internally consistent, audit-verified)
- ✅ All keywords locked and fully ruled
- ✅ Moses set: All 10 Units illustrated, all 9 Prayers illustrated, all 4 Sanctuaries illustrated, Avatars illustrated
- ✅ Pharaoh set: All 10 Units illustrated, all 9 Rituals illustrated, all 4 Strongholds illustrated, Avatar illustrated
- ✅ David + Philistine Army: Avatars designed and illustrated
- ✅ Moses Prophecy: Locked (2026-03-03)
- ✅ Card data in JSON format (moses-set.json — machine-readable)
- ✅ Card frame design system locked (Sanctuary frame, Unit frame, visual system)
- ✅ 120+ game simulations completed
- ✅ Unity board presentation design locked
- ✅ Unity animation spec (v1.0 tween approach)
- ✅ Balance testing in progress (temp changes applied 2026-03-04)
- ✅ Future hero concepts (Noah, Paul, Daniel) outlined
- ✅ Expansion roadmap outlined

### What's Pending / Not Done
- 🔲 All Relics not illustrated (0/5 Moses, 0/4 Pharaoh)
- 🔲 Moses Prophecy card not illustrated
- 🔲 Neutral cards not illustrated (7 designed)
- 🔲 Moses Covenant/Intervention art not confirmed illustrated (marked ✅ in MD but check)
- 🔲 David set cards (Units, Prayers, Relics, Sanctuaries, Prophecy) — NOT designed
- 🔲 Goliath (Philistine Avatar -5 summon) — stats/text not designed
- 🔲 Unity project not started
- 🔲 Spine 2D rigging not started
- 🔲 Text rework pass (Summon → Unit terminology in art) not started
- 🔲 Noah/Paul/Daniel sets — not designed beyond Avatar concepts
- 🔲 Balance test changes need Akasha confirmation before becoming permanent
- 🔲 Several open design questions (see Section 12)

---

## 13. OPEN QUESTIONS

*(Collected from all files — unresolved as of 2026-03-09)*

### Rules/Mechanics
1. **Sanctuary cost:** When are Sanctuaries played and at what cost? The rules say "max 1 per turn" and "effects begin next turn" but no cost is listed anywhere. Are they free? Is there a Faith cost?
2. **Going-second bonus:** Permanently +1 (6 total) or still +2 (7 total)? The temp balance change reduced it — not confirmed by Akasha.
3. **Meditate X timing:** Put cards on bottom "in random order" — confirmed in keywords.md but old notes say "in any order." Which is it?
4. **Covenant/Curse:** What does "horizontal card" mean in practice? Do they go in the same zone as Sanctuaries/Strongholds? Or a separate zone?
5. **Simultaneous damage for Duel:** Confirmed simultaneous. But does Ranged on a Dueling unit change this? (Duel explicitly says not an attack — probably no interaction with Ranged, but not stated)
6. **Prophecy advancement timing window:** Can Pharaoh play Hardened Heart after Moses declares advancement? No — costs are paid instantly and cannot be interrupted. But can they play it before Moses declares? Yes. This is confirmed intentional.
7. **Relic Unique rule:** The MD says "All Relics are inherently Unique by card type — not printed on card." But moses-set.json shows `"keywords": ["Unique"]` on Relics. Which is the correct representation for UI/data?

### Card Design
8. **The Burning Bush Relic:** Both the JSON and MD list a "The Burning Bush" as a Relic (2F, gain 1 Morale/turn) AND as a Prayer (1F, look at top 3). Can the same name exist on two different card types? This needs resolution.
9. **Let My People Go — balance test:** Current MD says "Remove 1 Corruption, Draw 2 Cards." JSON says "Remove 2 Corruption, Draw 1 Card." Which is canon right now? The temp balance note at top of MD says the MD version is the test version.
10. **High Overseer name:** "High Overseer" or "High Overseer of Pithom"? Inconsistent across files.
11. **Massacre flavor text:** Missing — noted as needing addition.
12. **Supplication name:** Confirmed intentional (humble prayer as Enemy card)?
13. **Charge! flavor text:** Same as proposed Idol of Ra Relic — needs unique flavor.
14. **Crown of the Pharaohs vs. Pharaoh's Headdress:** JSON calls it "Crown of the Pharaohs" (5D), MD calls it "Pharaoh's Headdress" (6D). Different names and costs — which is correct?
15. **Goliath stats:** The David Avatar's -5 summons Goliath (Unique). Stats and card text not designed.
16. **David Prophecy:** Not designed at all.
17. **Stone Tablets text inconsistency:** MD says "Sanctuaries can't be destroyed. Their effects doubled." JSON says "At start of turn, if 0 Corruption, draw 1 card. Enemy effects can't add more than 1 Corruption per turn." These are completely different cards. Which is canon for Stone Tablets?
18. **Blessed Spring cap:** MD says 2 Corruption/turn (temp balance), JSON says 1/turn (old value). Which is currently active?

### Production
19. **Testaments_Visual_System_v1.txt:** Referenced in chatgpt-exports/03 as existing — where is this file? Not in the repo.
20. **Covenants illustrated?** MD marks "✅ All Illustrated" for Moses Covenants but no art status tracking is visible anywhere for them.
21. **Text rework:** When will the Summon → Unit terminology audit happen? Multiple cards have wrong terminology in generated art.
22. **Purge Intervention:** Listed in the MD's Intervention section but NOT in the JSON. Is it a real card?

### Design Philosophy
23. **Multiplayer mode:** Co-op 2-Heroes vs 1-Enemy — when/how is this being designed?
24. **Generic card pools:** No generic Hero or Enemy pool cards are fully designed. Only the Avatar-specific pools exist for Moses/Pharaoh.

---

## 14. KEY FILES MAP

Every file in the repository and what it contains:

| File | Contents |
|------|----------|
| `README.md` | Project overview, repo structure, status (pre-production) |
| `design/GDD.md` | ⭐ Game Design Document v0.6 — core rules, card types, Moses/Pharaoh full design, keywords, launch roster |
| `design/mechanics/README.md` | Stub (placeholder) |
| `design/mechanics/keywords.md` | ⭐ Complete canonical keyword reference — ALL 9 keywords with full rules, Meditate shorthand |
| `design/lore/README.md` | Stub (placeholder) |
| `design/art-direction/README.md` | Stub (placeholder) |
| `cards/README.md` | Stub |
| `cards/data/README.md` | Stub |
| `cards/data/moses-set.md` | ⭐ Complete Moses/Pharaoh card set in markdown — all cards with text, flavor, art status, production checklist. Includes TEMP BALANCE CHANGES header |
| `cards/data/moses-set.json` | ⭐ Machine-readable JSON card data — full Moses/Pharaoh set including Neutrals. Use for Unity ScriptableObjects. Note: some values differ from .md |
| `cards/data/david-set.md` | David + Philistine Army Avatar cards. New keywords introduced. Production status. |
| `art/README.md` | Stub |
| `art/cards/.gitkeep` | Empty placeholder |
| `art/characters/.gitkeep` | Empty placeholder |
| `art/references/.gitkeep` | Empty placeholder |
| `art/ui/.gitkeep` | Empty placeholder |
| `docs/TEXT-REWORK-TODO.md` | ⭐ Checklist of all known card text issues — Summon→Unit terminology, name consistency, missing flavor text |
| `docs/chatgpt-exports/README.md` | Stub |
| `docs/chatgpt-exports/01-biblical-trading-card-game-raw.md` | ⭐ Original design concept — full initial vision, multiplayer structure, all Avatar concepts, initial rulebook skeleton, 1v1 vs multiplayer analysis |
| `docs/chatgpt-exports/02-testaments-rules-canon-raw.md` | ⭐ Official Rules Canon v1.0 — the most authoritative rules document. All locked mechanical decisions, ChatGPT audit, terminology lock |
| `docs/chatgpt-exports/03-hero-template-workflow-raw.md` | ⭐ Card frame design decisions — font system (Cinzel Bold), ALL locked AI generation prompts, Photoshop layer style values, card art pipeline |
| `docs/chatgpt-exports/04-design-space-raw.md` | ⭐ All major mechanical locks in sequence — resource model, Morale, Prophecy, turn structure, combat, deck construction. Plus full Noah/Paul/Daniel/Babylon/Rome Avatar designs. Cost curve baseline. |
| `docs/chatgpt-exports/05-sanctuary-card-frame-design-raw.md` | ⭐ Sanctuary/Stronghold frame specs — horizontal layout, material choices, faction variants, per-card art direction for all 8 Sanctuaries/Strongholds, text layout solutions |
| `docs/chatgpt-exports/06-summons-raw.md` | ⭐ Complete Unit list with art direction — per-unit camera/lighting/costume direction for all 10 launch units, card frame template specs, visual power hierarchy |
| `docs/design-review-enoch-240224.md` | ⭐ Enoch's design review from 2026-02-24 — keyword suggestions, balance concern on Taskmaster, full Prayer/Relic card designs for both sides, identified design gaps |
| `unity/README.md` | Unity stub — engine and platform targets |
| `unity/BOARD_PRESENTATION.md` | ⭐ Board visual design — character sprites on board, card preview on hover/hold, Unity prefab structure, animation spec (v1 tween through v2 3D), reference games |
| `simulations/SIM-INSTRUCTIONS.md` | Full simulation instructions with complete decklists, decision framework, recording format |
| `simulations/SIM-INSTRUCTIONS-FAST.md` | Condensed simulation instructions |
| `simulations/results/batch-01.md` through `batch-24.md` | 120 simulation game results (5 per batch) |
| `simulations/results/coordinator-A-report.md` | Games 71-95 results + balance analysis (temp changes applied) |
| `simulations/results/coordinator-B-report.md` | Games 96-120 results + balance analysis |

---

## 15. THINGS ELIJAH NEEDS TO KNOW

Critical context for someone joining this project:

### The State of the Game
The game design is substantially complete and internally consistent. This isn't speculative — Rules Canon v1.0 has been audited and verified by ChatGPT with no loops, no timing traps, and no resource spirals. The Moses/Pharaoh matchup has been simulated 120+ times. It works. The Hero wins ~56% of games, which is intentionally slight-Hero-favored by design.

### The Balance Test
As of 2026-03-04, there are 9 balance changes applied to the simulation deck that have NOT been confirmed by Akasha. These are marked at the top of `cards/data/moses-set.md`. Do NOT treat these as permanent until Akasha explicitly confirms them. The original values are in `moses-set.json`. The balance test makes the game more Pharaoh-favored (~44% Moses under Coordinator B's analysis).

### The JSON vs MD Discrepancy
`moses-set.json` and `moses-set.md` are not perfectly synced. The MD reflects more recent design decisions (including the temp balance changes). The JSON is the "clean" production data. Key discrepancies: Stone Tablets text, Blessed Spring cap value, High Overseer cost, Let My People Go text. When in doubt, ask Akasha which is canon for the field in question.

### The Terminology Rename
Cards generated before 2026-02-24 call Units "Summons" in their art text. The official card type is now "Unit." Multiple cards need art regeneration. This is tracked in `docs/TEXT-REWORK-TODO.md` and has not been done yet.

### The Art Pipeline
All art is AI-generated. The system is: AI generates character (transparent PNG) + AI generates background (separate PNG) + AI generates text elements (transparent PNGs) → Photoshop assembly. The locked AI generation prompts are in `chatgpt-exports/03`. The most important file not in the repo is `Testaments_Visual_System_v1.txt` — Akasha has this. Get it.

### What the Simulations Tell You
- Moses needs Parting the Red Sea to win reliably (Stage III requires 0 enemy units)
- Pharaoh's game plan is Corruption attrition to timeout at Round 12
- Stone Tablets + Mount Sinai is a hard counter to the Pithom engine
- Pithom + High Overseer (at 4D cost) is Pharaoh's most dangerous combo
- Moses going second is a meaningful disadvantage — the 6-card hand hurts his combo assembly

### What Enoch Did (Design Review)
`docs/design-review-enoch-240224.md` is Enoch's work: he read all 6 ChatGPT design chats and compiled a full design review on 2026-02-24. He suggested Martyr (adopted), Steadfast/Anointed (adopted as Anointed), and Persecuted (adopted). He flagged the Taskmaster + Avatar combo as a potential balance concern. He also wrote out full Prayer, Relic, and Intervention card designs for both sides — most of which were adopted. This doc is part of the design history.

### Design History Lives in ChatGPT Exports
The six chatgpt-export files contain the full design history — every decision made, every idea considered and rejected, every card designed. If something seems inconsistent or you wonder "why did they do it this way," the answer is almost certainly in one of those files.

### The David Set is Avatar-Only
David and Philistine Army are designed and illustrated at the Avatar level only. Zero other cards exist for that set. Goliath (summoned by Philistine -5) has no stats. The Prophecy for David doesn't exist. Noah, Paul, and Daniel are concept-level only.

### Unity Doesn't Exist Yet
The Unity project has not been started. All technical planning is on paper. The board presentation design and animation spec are designed but unimplemented. No code exists.

### The Repo is the Source of Truth
The goal per `TEXT-REWORK-TODO.md`: "repo becomes master record" after a final sync from all ChatGPT chats and a full card-by-card audit by Enoch. That final sync hasn't happened yet. Some design decisions may still exist only in ChatGPT chat logs that haven't been exported to the repo.

### Tone and Culture
Akasha's design intent: respectful, serious, not doctrinally prescriptive. This is a strategy game that uses biblical narrative as its framework — not a Christian ministry product, not a parody. Every card has a real biblical quote as flavor text. The art is historically grounded. The game should feel like the Bible brought to life as a competitive card game, not a Sunday school project.

---

*Briefing complete. Total files read: 50+ (all non-.git files in repo). Simulation data: 120 base games + 50 coordinator games. All design documents fully processed.*
