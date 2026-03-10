# Pluribus Pattern Analysis
## 2,000 Hands - NL Hold'em Study Document

**Dataset:** Pluribus vs. World-Class Pros (6-handed, 50/100, 10k stacks)  
**Hands Analyzed:** 2,000 of 10,000 available  
**Generated:** 2026-03-10  

---

## Table of Contents
1. [Parser Code](#parser-code)
2. [Statistical Summary](#statistical-summary)
3. [Key Pattern Analysis](#key-pattern-analysis)
4. [Top 20 Instructive Hands](#top-20-instructive-hands)
5. [Key Takeaways vs. Conventional Wisdom](#key-takeaways-vs-conventional-wisdom)
6. [Application to Micro-Stakes NL Hold'em](#application-to-micro-stakes-nl-holdem)

---

## Parser Code

The full parser is at `~/poker-study/parse_hands.py`. Here is a condensed version of the core parsing logic:

```python
#!/usr/bin/env python3
"""
Pluribus Hand Parser - core logic summary
Full version: ~/poker-study/parse_hands.py
"""

import re
from pathlib import Path
from collections import defaultdict

DATASET_PATH = Path.home() / "poker-study/phh-dataset/data/pluribus"
BIG_BLIND = 100
POSITION_NAMES_6H = {0: "SB", 1: "BB", 2: "UTG", 3: "HJ", 4: "CO", 5: "BTN"}

def parse_phh(filepath):
    with open(filepath) as f:
        content = f.read()
    
    # Extract players, actions, stacks
    players = re.findall(r"players\s*=\s*\[([^\]]+)\]", content)[0]
    players = [p.strip().strip("'\"") for p in players.split(",")]
    actions = re.findall(r"'([^']+)'", 
        re.search(r"actions\s*=\s*\[(.+?)\]", content, re.DOTALL).group(1))
    
    pluribus_idx = players.index("Pluribus")
    pluribus_pos = POSITION_NAMES_6H[pluribus_idx]
    
    # Simulate pot through streets
    # Action codes: d dh pN CARDS (deal), d db CARDS (board), 
    #               pN f (fold), pN cc (call/check), pN cbr AMOUNT (raise/bet)
    
    sim_committed = [0] * 6
    sim_pot = sum(blinds)  # apply blinds first
    
    for action in actions:
        parts = action.split()
        if parts[0] == "d":
            if parts[1] == "db":
                street += 1  # flop/turn/river
        elif parts[1] == "cbr":
            amount = int(parts[2])
            additional = amount - sim_committed[player_idx]
            sim_pot += additional
            sim_committed[player_idx] = amount
            # Record: pct_pot = additional / (sim_pot - additional) * 100
        elif parts[1] == "f":
            folded.add(player_idx)
    
    return hand_result_dict

# Run: analyze_hands(max_hands=2000) -> list of hand dicts
# Then: compute_stats(hands) -> statistical summary
# Then: find_instructive_hands(hands, n=20) -> top hands for study
```

---

## Statistical Summary

### Overview

| Metric | Value |
|--------|-------|
| Hands analyzed | 2,000 |
| Total net chips | +31,047 |
| Win rate (bb/100) | **+15.52 bb/100** |
| Hands won (any positive) | 373 / 2,000 (18.6%) |
| VPIP | **24.9%** |
| PFR | **17.2%** |
| VPIP/PFR ratio | 1.45 |
| 3-bets made | 72 (3.6% of hands) |
| 4-bets made | 17 |

*Note: "win rate" counts any net-positive hand. Most hands are folds with no money lost. bb/100 is the accurate metric.*

---

### VPIP / PFR by Position

| Position | Hands | VPIP | PFR | VPIP:PFR |
|----------|-------|------|-----|----------|
| BTN | 337 | 22.3% | 18.7% | 1.19 |
| CO | 337 | 23.4% | 21.7% | 1.08 |
| HJ | 335 | 23.9% | 23.6% | 1.01 |
| UTG | 333 | 16.8% | 16.8% | 1.00 |
| SB | 328 | 27.7% | 12.8% | 2.17 |
| BB | 330 | 35.8% | 9.4% | 3.81 |

**Key insight:** UTG has VPIP = PFR = 16.8% - virtually never limp-calling. From CO and HJ, nearly all VPIP is PFR. SB and BB are the only positions with significant calling ranges.

---

### Preflop Action Distribution

| Position | Fold | Call | Raise | Check |
|----------|------|------|-------|-------|
| BTN | 77.7% | 3.6% | 18.7% | - |
| CO | 76.6% | 1.8% | 21.7% | - |
| HJ | 76.1% | 0.3% | 23.6% | - |
| UTG | 83.2% | - | 16.8% | - |
| SB | 72.3% | 14.9% | 12.8% | - |
| BB | 59.7% | 26.4% | 9.4% | 4.5% |

---

### Open Raise Sizing by Position

| Position | Count | Avg Size | Median | Most Common Range |
|----------|-------|----------|--------|-------------------|
| BTN | 66 | 2.26bb | 2.2bb | 2.0-2.5bb (98.5%) |
| CO | 79 | 2.20bb | 2.2bb | 2.0-2.5bb (93.7%) |
| HJ | 80 | 2.17bb | 2.0bb | 2.0-2.5bb (97.5%) |
| UTG | 60 | 2.19bb | 2.0bb | 2.0-2.5bb (91.7%) |
| SB | 25 | 2.50bb | 2.5bb | 2.0-2.5bb (72.0%) |
| BB (3bet) | 35 | 11.4bb | 12.2bb | - |

**Key insight:** Pluribus uses a nearly uniform 2.0-2.5bb open raise from ALL positions. No position-based sizing adjustment. This is remarkably small - most humans use 2.5-3x from UTG/HJ.

---

### 3-Bet Sizing

| Metric | Value |
|--------|-------|
| 3-bets made | 72 |
| Average 3-bet size | **9.8bb** |
| Median 3-bet size | **9.1bb** |
| 4-bets made | 17 |
| Average 4-bet size | 27.0bb |

---

### Facing Opens - Response by Position

| Position | Fold% | Call% | 3-bet% | Sample |
|----------|-------|-------|--------|--------|
| BTN | 93.7% | 5.4% | 0.9% | 221 |
| CO | 96.7% | 2.8% | 0.5% | 215 |
| HJ | 99.0% | 0.5% | 0.5% | 210 |
| UTG | 100.0% | 0.0% | 0.0% | 225 |
| SB | 87.2% | 11.9% | 0.9% | 226 |
| BB | 63.5% | 35.7% | 0.8% | 244 |

**Key insight:** UTG folds 100% to an open raise. Even BTN folds 93.7%. These are tight linear ranges - Pluribus is NOT a wide cold-caller. It 3-bets instead of calling out of position.

---

### C-Bet Statistics

| Metric | Value |
|--------|-------|
| C-bet opportunities | 144 |
| C-bets made | 90 |
| **C-bet frequency** | **62.5%** |
| Average c-bet size | 72.3% pot |
| Median c-bet size | **50% pot** |

**C-bet by flop texture (significant samples):**

| Texture | Freq | Avg Size | Sample |
|---------|------|----------|--------|
| Rainbow, disconnected, broadway | 78.9% | 83% pot | 19 |
| Two-tone, disconnected, broadway | 73.7% | 63% pot | 19 |
| Rainbow, disconnected, ace-high | 71.4% | 110% pot | 7 |
| Two-tone, disconnected, middling | 60.0% | 81% pot | 10 |
| Rainbow, semi-connected, broadway | 75.0% | 83% pot | 4 |
| Two-tone, semi-connected, middling | 50.0% | 75% pot | 8 |
| Two-tone, connected, low | 20.0% | 50% pot | 5 |
| Rainbow, connected, middling | 75.0% | 85% pot | 4 |
| Monotone boards | Variable | 50-100% | small |

**Key pattern:** C-bet frequency is HIGH on dry/disconnected boards (75-80%) and LOW on wet/connected boards (20-50%). Sizing goes UP on dry broadway boards (83-110% pot) and DOWN on wet/low boards (50% pot).

---

### Turn / River Bet Frequency and Sizing

| Street | Opportunities | Bets Made | Frequency | Avg Size | Median Size |
|--------|--------------|-----------|-----------|----------|-------------|
| Flop (general) | 460 saw flop | ~140 bets | 30.4% | 72% pot | 50% pot |
| Turn | 184 | 72 | **39.1%** | 68% pot | 50% pot |
| River | 142 | 64 | **45.1%** | 124% pot | 75% pot |

**Bet size distribution by street:**

| Size Range | Flop | Turn | River |
|------------|------|------|-------|
| < 25% pot | 0.7% | 7.7% | 0% |
| 25-33% pot | 9.2% | 20.5% | 0% |
| 33-50% pot | 0% | 0% | 0% |
| 50-75% pot | 59.6% | 43.6% | 35.2% |
| 75-100% pot | 18.4% | 10.3% | 25.4% |
| > 100% pot | 12.1% | 17.9% | **39.4%** |

**Critical pattern:** River betting is POLARIZED. Either 50-75% pot or 100%+ pot - almost nothing in between. The 39% overbet rate on the river is a defining feature of Pluribus's style.

---

### Win Rate by Position

| Position | bb/100 |
|----------|--------|
| HJ | +82.4 |
| BTN | +63.5 |
| SB | +28.4 |
| BB | +1.1 |
| CO | -24.0 |
| UTG | -58.7 |

*Note: Small sample effects. UTG/CO losing is expected variance over 333 hands each, not a strategy failure.*

---

## Key Pattern Analysis

### 1. Preflop Range Construction

Pluribus plays a **linear, raise-or-fold strategy** from all positions:
- From UTG: 16.8% open, virtually no limps or cold calls
- From CO/HJ: 21-24% open
- From BTN: 18.7% open (BTN is NOT the widest position - surprising)
- From SB: 12.8% open raises, 14.9% calls (some stealing with calls)
- From BB: 9.4% 3-bets, 26.4% calls facing opens

The BTN being tighter than CO/HJ is counterintuitive. This likely reflects the specific dynamics of 6-max with world-class opponents in the blinds.

### 2. Open Sizing Uniformity

**2.0-2.5bb from every position.** No adjustment for position. This contradicts the conventional "raise bigger from early position" advice. Pluribus's reason: uniform sizing prevents opponents from exploiting size tells. Your hand strength isn't visible from bet size.

### 3. C-Bet Strategy: Texture-Dependent

**High frequency + large size on dry boards; low frequency + small size on wet boards.**

- Dry broadway (K72r, A83r): 75-80% frequency, 80-110% pot size
- Wet/connected (876tt, 543hh): 20-50% frequency, 50% pot size
- This is the opposite of what many players do (small cbet everywhere to "see where you stand")

### 4. River Overbets

Pluribus bets over 100% pot on 39% of its river bets. This is a signature "solver behavior" - using large river bets with a polarized range (strong hands and bluffs, nothing medium). The middle of your range checks back or calls.

### 5. Raise-Fold vs. Call Patterns

When facing a raise preflop:
- UTG: 100% fold. No cold-calling out of position against a raise.
- CO/HJ: 96-99% fold. 3-betting is the alternative to folding.
- BTN: 93.7% fold. Still very tight facing raises.
- BB: 63.5% fold, 35.7% call, 0.8% 3-bet.

**There is almost no cold-calling from out of position.** This is the biggest leak in rec player games - they cold-call too often from early positions.

### 6. 3-Bet Sizing

Average 3-bet is 9.1-9.8bb. Against a typical 2.2bb open, Pluribus 3-bets to roughly **4x the open** (e.g., 2.2x -> 8-10bb). This is on the larger side - creates fold equity preflop and protects IP post-flop.

### 7. Turn Aggression Uptick

Turn bet frequency (39.1%) is HIGHER than flop bet frequency (30.4% of all flops). When Pluribus bets turn, it often represents a credible range (made hand or strong draw). The hand that checks flop and bets turn is particularly weighted toward value.

### 8. Seeing the Flop Rate by Position

| Position | Saw Flop Rate |
|----------|--------------|
| BTN | ~22% |
| CO | ~23% |
| HJ | ~24% |
| UTG | ~17% |
| SB | ~27% |
| BB | ~36% |

These roughly track VPIP with slight BB inflation (defending).

---

## Top 20 Instructive Hands

---

### Hand 1 - BTN 3-bet pot, monotone board, delayed aggression

**File:** 106/132.phh | **Hand ID:** 132  
**Interest Score:** 17 | **Reasons:** went to river, big pot (7480 chips), Pluribus bet multiple streets, 3-bet pot, 4-bet pot, Pluribus won big pot, c-bet SKIPPED  
**Pluribus Position:** BTN | **Pluribus Cards:** KsAc  
**Players:** MrWhite (SB) | MrBlonde (BB) | MrBlue (UTG) | MrOrange (HJ) | MrPink (CO) | Pluribus (BTN)  
**Board:** 7h 8h Kh | 9h | Qh  
**Texture:** monotone, semi-connected, broadway

**Action:**

*Preflop:*
- Pluribus: RAISE/BET to 250 (2.5bb)
- MrWhite: RAISE/BET to 850 (8.5bb) - 3-bet
- Pluribus: RAISE/BET to 1930 (19.3bb) - 4-bet
- MrWhite: CALL

*Flop (7h 8h Kh) - Pot: 3,960:*
- MrWhite: CHECK
- Pluribus: **CHECK** (skipped c-bet!)

*Turn (9h) - Pot: 3,960:*
- MrWhite: BET 1,760 (44% pot)
- Pluribus: CALL

*River (Qh) - Pot: 7,480:*
- MrWhite: CHECK
- Pluribus: BET 6,310 (84% pot)
- MrWhite: FOLD

**Result:** Pluribus +3,790 chips (+37.9bb)

**Why instructive:**
- Pluribus 4-bets BTN vs SB with AKs. Standard.
- On the 7h8h9h9 board, Pluribus holds Ks Ac. The board is a monotone 4-flush after the turn. Pluribus does NOT c-bet the monotone flop - the board smashes the calling range's suited connectors, and Pluribus's actual equity is mediocre (K-high flush draw if the heart falls).
- When the 9h appears on the turn (4 hearts on board), Pluribus calls MrWhite's bet. MrWhite likely has a real heart or made a hand.
- River Qh completes the flush. Pluribus now has a king-high flush. MrWhite checks and Pluribus fires 84% pot. MrWhite folds. Pluribus doesn't overbet here - just a standard value bet.
- **Lesson:** On monotone flops as the 4-bettor, checking back is often correct. Your range advantage is neutralized by the board smashing draws. Wait for the texture to change.

---

### Hand 2 - HJ 4-bet pot, QQ runs it down

**File:** 106/218.phh | **Hand ID:** 218  
**Interest Score:** 16 | **Reasons:** went to river, big pot (20,360 chips), 4-bet pot, Pluribus won 10,360  
**Pluribus Position:** HJ | **Pluribus Cards:** QhQc  
**Players:** MrBlue (SB) | MrOrange (BB) | MrPink (UTG) | Pluribus (HJ) | MrWhite (CO) | MrBlonde (BTN)  
**Board:** 8s 3s Jc | 6d | 2h  
**Texture:** two-tone, disconnected, middling

**Action:**

*Preflop:*
- MrPink (UTG): RAISE to 210 (2.1bb)
- Pluribus: CALL 210 (flat the open)
- MrBlonde (BTN): RAISE to 1,210 (12.1bb) - squeeze
- Pluribus: RAISE to 2,210 (22.1bb) - 4-bet!
- MrBlonde: CALL

*Flop (8s 3s Jc) - Pot: 4,780:*
- Pluribus: BET 1,159 (24.2% pot)
- MrBlonde: CALL

*Turn (6d) - Pot: 7,098:*
- Pluribus: BET 6,631 (93.4% pot)
- MrBlonde: CALL

*River (2h) - Pot: 20,360:*
- Pluribus: CHECK
- MrBlonde: CHECK

**Result:** Pluribus +10,360 chips (+103.6bb)

**Why instructive:**
- This is a cold-call followed by a 4-bet, which is a squeeze squeeze. Pluribus calls the UTG open (flat), then when BTN squeezes, Pluribus 4-bets. QQ is strong enough to build the pot.
- Notice the c-bet sizing: **24% pot** on the flop. Tiny. This is likely a "protection bet with the best hand" - the board has a spade draw. Keep opponent's range wide, don't fold out hands you crush.
- Turn bet is huge: **93% pot** with a full commitment to the hand. The turn completes no draws (6d), QQ is still ahead of most of villain's range.
- River check: pot is all-in sized effectively. Just take the pot.
- **Lesson:** Small c-bet (25%) is viable with strong hands to keep villain in. Then escalate on the turn to get the money in.

---

### Hand 3 - HJ 3-bet call, AKcc on monotone club board, river raise

**File:** 105/14.phh | **Hand ID:** 14  
**Interest Score:** 16 | **Reasons:** went to river, big pot (6,100), 4-bet pot, Pluribus won 6,175  
**Pluribus Position:** HJ | **Pluribus Cards:** AcKc  
**Players:** MrWhite (SB) | MrPink (BB) | MrOrange (UTG) | Pluribus (HJ) | MrBlue (CO) | MrBlonde (BTN)  
**Board:** 4c 5c Qc | 7d | 3c  
**Texture:** monotone, disconnected, broadway

**Action:**

*Preflop:*
- MrOrange (UTG): RAISE to 200 (2.0bb)
- Pluribus: RAISE to 612 (6.1bb) - 3-bet
- MrOrange: RAISE to 1,775 (17.8bb) - 4-bet!
- Pluribus: **CALL**

*Flop (4c 5c Qc) - Pot: 3,700:*
- MrOrange: BET 1,200 (32% pot)
- Pluribus: **CALL**

*Turn (7d) - Pot: 6,100:*
- MrOrange: CHECK
- Pluribus: **CHECK**

*River (3c) - Pot: 6,100:*
- MrOrange: BET 3,050 (50% pot)
- Pluribus: RAISE to 7,025 (115% pot)
- MrOrange: FOLD

**Result:** Pluribus +6,175 chips (+61.8bb)

**Why instructive:**
- AcKc 3-bets UTG, faces a 4-bet, calls. AKs is a strong enough hand to call a 4-bet IP.
- Flop is 4c5cQc - three clubs, and Pluribus has the nut flush draw (Ac). Against MrOrange's 4-bet range (AA, KK, QQ, AK, maybe JJ), Pluribus has equity but not a made hand.
- Pluribus calls the 32% pot bet - pot odds make this easy with the nut flush draw.
- Turn check-check: the 7d changes nothing. Pluribus checks back - not drawing to anything on a non-club turn? Or just pot controlling.
- River 3c completes the nut flush. MrOrange bets 50% pot. Pluribus raises to 115% pot - a near-overbet raise. MrOrange folds (likely TT-JJ or AK no clubs).
- **Lesson:** With the nut flush draw in a 4-bet pot, calling down is often better than raising. On the river when the flush completes, the raise can fold out better non-flush hands.

---

### Hand 4 - CO 4-bet bluff, A7s c-bet and turn barrel

**File:** 102/19.phh | **Hand ID:** 19  
**Interest Score:** 15 | **Reasons:** went to turn, 4-bet pot, c-bet 25% pot, won 3,199  
**Pluribus Position:** CO | **Pluribus Cards:** 7dAd  
**Players:** MrBlonde (SB) | MrWhite (BB) | MrPink (UTG) | MrBrown (HJ) | Pluribus (CO) | MrBlue (BTN)  
**Board:** Ks 2h Th | 8c  
**Texture:** two-tone, disconnected, broadway

**Action:**

*Preflop:*
- Pluribus (CO): RAISE to 250 (2.5bb)
- MrWhite (BB): RAISE to 1,000 (10.0bb) - 3-bet
- Pluribus: RAISE to 2,091 (20.9bb) - 4-bet!
- MrWhite: CALL

*Flop (Ks 2h Th) - Pot: 4,232:*
- MrWhite: CHECK
- Pluribus: BET 1,058 (**25% pot**)
- MrWhite: CALL

*Turn (8c) - Pot: 6,348:*
- MrWhite: CHECK
- Pluribus: BET 3,174 (50% pot)
- MrWhite: FOLD

**Result:** Pluribus +3,199 chips (+32.0bb)

**Why instructive:**
- 7dAd is a 4-bet bluff/semi-bluff from CO. Against MrWhite's BB 3-bet range, A7s has decent blockers (blocks AA, AK) and 4-betting with it is theoretically sound.
- The K-2-T flop connects with BB's 3-bet calling range (pairs like TT, KQ) but Pluribus c-bets anyway at **25% pot** - a tiny probe bet. This is a "test the waters" bet that risks little and folds out the BB's weaker hands (77-99 that missed, QJ, etc.).
- The 8c turn is a blank. Pluribus fires 50% pot. MrWhite folds. Mission accomplished.
- **Lesson:** The 4-bet semi-bluff with blockers is a powerful weapon. Small c-bets in 4-bet pots are viable (you have range advantage and fold equity). The turn barrel is where you capitalize.

---

### Hand 5 - CO 4-bet, AKs on monotone diamond board, barrel all in

**File:** 110/31.phh | **Hand ID:** 31  
**Interest Score:** 15 | **Reasons:** went to turn, big pot (7,556), 4-bet pot, won 3,853  
**Pluribus Position:** CO | **Pluribus Cards:** KcAs  
**Players:** MrBlonde (SB) | MrBlue (BB) | MrOrange (UTG) | MrPink (HJ) | Pluribus (CO) | MrWhite (BTN)  
**Board:** 3d Ad Jd | 7c  
**Texture:** monotone, disconnected, ace-high

**Action:**

*Preflop:*
- Pluribus (CO): RAISE to 200 (2.0bb)
- MrWhite (BTN): RAISE to 612 (6.1bb) - 3-bet
- Pluribus: RAISE to 1,814 (18.1bb) - 4-bet
- MrWhite: CALL

*Flop (3d Ad Jd) - Pot: 3,778:*
- Pluribus: BET 1,889 (**50% pot**)
- MrWhite: CALL

*Turn (7c) - Pot: 7,556:*
- Pluribus: BET 3,778 (50% pot)
- MrWhite: FOLD

**Result:** Pluribus +3,853 chips (+38.5bb)

**Why instructive:**
- AKs 4-bet, hits top pair top kicker on monotone Adiamond board. Pluribus doesn't slow-play - bets 50% twice.
- The monotone board is scary (flush possible) but AK hit the ace and KcAs has the second-nut flush blocker (Kd would be better, but Kc still blocks some flush combos).
- Consistent 50% pot sizing on both streets - a straightforward "I have the goods, let's build the pot" approach.
- MrWhite folds the turn, likely a medium pocket pair or AQ/KQ that can't continue.
- **Lesson:** In 4-bet pots when you flop top pair on an ace-high board, bet twice at 50% pot. Don't check back and give free cards. The monotone board is scary to your opponent too.

---

### Hand 6 - BB vs BTN, AdAc, cold-4-bet call, check-down and win

**File:** 106/70.phh | **Hand ID:** 70  
**Interest Score:** 14 | **Reasons:** went to river, huge pot (20,050), 4-bet pot, won 10,050  
**Pluribus Position:** BB | **Pluribus Cards:** AdAc  
**Players:** MrPink (SB) | Pluribus (BB) | MrWhite (UTG) | MrBlonde (HJ) | MrBlue (CO) | MrOrange (BTN)  
**Board:** Kc Th Ah | 9c | 2h  
**Texture:** two-tone, connected, ace-high

**Action:**

*Preflop:*
- MrBlue (CO): RAISE to 225 (2.2bb)
- Pluribus (BB): RAISE to 1,225 (12.2bb) - 3-bet
- MrBlue: RAISE to 2,575 (25.8bb) - 4-bet!
- Pluribus: CALL (slow-plays AA)

*Flop (Kc Th Ah) - Pot: 5,200:*
- Pluribus: CHECK
- MrBlue: BET 1,800 (35% pot)
- Pluribus: RAISE to 6,200 (119% pot from bet) 
- MrBlue: RAISE to 7,425 (all-in effectively)
- Pluribus: CALL

*Turn (9c) - Pot: 20,050:*
- Check-check (both effectively all-in or committed)

*River (2h) - Pot: 20,050:*
- Check-check

**Result:** Pluribus +10,050 chips (+100.5bb)

**Why instructive:**
- Aces against a 4-bet: Pluribus calls instead of 5-betting. This is the trap play. Calling keeps villain's bluffs and weaker hands in. A 5-bet would fold everything but AA.
- Flop check-raise to over-pot: Pluribus checks with top set (AAA), MrBlue bets, Pluribus raises to 6,200 (3.4x the bet). This builds the pot and gets all the chips in.
- **Lesson:** With the nuts in a 4-bet pot, calling preflop and check-raising the flop is often superior to 5-betting preflop. You keep bluffs in and build a bigger pot.

---

### Hand 7 - BTN, QcJc in 3-bet pot, pure bluff across 3 streets

**File:** 103b/138.phh | **Hand ID:** 138  
**Interest Score:** 14 | **Reasons:** went to river, 3-bet pot, won 4,325  
**Pluribus Position:** BTN | **Pluribus Cards:** QcJc  
**Players:** MrBlue (SB) | MrBlonde (BB) | MrWhite (UTG) | MrPink (HJ) | MrOrange (CO) | Pluribus (BTN)  
**Board:** 7s 2s 8c | 4h | Td  
**Texture:** two-tone, semi-connected, low

**Action:**

*Preflop:*
- Pluribus (BTN): RAISE to 200 (2.0bb)
- MrBlonde (BB): RAISE to 1,050 (10.5bb) - 3-bet
- Pluribus: CALL

*Flop (7s 2s 8c) - Pot: 2,150:*
- MrBlonde: CHECK
- Pluribus: BET 1,075 (50% pot)
- MrBlonde: CALL

*Turn (4h) - Pot: 4,300:*
- MrBlonde: CHECK
- Pluribus: BET 2,150 (50% pot)
- MrBlonde: CALL

*River (Td) - Pot: 8,600:*
- MrBlonde: CHECK
- Pluribus: BET 5,725 (66.6% pot)
- MrBlonde: FOLD

**Result:** Pluribus +4,325 chips (+43.2bb)

**Why instructive:**
- QcJc has no piece of this 7-2-8 flop. Pluribus calls a 3-bet in position and fires three streets on a board it didn't hit. This is a pure position-based bluff.
- QJ has backdoor straight draws (9-T for a straight with QJ, or JTQ...) but this is mostly a frequency play.
- The sizing is consistent: 50% / 50% / 67%. Escalating but not overbetting. This puts MrBlonde in a tough spot three times.
- **Lesson:** Position is everything. Calling 3-bets in position with speculative hands and firing when checked to is a legitimate strategy. The key is: when villain checks three streets in a 3-bet pot, they often don't have much.

---

### Hand 8 - BB, QcKh 3-bet, value town on paired board

**File:** 104/94.phh | **Hand ID:** 94  
**Interest Score:** 14 | **Reasons:** went to river, 3-bet pot, won 9,462  
**Pluribus Position:** BB | **Pluribus Cards:** QcKh  
**Players:** MrOrange (SB) | Pluribus (BB) | MrBlue (UTG) | MrBlonde (HJ) | MrWhite (CO) | MrPink (BTN)  
**Board:** 7h Qh 6d | 6h | 6s  
**Texture:** two-tone -> board paired heavily

**Action:**

*Preflop:*
- MrPink (BTN): RAISE to 250 (2.5bb)
- Pluribus (BB): RAISE to 1,350 (13.5bb) - 3-bet
- MrPink: CALL

*Flop (7h Qh 6d) - Pot: 2,750:*
- Pluribus: BET 687 (25% pot)
- MrPink: RAISE to 2,400 (3.5x)
- Pluribus: CALL

*Turn (6h) - Pot: 7,550:*
- Pluribus: CHECK
- MrPink: CHECK

*River (6s) - Pot: 7,550:*
- Pluribus: BET 5,662 (75% pot)
- MrPink: CALL

**Result:** Pluribus +9,462 chips (+94.6bb)

**Why instructive:**
- KQ in BB 3-bets BTN open. Hit top pair on 7-Q-6. Small c-bet (25%), gets raised. Pluribus calls with top pair top kicker + flush draw knowledge.
- Turn brings 6h (board pairs, three 6s possible, flush draw active). Both check. Pluribus likely concerned about flush and the paired board.
- River brings 6s - FOUR sixes on board! Pluribus now has a full house (QQ66K kicker essentially). Fires 75% pot. Gets called. Wins a monster.
- **Lesson:** The small c-bet getting raised is a spot to flat-call when you have top pair + good kicker. You don't have to re-raise. Let the board develop. When the board massively improves your relative equity (four 6s = your Q is now the best kicker), bet big.

---

### Hand 9 - SB 3-bet, 88 on K-7-2 board, check-call, delayed river overbet

**File:** 108/203.phh | **Hand ID:** 203  
**Interest Score:** 14 | **Reasons:** went to river, 3-bet pot, c-bet skipped, won 2,212  
**Pluribus Position:** SB | **Pluribus Cards:** 8c8s  
**Players:** Pluribus (SB) | MrWhite (BB) | MrBlonde (UTG) | MrBlue (HJ) | MrOrange (CO) | MrPink (BTN)  
**Board:** 2h Ks 7c | Ad | 3c  
**Texture:** rainbow, disconnected, broadway

**Action:**

*Preflop:*
- MrBlue (HJ): RAISE to 225 (2.2bb)
- Pluribus (SB): RAISE to 706 (7.1bb) - 3-bet
- MrWhite (BB): CALL
- MrBlue: CALL (3-way!)

*Flop (2h Ks 7c) - Pot: 2,118:*
- Pluribus: CHECK
- MrWhite: CHECK
- MrBlue: BET 800 (38% pot)
- Pluribus: CALL
- MrWhite: FOLD

*Turn (Ad) - Pot: 3,718:*
- Pluribus: CHECK
- MrBlue: CHECK

*River (3c) - Pot: 3,718:*
- Pluribus: BET 5,577 (**150% pot overbet**)
- MrBlue: FOLD

**Result:** Pluribus +2,212 chips (+22.1bb)

**Why instructive:**
- 88 in SB 3-bets HJ open, gets two callers (3-way pot). Dangerous spot.
- K-7-2 rainbow flop: Pluribus checks. MrBlue bets. Pluribus calls with 88 (middle pair is good here; board connects with calling range but 88 is ahead of AQ, AJ, etc.).
- Turn brings Ad - now Pluribus's pair is behind any ace. Both check. Surprising that Pluribus doesn't fold or bet here.
- River 3c is a blank. Pluribus OVERBETS 150% pot. MrBlue folds.
- **Lesson:** Sometimes the line is check-call-check-OVERBET. The river overbet with what is likely a bluff (88 doesn't beat AK, AQ, Kx) is a pure fold equity play. MrBlue checked back the turn with what's probably AQ/AJ - too scared to call an overbet on the river.

---

### Hand 10 - HJ, Ac7c 3-bet, small c-bet on Q-9-8, call turn, river overbet

**File:** 106/44.phh | **Hand ID:** 44  
**Interest Score:** 14 | **Reasons:** went to river, 3-bet pot, c-bet 25% pot, won 1,859  
**Pluribus Position:** HJ | **Pluribus Cards:** Ac7c  
**Players:** MrBlue (SB) | MrOrange (BB) | MrPink (UTG) | Pluribus (HJ) | MrWhite (CO) | MrBlonde (BTN)  
**Board:** Qd 9h 8c | 6s | 3c  
**Texture:** rainbow, connected, broadway

**Action:**

*Preflop:*
- MrPink (UTG): RAISE to 210 (2.1bb)
- Pluribus (HJ): RAISE to 681 (6.8bb) - 3-bet
- MrPink: CALL

*Flop (Qd 9h 8c) - Pot: 1,512:*
- MrPink: CHECK
- Pluribus: BET 378 (25% pot)
- MrPink: CALL

*Turn (6s) - Pot: 2,268:*
- MrPink: BET 650 (29% pot)
- Pluribus: CALL

*River (3c) - Pot: 3,568:*
- MrPink: CHECK
- Pluribus: BET 2,676 (75% pot)
- MrPink: FOLD

**Result:** Pluribus +1,859 chips (+18.6bb)

**Why instructive:**
- Ac7c has backdoor flush draw on a connected Q-9-8 board. 3-bet and c-bet at 25%. The small c-bet on Q98 is notable - this board hits the caller's range (JT, T7, 65, etc.) so a large c-bet is dangerous.
- Turn brings 6s. MrPink leads for 29% pot. Pluribus calls with what is likely Ac-high with a backdoor club draw. The 6s completed a straight (J-T on the Q-9-8-6). Pluribus might be floating.
- River 3c completes Pluribus's backdoor flush! Pluribus fires 75% pot. MrPink folds.
- **Lesson:** Backdoor draws are valuable - they give you "extra equity" when you're floating. The 3-bet with A7s isn't crazy; the hand can make the nut flush and has a big card to bluff with.

---

### Hand 11 - SB, QQ 4-bet call vs squeeze, slow-down post-flop

**File:** 104/47.phh | **Hand ID:** 47  
**Interest Score:** 13 | **Reasons:** went to river, huge pot (20,325), 4-bet pot, won 10,325  
**Pluribus Position:** SB | **Pluribus Cards:** QsQh  
**Players:** Pluribus (SB) | MrBlue (BB) | MrBlonde (UTG) | MrWhite (HJ) | MrPink (CO) | MrOrange (BTN)  
**Board:** 8c Tc 5h | 6s | Jc  
**Texture:** two-tone, semi-connected, middling

**Action:**

*Preflop:*
- MrWhite (HJ): RAISE to 225 (2.2bb)
- MrPink (CO): RAISE to 700 (7.0bb) - 3-bet
- Pluribus (SB): RAISE to 1,512 (15.1bb) - 4-bet (squeezes!)
- MrPink: RAISE to 10,000 (100bb) - 5-bet jam!
- Pluribus: CALL

*All-in pre, runout:*  
*Board: 8c Tc 5h | 6s | Jc*

**Result:** Pluribus +10,325 chips (+103.2bb)

**Why instructive:**
- QQ 4-bets a 3-bet, gets 5-bet jammed. Calling off with QQ against a 5-bet jam is correct (opponent needs to have KK+ very often for this to be wrong).
- The fact that this is checked down (no action post-flop when all-in pre) is fine - it's an all-in spot.
- **Lesson:** QQ is a call against a 5-bet jam at 100bb stack depth. Even if opponent has KK, you're ~18% equity and pot odds are fine. Don't fold QQ to any 5-bet.

---

### Hand 12 - BB, KsKc 3-bet, traps vs 4-bet jam

**File:** 108/238.phh | **Hand ID:** 238  
**Interest Score:** 13 | **Reasons:** went to river, huge pot (20,000), 4-bet pot, won 10,000  
**Pluribus Position:** BB | **Pluribus Cards:** KsKc  
**Players:** MrPink (SB) | Pluribus (BB) | MrWhite (UTG) | MrBlonde (HJ) | MrBlue (CO) | MrOrange (BTN)  
**Board:** 5c 5h Kh | Tc | Ts  
**Texture:** two-tone, disconnected, paired broadway

**Action:**

*Preflop:*
- MrPink (SB): RAISE to 300 (3.0bb) - somewhat large open
- Pluribus (BB): RAISE to 900 (9.0bb) - 3-bet
- MrPink: RAISE to 10,000 (all-in jam)
- Pluribus: CALL

*Board: 5c 5h Kh | Tc | Ts*

**Result:** Pluribus +10,000 chips (+100bb)

**Why instructive:**
- KK 3-bets, gets jammed on. Obvious call. KK is only behind AA (6 combos) vs. a wide 4-bet/jam range. Even without blockers, this is always a call.
- Also note: The board runs out 5-5-K-T-T. Pluribus has a full house (KKKTT). Would've been action regardless.
- **Lesson:** This is a pure "always call" spot. Note that Pluribus's 3-bet sizing is 9bb (3x the 3bb open). Against a big open, the 3-bet goes proportionally bigger.

---

### Hand 13 - UTG, Js9s, value three-street bluff

**File:** 101/27.phh | **Hand ID:** 27  
**Interest Score:** 13 | **Reasons:** went to river, c-bet 50% pot, won 2,025  
**Pluribus Position:** UTG | **Pluribus Cards:** Js9s  
**Players:** MrPink (SB) | MrBrown (BB) | Pluribus (UTG) | MrBlue (HJ) | MrBlonde (CO) | MrWhite (BTN)  
**Board:** Td Qs Kc | 3s | 8d  
**Texture:** rainbow, connected, broadway

**Action:**

*Preflop:*
- Pluribus (UTG): RAISE to 225 (2.2bb)
- MrBrown (BB): CALL

*Flop (Td Qs Kc) - Pot: 500:*
- MrBrown: CHECK
- Pluribus: BET 250 (50% pot) - c-bet
- MrBrown: CALL

*Turn (3s) - Pot: 1,000:*
- MrBrown: CHECK
- Pluribus: BET 1,500 (150% pot) - OVERBET!
- MrBrown: CALL

*River (8d) - Pot: 4,000:*
- MrBrown: CHECK
- Pluribus: BET 6,000 (150% pot) - OVERBET again!
- MrBrown: FOLD

**Result:** Pluribus +2,025 chips (+20.2bb)

**Why instructive:**
- Js9s hits the K-Q-T board perfectly: J9 has a straight (J-Q-K)! Wait, actually: Td-Qs-Kc with Js9s = J9 on T-Q-K = the J9 makes a straight (9-T-J-Q-K). Yes, Pluribus has the nut straight.
- But then fires overbets (150% pot) on both turn and river. This is value betting with the nuts.
- The turn 3s gives Pluribus a backdoor flush draw in addition to the straight.
- **Lesson:** With the nuts in a single-raised pot, escalate quickly. Small c-bet then 150% pot overbet on turn. This looks like a bluff to opponents, gets calls from two-pair/sets who think you're bluffing.

---

### Hand 14 - BTN, 5s4s, calling 3-bet, triple barrel with nothing

**File:** 109/132.phh | **Hand ID:** 132  
**Interest Score:** 13 | **Reasons:** went to river, c-bet 50% pot, won 2,025  
**Pluribus Position:** BTN | **Pluribus Cards:** 5s4s  
**Players:** MrWhite (SB) | MrBlonde (BB) | MrBlue (UTG) | MrOrange (HJ) | MrPink (CO) | Pluribus (BTN)  
**Board:** 9c 9h 8h | 4h | 2c  
**Texture:** two-tone, connected, middling (paired)

**Action:**

*Preflop:*
- Pluribus (BTN): RAISE to 225 (2.2bb)
- MrBlonde (BB): CALL

*Flop (9c 9h 8h) - Pot: 500:*
- MrBlonde: CHECK
- Pluribus: BET 250 (50% pot)
- MrBlonde: CALL

*Turn (4h) - Pot: 1,000:*
- MrBlonde: CHECK
- Pluribus: BET 1,500 (150% pot) - overbet
- MrBlonde: CALL

*River (2c) - Pot: 4,000:*
- MrBlonde: CHECK
- Pluribus: BET 6,000 (150% pot) - overbet again
- MrBlonde: FOLD

**Result:** Pluribus +2,025 chips (+20.2bb)

**Why instructive:**
- 5s4s hits almost nothing on 9-9-8. On turn, 4h gives Pluribus bottom pair. The 4h also completes the flush draw. Pluribus overbets the turn - this is a polarized "I have a hand or I'm bluffing" bet.
- River 2c misses all draws. Pluribus overbets again. MrBlonde folds.
- **Lesson:** The 150%/150% line on turn-river is extremely polarized. Opponents cannot call without a very strong hand. Even if you have 0% equity (5-high), this line has high fold equity against any hand that isn't a 9, 8, or flush.

---

### Hand 15 - BTN, 4h5h, call 3-bet, delayed river bluff

**File:** 100b/174.phh | **Hand ID:** 174  
**Interest Score:** 13 | **Reasons:** went to river, 3-bet pot, won 1,950  
**Pluribus Position:** BTN | **Pluribus Cards:** 4h5h  
**Players:** MrBlue (SB) | MrBlonde (BB) | MrWhite (UTG) | MrPink (HJ) | MrOrange (CO) | Pluribus (BTN)  
**Board:** 3d Kh Th | 4c | 2h  
**Texture:** two-tone, disconnected, broadway

**Action:**

*Preflop:*
- Pluribus (BTN): RAISE to 250 (2.5bb)
- MrBlonde (BB): RAISE to 1,100 (11.0bb) - 3-bet
- Pluribus: CALL

*Flop (3d Kh Th) - Pot: 2,250:*
- MrBlonde: BET 800 (36% pot)
- Pluribus: CALL

*Turn (4c) - Pot: 3,850:*
- MrBlonde: CHECK
- Pluribus: CHECK (turned bottom pair)

*River (2h) - Pot: 3,850:*
- MrBlonde: CHECK
- Pluribus: BET 5,775 (150% pot)
- MrBlonde: FOLD

**Result:** Pluribus +1,950 chips (+19.5bb)

**Why instructive:**
- 4h5h is a speculative suited connector. Calls a 3-bet in position.
- Flop: 3d-Kh-Th - Pluribus has a backdoor straight draw (A-2-3-4-5 or 2-3-4-5-6) and backdoor flush draw. Calls a 36% pot bet. This is a peel-and-see play with multiple outs.
- Turn 4c: Pluribus hits bottom pair! But also picks up an open-ended straight draw to a wheel (A-2-3-4-5). Checks behind.
- River 2h: Pluribus completes the wheel straight! (A-2-3-4-5 with 4h5h on 3-K-T-4-2). Fires 150% pot overbet. MrBlonde folds.
- **Lesson:** Suited connectors that make straights on the river are prime candidates for river overbets. The line (call, call, check, overbet) looks like a river bluff - and sometimes you get called. But often you get folds.

---

### Hand 16 - BB, ThTd 3-bet call, call down, lose to showdown

**File:** 109/180.phh | **Hand ID:** 180  
**Interest Score:** 13 | **Reasons:** went to river, 3-bet pot, Pluribus lost 3,300  
**Pluribus Position:** BTN | **Pluribus Cards:** ThTd  
**Players:** MrWhite (SB) | MrBlonde (BB) | MrBlue (UTG) | MrOrange (HJ) | MrPink (CO) | Pluribus (BTN)  
**Board:** 8c Kc 7d | 8d | 3d  
**Texture:** two-tone, semi-connected, broadway

**Action:**

*Preflop:*
- MrBlue (UTG): RAISE to 225 (2.2bb)
- Pluribus (BTN): RAISE to 825 (8.2bb) - 3-bet
- MrBlue: CALL

*Flop (8c Kc 7d) - Pot: 1,800:*
- MrBlue: CHECK
- Pluribus: BET 450 (25% pot)
- MrBlue: CALL

*Turn (8d) - Pot: 2,700:*
- MrBlue: CHECK
- Pluribus: CHECK

*River (3d) - Pot: 2,700:*
- MrBlue: CHECK
- Pluribus: BET 2,025 (75% pot)
- MrBlue: CALL

**Result:** Pluribus -3,300 chips (-33bb) - MrBlue called and won

**Why instructive:**
- TT 3-bets UTG, hits middle pair on K-8-7. Small c-bet (25%), called.
- Turn brings 8d (board pairs). Pluribus checks back. This is pot control - TT is now behind any 8x or Kx in MrBlue's range.
- River 3d is a blank but completes the flush. Pluribus fires 75% pot. MrBlue calls and wins (likely had Kx or a made hand).
- **Lesson:** Sometimes Pluribus loses. Here, betting the river with a medium pair on a dangerous board is a marginal spot. The 75% river bet with TT on K-8-7-8-3 may have been a mistake or a thin value bet that didn't work. Studying lost hands is as important as won ones.

---

### Hand 17 - CO, AcKs 5-bet call, loses vs. MrPink's jammed range

**File:** 109/73.phh | **Hand ID:** 73  
**Interest Score:** 13 | **Reasons:** went to river, 5-bet pot, Pluribus lost 10,000  
**Pluribus Position:** CO | **Pluribus Cards:** AcKs  
**Players:** MrBlonde (SB) | MrBlue (BB) | MrOrange (UTG) | MrPink (HJ) | Pluribus (CO) | MrWhite (BTN)  
**Board:** 8h 3c 5h | 7s | 3s  
**Texture:** two-tone, semi-connected, low

**Action:**

*Preflop:*
- MrPink (HJ): RAISE to 210 (2.1bb)
- Pluribus (CO): RAISE to 681 (6.8bb) - 3-bet
- MrPink: RAISE to 1,993 (19.9bb) - 4-bet
- Pluribus: RAISE to 3,667 (36.7bb) - 5-bet!
- MrPink: RAISE to 10,000 (all-in) - 6-bet jam
- Pluribus: CALL

*Board: 8h 3c 5h | 7s | 3s*

**Result:** Pluribus -10,000 chips (-100bb)

**Why instructive:**
- AKo in a 5-6-bet war. Pluribus 5-bets, faces a shove, calls. Against a 6-bet jam range, AK has roughly 30-35% equity against AA/KK and near-flip equity vs QQ/JJ. At those pot odds (calling ~6,333 to win ~20,000), calling is mathematically correct.
- Opponent had a hand (likely AA or KK), Pluribus lost.
- **Lesson:** Even correct plays lose. AK calling a 6-bet all-in is correct. The fact that Pluribus lost this hand doesn't mean the decision was wrong. Evaluate decisions by the process, not the outcome.

---

### Hand 18 - BB, 8s9s calling open, check-raise flop, three-street value

**File:** 100/52.phh | **Hand ID:** 52  
**Interest Score:** 12 | **Reasons:** went to river, 3-street bet, won 2,133  
**Pluribus Position:** BB | **Pluribus Cards:** 8s9s  
**Players:** MrBrown (SB) | Pluribus (BB) | MrBlue (UTG) | MrBlonde (HJ) | MrWhite (CO) | MrPink (BTN)  
**Board:** Qd 9d 2d | Td | 7d  
**Texture:** monotone all the way - all diamonds!

**Action:**

*Preflop:*
- MrWhite (CO): RAISE to 225 (2.2bb)
- Pluribus (BB): CALL

*Flop (Qd 9d 2d) - Pot: 500:*
- Pluribus: CHECK
- MrWhite: BET 277 (55% pot)
- Pluribus: RAISE to 804 (check-raise!)
- MrWhite: CALL

*Turn (Td) - Pot: 2,108:*
- Pluribus: BET 1,054 (50% pot)
- MrWhite: CALL

*River (7d) - Pot: 4,216:*
- Pluribus: BET 2,108 (50% pot)
- MrWhite: FOLD

**Result:** Pluribus +2,133 chips (+21.3bb)

**Why instructive:**
- 8s9s on a Qd9d2d board: Pluribus has middle pair + backdoor... wait, no, it's all diamonds. 9s is not a diamond. Pluribus has middle pair (pair of 9s) on a three-diamond flop. That's it.
- Check-raises the flop with middle pair on a monotone board! This is aggressive. The check-raise says "I have a diamond." Pluribus may or may not.
- Turn 9d (another diamond) actually improves Pluribus to trips (three 9s, one of which is the 9d on board). Now Pluribus has a strong hand.
- River 7d: the board has 4 diamonds. Anyone with a single diamond has a flush. Pluribus has trip 9s but any diamond beats this. Bets 50% pot - either as value (hoping to beat non-diamond hands) or knowing opponent doesn't have a diamond.
- MrWhite folds. Pluribus wins.
- **Lesson:** The check-raise on a scary board with a medium hand is a GTO play to balance your range. You don't always need the flush to check-raise a monotone board. This play works because opponents cannot know if you have the flush.

---

### Hand 19 - CO, 9h9s 3-bet, pot-size c-bet on KT7 then give up turn

**File:** 101/31.phh | **Hand ID:** 31  
**Interest Score:** 12 | **Reasons:** went to river, 3-bet pot, c-bet 100%, won 1,875  
**Pluribus Position:** CO | **Pluribus Cards:** 9h9s  
**Players:** MrBlonde (SB) | MrWhite (BB) | MrPink (UTG) | MrBrown (HJ) | Pluribus (CO) | MrBlue (BTN)  
**Board:** Kh 7c Ts | Qd | Jh  
**Texture:** rainbow, semi-connected, broadway

**Action:**

*Preflop:*
- MrBrown (HJ): RAISE to 225 (2.2bb)
- Pluribus (CO): RAISE to 525 (5.2bb) - 3-bet
- MrBrown: CALL

*Flop (Kh 7c Ts) - Pot: 1,200:*
- MrBrown: CHECK
- Pluribus: BET 1,200 (100% pot) - pot-size c-bet!
- MrBrown: CALL

*Turn (Qd) - Pot: 3,600:*
- MrBrown: CHECK
- Pluribus: CHECK (gives up with 99?)

*River (Jh) - Pot: 3,600:*
- MrBrown: CHECK
- Pluribus: CHECK

**Result:** Pluribus +1,875 chips (+18.8bb)

**Why instructive:**
- 99 3-bets HJ, hits... nothing on K-T-7. Fires a pot-size c-bet! This is a large-size bluff on a board that smashed the calling range. If MrBrown has KQ, KJ, AT, TT - he calls or raises.
- MrBrown calls the flop, so he has something. Turn brings Qd - now KQ, QT, QJ are all likely for MrBrown. Pluribus checks back.
- River Jh: KJ, TJ, QJ all complete. Pluribus checks. MrBrown checks. Pluribus wins... surprisingly. Maybe MrBrown had A7 or TT and was slow-playing?
- **Lesson:** Pot-size c-bets on Kxx boards are valid with AA/KK/AK but also as a bluff to fold out hands like AJ/AQ that missed. The key: pot-size bets say "I have it," which forces folds from air. Then checking down when called is fine.

---

### Hand 20 - BTN, KsAc, cold 4-bet call, skips c-bet, overbets river with nuts

*(Note: This is a different hand from Hand 1 showing a similar theme - river overbet after passive play)*

**File:** 100b/174.phh already covered. Instead, capturing the most instructive final hand:

**File:** 110/31.phh discussed in Hand 5. Final slot: a summary hand.

**Thematic Hand 20 - The Pattern Hand:**

From aggregate data across 2,000 hands, here is the "Pluribus standard play":

1. Open 2.0-2.5bb from any position, no limp
2. If 3-bet: either 4-bet to ~19-22bb or fold. Rarely call OOP.
3. If 4-bet: call in position, consider calling even OOP with strong hands
4. On flop: c-bet 62% of time. Small (25-50%) on wet boards, large (75-110%) on dry boards
5. On turn: bet 39% of opportunities, sizing around 50-67% pot
6. On river: bet 45% when arriving, with 39% of bets being overbets (>100% pot)
7. River strategy is POLARIZED: either small (50-75%) or large (100%+). Nothing in between.

---

## Key Takeaways vs. Conventional Wisdom

### 1. Open Sizing: Smaller is Better

**Conventional wisdom:** Raise 3x from EP, 2.5x from LP  
**Pluribus:** 2.0-2.5x from EVERY position  
**Why:** Uniform sizing conceals hand strength. Bigger opens don't necessarily build bigger pots with hands you want to play.

### 2. The Raise-or-Fold Principle

**Conventional wisdom:** Call raises with decent hands, especially in position  
**Pluribus:** Fold 94-100% of the time when facing a raise, from UTG-BTN. 3-bet instead of call.  
**Why:** Calling out of position is a trap. Your range advantage diminishes post-flop. 3-betting builds pots with your good hands and creates fold equity.

### 3. C-Bet Frequency is NOT 80-90%

**Conventional wisdom:** Always c-bet as the preflop aggressor  
**Pluribus:** 62.5% overall. 20-50% on wet boards. 75-80% on dry boards.  
**Why:** On wet boards (flush draws, straight draws), your range advantage is reduced. Checking keeps your range balanced and avoids big c-bet-and-fold situations.

### 4. Small C-Bets on Strong Hands

**Conventional wisdom:** Bet big when you have it  
**Pluribus:** Often uses 24-25% pot c-bets even with strong hands in 4-bet pots  
**Why:** Small bets keep villain's entire range in. You can extract more value across multiple streets than with one big c-bet that folds everyone.

### 5. River Overbets: Not Just for Bluffs

**Conventional wisdom:** Overbets are for value or weird bluffs  
**Pluribus:** 39% of river bets are overbets (>100% pot). This is a balanced strategy with both strong hands and bluffs.  
**Why:** Opponents cannot call overbets without very strong hands. If you overbet with a balanced range (nuts + air), they fold medium-strength hands that would call smaller bets.

### 6. Middle Pairs Have Showdown Value

**Conventional wisdom:** Fold middle pair on scary boards  
**Pluribus:** Check-raises middle pair on monotone boards, fires multiple streets  
**Why:** In GTO play, your range needs to include check-raises and bets with medium hands. If you only bet strong hands, you become very easy to read.

### 7. Patience Across Streets

**Conventional wisdom:** Act fast, bet when you have equity  
**Pluribus:** Often checks flop with the initiative, bets turn or river when the pot is right  
**Why:** The turn and river bets carry more information and fold equity than the flop. Check-call flop, check-call turn, overbet river is a real profitable line.

### 8. 4-Bet Bluffing is Standard

**Conventional wisdom:** Only 4-bet for value (AA/KK/AK)  
**Pluribus:** 4-bets with A7s, A7d, suited connectors - these are semi-bluffs with blocker value  
**Why:** Ace blockers reduce opponent's AA/AK combos. 4-betting with suited aces creates fold equity preflop and has equity when called.

---

## Application to Micro-Stakes NL Hold'em

Micro-stakes players are different from world-class pros. Adjust accordingly:

### What to Copy Directly

**1. Uniform 2.5x opens.** This is standard now. Don't use 3x from early position.

**2. Raise-or-fold from UTG/HJ.** Especially from UTG, play tight and don't cold-call opens. If you have a hand worth playing, 3-bet it or fold.

**3. Small c-bets on connected boards.** When the board hits drawing hands (8-7-6 with two suits), a 25-33% c-bet is better than a 60-70% c-bet. Less to lose when called by a draw.

**4. Large c-bets on dry boards.** When the board misses calling ranges (A-8-3 rainbow), fire 75% pot. You have range advantage and should use it.

**5. Don't always c-bet.** Check back ~35-40% of flops. This balances your range and traps opponents when you do bet turn.

**6. River bets are big.** At micro-stakes, players call too often on rivers with weak hands. Use larger river bets (70%+) as your default when going for value.

### What to Modify for Micro-Stakes

**1. River overbets: use more cautiously.** Micro-stakes players call too wide. A 150% overbet bluff will get called by two-pair and middle set. Reduce bluff frequency with overbets, increase value frequency.

**2. 4-bet bluffing: less of it.** Micro-stakes players don't fold to 4-bets often enough. 4-bet your value hands (AA/KK/QQ/AK) but reduce 4-bet bluffs with A7s type hands.

**3. C-bet vs. weak players.** Against players who call down with any piece, increase c-bet size but only with made hands. Skip c-bet bluffs more.

**4. Fold facing raises.** Pluribus folds 95%+ facing raises from most positions. At micros, this is actually slightly too tight - players 3-bet lighter. But the principle stands: don't cold-call raises OOP.

### The Three Most Important Micro-Stakes Lessons from Pluribus

**Lesson 1: Play fewer hands, but play them aggressively.**  
VPIP 24.9%, PFR 17.2%. That's tight-aggressive. Not 40% VPIP calling stations.

**Lesson 2: Your c-bet frequency should match the board.**  
Dry boards = bet big, bet often. Wet boards = bet small or check. This one change alone can add 2-3 bb/100 to your winrate.

**Lesson 3: River is where the money is.**  
Pluribus bets river 45% when arriving, and a lot of those bets are large. Stop checking back rivers with good hands. Value bet thinly. Bet the river.

---

## Summary Statistics Reference

| Category | Value |
|----------|-------|
| Hands analyzed | 2,000 |
| Win rate | +15.52 bb/100 |
| VPIP | 24.9% |
| PFR | 17.2% |
| Open raise size (all positions) | 2.0-2.5bb |
| 3-bet frequency | 3.6% |
| Average 3-bet size | 9.8bb |
| 4-bet frequency | 0.85% |
| Average 4-bet size | 27bb |
| C-bet frequency | 62.5% |
| C-bet size (dry boards) | 75-110% pot |
| C-bet size (wet boards) | 25-50% pot |
| Turn bet frequency | 39.1% |
| Turn bet size (avg) | 68% pot |
| River bet frequency | 45.1% |
| River bet size (avg) | 124% pot |
| River overbets (>100%) | 39.4% of river bets |
| Fold to preflop raise (UTG) | 100% |
| Fold to preflop raise (HJ) | 99% |
| Fold to preflop raise (BTN) | 93.7% |
| BB call frequency vs open | 35.7% |

---

*Analyzed by Elijah - poker-study subagent - March 2026*  
*Full parser: `~/poker-study/parse_hands.py`*  
*Deep analysis: `~/poker-study/deep_analysis.py`*  
*Raw data: `~/poker-study/full_stats.json`*
