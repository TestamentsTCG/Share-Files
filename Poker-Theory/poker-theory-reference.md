# Poker Theory & Mathematics: Comprehensive AI Reference

**Purpose:** Training reference for a poker-playing AI in Heroes of Holdem (blockchain TCG/poker/RPG).
**Scope:** First principles through advanced GTO theory.
**Format:** Every concept includes definition, formula, and worked example.

---

## Table of Contents

1. [Foundational Mathematics](#1-foundational-mathematics)
2. [Core Strategy Framework](#2-core-strategy-framework)
3. [Hand Reading & Ranges](#3-hand-reading--ranges)
4. [Bet Sizing Theory](#4-bet-sizing-theory)
5. [Postflop Play](#5-postflop-play)
6. [Tournament Concepts](#6-tournament-concepts)
7. [Book Summaries & Key Lessons](#7-book-summaries--key-lessons)
8. [GTO & Solver Era](#8-gto--solver-era)
9. [HoH-Relevant Applications](#9-hoh-relevant-applications)

---

# 1. Foundational Mathematics

## 1.1 Pot Odds

**Definition:** Pot odds are the ratio of the current pot size to the cost of a call. They express the minimum equity your hand needs to make a call profitable (break-even).

**Formula:**
```
Pot Odds (ratio)  = Pot Size : Call Amount
Pot Odds (%)      = Call Amount / (Pot Size + Call Amount)
Required Equity   = Call Amount / (Pot + Call Amount)
```

**Worked Example 1 (Basic):**
- Pot: $100
- Villain bets: $50
- You must call $50 into a pot that will be $150 after your call.

```
Required Equity = 50 / (100 + 50 + 50) = 50 / 200 = 25%
```

If your hand has more than 25% equity vs villain's range, the call is profitable. If less, fold.

**Worked Example 2 (Full NL game):**
- Pot: $200, villain shoves $300 on the river.
- New pot if you call: $200 + $300 + $300 = $800
- Required equity: $300 / $800 = 37.5%

If you hold the second-nut flush and villain can only have the nut flush or a bluff, and you estimate they bluff 45% of the time, your equity vs their range exceeds 37.5%, so you call.

**Converting pot odds to a percentage:**
- 2:1 pot odds = call $1 to win $2 = 33% equity needed
- 3:1 pot odds = call $1 to win $3 = 25% equity needed
- 4:1 pot odds = call $1 to win $4 = 20% equity needed
- 1:1 pot odds (calling a pot-size bet) = 50% equity needed

**Key Principle:** Pot odds only tell you the break-even point for THIS street. They do not account for future betting.

---

## 1.2 Implied Odds

**Definition:** Implied odds extend pot odds by factoring in money you expect to win on future streets if you hit your draw. They matter most when calling draws.

**Formula:**
```
Implied Pot Odds = (Current Pot + Expected Future Winnings) : Call Amount
Required Equity (implied) = Call / (Pot + Call + Expected Future Wins)
```

**When Implied Odds Are High:**
- Drawing to the nuts (villain can't beat you if you hit)
- Deep stacks (more money behind to extract)
- Villain likely to stack off with second-best hand
- Hidden draws (e.g., flopped bottom set, backdoor flush draws)

**When Implied Odds Are Low:**
- Drawing to non-nut hands (someone may have you beat even when you hit)
- Shallow stacks (little money behind)
- Transparent draws (villain will know you hit and fold)
- Drawing to a flush when paired board = risk of full house for villain

**Worked Example:**
- Pot: $50. Villain bets $25. You have a gutshot straight draw (4 outs).
- Call amount: $25. New pot: $100.
- Pot odds alone: 25/100 = 25% equity needed.
- Your equity with a gutshot on the flop (with two cards to come): ~17% (precise) or 8+8=16% (2/4 rule).
- Pure pot odds say FOLD (17% < 25%).

Now add implied odds:
- You have $500 effective stacks. If you hit your gutshot, villain will pay you off $200 more.
- Adjusted pot: 50 + 25 + 25 + 200 = $300.
- Adjusted equity needed: 25/300 = 8.3%.
- Your equity (17%) >> 8.3%, so you CALL based on implied odds.

**Reverse Implied Odds:** When hitting your draw could still lose to a better hand. Example: Drawing to a flush on a paired board where villain may have a full house. This reduces your effective implied odds.

---

## 1.3 Equity

**Definition:** Equity is your share of the pot if the hand were run out to completion with no more betting. Expressed as a percentage.

**Hand vs. Hand Equity (exact):**
- AhKh vs 7c7d preflop: AKs is approximately 46% equity, 77 is approximately 54%.
- AA vs KK: AA is ~82% equity.
- Flush draw (9 outs) vs top pair on flop: ~35% equity (both cards to come).

**The 2/4 Rule (approximation):**
```
Outs × 2 = approximate equity for ONE more card (turn or river only)
Outs × 4 = approximate equity with TWO cards to come (flop to river)
```

Examples:
- Flush draw (9 outs): 9×2 = 18% per card, 9×4 = 36% with two cards (precise: 34.97%)
- Open-ended straight draw (8 outs): 8×4 = 32% (precise: 31.5%)
- Gutshot (4 outs): 4×4 = 16% (precise: 16.47%)
- Two overcards (6 outs): 6×4 = 24% (precise: 22.6%)

**Common Outs Table:**
```
Draw Type                  | Outs | Turn % | Turn+River %
---------------------------|------|--------|-------------
Flush draw                 |  9   | 19.1%  | 34.97%
Open-ended straight draw   |  8   | 17.0%  | 31.45%
Two overcards              |  6   | 12.8%  | 22.60%
Gutshot straight           |  4   |  8.5%  | 16.47%
One overcard               |  3   |  6.4%  | 12.49%
Pocket pair to set         |  2   |  4.3%  |  8.42%
Inside straight + flush    | 12   | 25.5%  | 45.00%
Flush + overcard           | 12   | 25.5%  | 45.00%
Flush + open straight      | 15   | 31.9%  | 54.10%
```

**Equity vs. Ranges (more realistic):**
Rather than hand vs. hand, real poker requires calculating equity vs. a range of hands.

Example: You hold AsKs on a Qs-7h-2c flop.
Villain's range: TT, JJ, QQ, KK, AA, AK, KQ, AQ, bluffs.

Your equity against each part of their range:
- vs QQ: ~14% (they flopped top set)
- vs KK: ~28% (you have two overcards + potential)
- vs AA: ~25%
- vs AQ: ~27%
- vs KQ: ~33% (gutshot + backdoor flush)
- vs bluffs (76s, etc.): ~70%

Weight each by combo count and frequency, sum = your equity vs. their full range.

**Equity Realization:**
Not all equity is equal. Equity realization is how much of your theoretical equity you actually capture due to positional advantages, initiative, and hand characteristics.
- In position + initiative: realize close to 100% of equity.
- Out of position + no initiative: may only realize 60-70% of theoretical equity.
- High-card hands (AK) realize equity well; connected small cards often do not.

---

## 1.4 Expected Value (EV)

**Definition:** EV is the average profit or loss of a decision, weighted by probability. It is THE fundamental decision metric in poker.

**Formula:**
```
EV = (P_win × Amount_won) - (P_lose × Amount_lost)
```

**Worked Example 1 (Calling a shove):**
- You have 9d8d on a flop of 7c-6s-2d. Villain shoves $100 into a $100 pot.
- You have 8 outs to the straight (four 5s + four tens).
- Required equity: 100/(100+100+100) = 33.3%
- Your equity: 8 outs × 4 = 32% (approximate), precise ~31.5% with two cards.
- EV of call: (0.315 × $200) - (0.685 × $100) = $63 - $68.50 = -$5.50

Slight negative EV, slight fold. But add implied odds if not all-in...

**Worked Example 2 (Betting):**
- Pot: $200. You're deciding whether to bet $100 as a bluff.
- If you bet and villain folds: you win $200 (the pot).
- If you bet and villain calls/raises: you lose $100.
- Villain's fold frequency: 60%

```
EV(bet) = (0.60 × $200) + (0.40 × -$100)
        = $120 - $40
        = +$80
```

Compare to EV(check) = $0 (you have no showdown value in this example).
Betting has EV of +$80, checking has EV of $0. Bet.

**Worked Example 3 (Multi-way):**
- Pot: $100. You can bet $50. Three players behind.
- Estimate each folds 50% of the time independently.
- P(all three fold) = 0.5 × 0.5 × 0.5 = 12.5%
- P(at least one calls) = 87.5%

The math gets complex in multiway pots, which is why multiway = tighter value requirements.

**Key EV Principles:**
1. Always choose the highest EV action.
2. EV calculations must include ALL possible outcomes (not just best case).
3. Short-term results don't matter; long-run EV accumulation does.
4. EV is not just about one hand - it includes how your play affects future hands (meta-game).

---

## 1.5 Fold Equity

**Definition:** Fold equity is the additional EV gained from the probability that a bet causes your opponent to fold. It's the value of a bluff or semi-bluff beyond raw hand equity.

**Formula:**
```
Fold Equity = P(fold) × Pot Size
Total Semi-bluff EV = Fold Equity + (P(call) × Hand Equity × Pot)
```

**Worked Example:**
- Pot: $100. You have a flush draw (35% equity vs calling range).
- You bet $75. Villain folds 40% of the time.

```
EV if called = 0.35 × ($100 + $75 + $75) - 0.65 × $75
             = 0.35 × $250 - 0.65 × $75
             = $87.50 - $48.75
             = +$38.75

EV if folds = $100 (win pot immediately)

EV(bet) = (0.40 × $100) + (0.60 × $38.75)
        = $40 + $23.25
        = +$63.25

EV(check) = 0.35 × $100 = $35 (rough approximation of showdown equity)
```

Betting is better by $28.25. Fold equity makes semi-bluffs more profitable than pure calls.

**Fold Equity Increases When:**
- Villain has a marginal/medium-strength hand (will fold often)
- Villain is risk-averse (nits, tight players)
- Stack sizes create pressure (big potential loss if they continue)
- Your perceived range is very strong (you have nut advantage)

---

## 1.6 Combinatorics

**Definition:** Combinatorics is the counting of hand combinations. Essential for range analysis because not all hands are equally likely.

**Basic Counting:**
- A deck has 52 cards, 4 suits, 13 ranks.
- Total 2-card combinations from 52 cards = C(52,2) = 1,326

**Paired Hands (pocket pairs):**
- Each pair has 4 suits, so C(4,2) = 6 combinations.
- Example: AA = AhAs, AhAd, AhAc, AsAd, AsAc, AdAc = 6 combos.

**Unpaired Hands (off-suit):**
- Each unpaired offsuit hand = 4 × 3 = 12 combinations.
- Example: AKo = AhKs, AhKd, AhKc, AsKh, AsKd, AsKc, AdKh, AdKs, AdKc, AcKh, AcKs, AcKd = 12 combos.

**Unpaired Hands (suited):**
- Each unpaired suited hand = 4 combinations (one per suit).
- Example: AKs = AhKh, AsKs, AdKd, AcKc = 4 combos.

**Why This Matters:**
```
AKo has 12 combos.
AKs has 4 combos.
Total AK = 16 combos.
75% of AK combos are offsuit.
```

So when villain 3-bets and you think they have AK, they're 3× more likely to have AKo than AKs.

**Blocker Effects on Combos:**
When you hold a card, you remove it from villain's possible holdings.

Example: You hold AhKh. How many AA combos can villain have?
- Normally AA = 6 combos.
- But you hold Ah, so villain can't have Ah.
- Remaining AA combos: AsAd, AsAc, AdAc = 3 combos (50% reduction).

**Starting Hand Frequencies:**
```
Hand Category     | Combos | % of All Hands
------------------|--------|---------------
Pocket pairs      |   78   |   5.88%
Suited connectors |  ~52   |   ~4%
Suited aces       |   48   |   3.62%
AK (any)          |   16   |   1.21%
QQ+              |   18   |   1.36%
JJ+              |   24   |   1.81%
TT+              |   30   |   2.26%
99+              |   36   |   2.71%
```

**Flop Texture and Combos:**
After a flop lands (e.g., Ah-Kd-5c), we can calculate villain's range combos:
- Two-pair (AK): A has 3 remaining, K has 3 remaining = 3×3 = 9 combos of AK
- But wait: if we don't hold any of these cards, villain has 3×3 = 9 combos of AhKd, AhKc, AhKs, AdKd... 

(Exact counting requires accounting for all community cards already dealt.)

---

## 1.7 Probability of Hitting Draws: Precise Math

**From flop to river (two cards remaining):**
```
P(hit at least once) = 1 - P(miss both)
P(miss turn) = (52 - 5 - outs) / (52 - 5)
             = (47 - outs) / 47

P(miss river, given missed turn) = (46 - outs) / 46

P(miss both) = [(47 - outs)/47] × [(46 - outs)/46]
P(hit at least once) = 1 - P(miss both)
```

**Example: Flush draw (9 outs), flop → river:**
```
P(miss turn) = 38/47 = 0.8085
P(miss river | missed turn) = 37/46 = 0.8043
P(miss both) = 0.8085 × 0.8043 = 0.6502
P(hit) = 1 - 0.6502 = 34.97% ≈ 35%
```

The 2/4 rule says 9 × 4 = 36%, very close.

**Precise outs table (flop to river):**
```
Outs | 2/4 Rule | Exact %
-----|----------|--------
 1   |  4%      |  4.26%
 2   |  8%      |  8.42%
 3   | 12%      | 12.49%
 4   | 16%      | 16.47%
 5   | 20%      | 20.35%
 6   | 24%      | 24.14%
 7   | 28%      | 27.84%
 8   | 32%      | 31.45%
 9   | 36%      | 34.97%
10   | 40%      | 38.39%
11   | 44%      | 41.72%
12   | 48%      | 44.96%
13   | 52%      | 48.10%
14   | 56%      | 51.16%
15   | 60%      | 54.12%
```

**Turn to River only (one card):**
```
P(hit) = outs / 46

Flush draw (9 outs): 9/46 = 19.57% ≈ 20%
OESD (8 outs): 8/46 = 17.39% ≈ 17%
Gutshot (4 outs): 4/46 = 8.70% ≈ 9%
```

---

## 1.8 Starting Hand Strength and Preflop Frequencies

**Hand Rankings (best to worst preflop):**
1. AA (82-85% vs random hand)
2. KK (~77%)
3. QQ (~72%)
4. AKs (~67%)
5. JJ (~68%)
6. TT (~63%)
7. AQs (~66%)
8. AKo (~65%)
9. AJs (~65%)
10. KQs (~63%)

**Key Preflop Stats:**
- AA is dealt once every 221 hands (0.45%)
- QQ+ is dealt once every 73 hands (1.36%)
- A premium hand (TT+, AK) comes once every ~20 hands

**Sklansky Hand Groups (classic framework):**
```
Group 1: AA, KK, QQ, JJ, AKs
Group 2: TT, AQs, AJs, KQs, AKo
Group 3: 99, JTs, QJs, KJs, ATs, AQo
Group 4: T9s, KQo, 88, QTs, 98s, J9s, AJo, KTs
Group 5: 77, 87s, Q9s, T8s, KJo, QJo, JTo, 76s, 97s, Axs, 65s
Group 6: 66, ATss, 55, 86s, KTo, QTo, 54s, K9s, J8s, 75s
Group 7: 44, J9o, 64s, T9o, 53s, 33, 98o, 43s, 22, K8s thru K2s
Group 8 (playable in right conditions): A9o-A2o, Q8s, 87o, 76o, T8o, 65o, 54o
```

---

# 2. Core Strategy Framework

## 2.1 Position

**Definition:** Position refers to where you sit relative to the dealer button and thus when you act. Acting later in the hand is a massive structural advantage.

**Position Names (6-max game, 9-handed, left to right):**
- UTG (Under the Gun) - first to act preflop, worst position
- UTG+1, UTG+2
- HJ (Hijack)
- CO (Cutoff) - second-best position
- BTN (Button/Dealer) - best position postflop
- SB (Small Blind) - must act first postflop, second-worst position
- BB (Big Blind) - last to act preflop, first to act postflop (except vs SB)

**Why Position Matters:**
1. **Information advantage:** You see villain's action before deciding.
2. **Pot control:** Can check behind to keep pot small, or bet to build it.
3. **Last action on every street:** Can dictate the size of the pot.
4. **Realize more equity:** Positional advantage increases equity realization by 10-20%.
5. **Bluffing power:** River bluffs are more effective in position.

**Positional Adjustments:**
```
Position | VPIP range | Open raise size | Implied 3bet defend
---------|------------|-----------------|--------------------
UTG      | ~14%       | 2.5-3x          | Tight (best hands only)
HJ       | ~18%       | 2.5x            | Medium
CO       | ~24%       | 2.5x            | Wider
BTN      | ~42%       | 2.2-2.5x        | Widest (position advantage)
SB       | ~30%       | 3x (vs BTN)     | Varies
BB       | DEFEND ~50%| N/A (call/3bet) | Must defend pot odds
```

**Worked Example - Position Value:**
Hand: KdQd. UTG opens to $6, you are on the BTN.

In position, KQs is a clear flat call (excellent connectivity + position).
Out of position (e.g., from SB), KQs becomes a 3-bet or fold due to reduced equity realization.

---

## 2.2 Ranges vs. Specific Hands

**Definition:** Ranges are the complete set of hands a player could hold in a given situation. Modern poker thinks in ranges, not individual hands.

**Why Ranges:**
- You never know villain's exact hand.
- Strategy must work against all possible hands in their range.
- Your actions are interpreted relative to your range, not just your hand.

**Range Notation:**
- AA = only pocket aces
- TT+ = TT, JJ, QQ, KK, AA
- ATs+ = ATs, AJs, AQs, AKs
- ATo+ = ATo, AJo, AQo, AKo
- 76s = exactly 76 suited
- 65s+ = 65s, 76s, 87s, 98s, T9s

**Building a Villain's Range - Example:**
Villain is a 15% VPIP, 12% PFR tight-aggressive player.
They open from UTG to 3x.

Their UTG opening range (~13% of hands):
```
Premium pairs: AA, KK, QQ, JJ, TT (maybe 99)
Nut hands: AKs, AKo, AQs, AQo
Strong suited: AJs, ATs, KQs, KJs
Broader: JTs, maybe QJs
```

This creates a strong, condensed range heavily weighted toward premium holdings.

**Your Own Range:**
Always think about what range you represent with your actions. If you 3-bet from the BB vs a BTN open, your range includes both value hands (QQ+, AK) and bluffs (A5s, suited connectors). This "balanced" range means villain can't exploit you.

---

## 2.3 GTO vs. Exploitative Play

**GTO (Game Theory Optimal):**
A strategy that cannot be exploited regardless of what villain does. A perfect GTO strategy breaks even against any opponent and profits from any deviation from GTO.

**Key GTO Properties:**
1. Makes opponent indifferent to calling or folding (at the margin).
2. Uses mixed strategies (sometimes bet, sometimes check with same hand).
3. Maintains balanced value-to-bluff ratios.
4. Not necessarily maximally profitable vs. bad players.

**Exploitative Play:**
Deviating from GTO to maximize profit against specific opponent tendencies (leaks).

Examples:
- Villain never folds to c-bets: Stop bluffing, only c-bet for value.
- Villain folds 70% to river bets: Bluff more at river.
- Villain over-calls draws: Charge more for them.
- Villain always 3-bets your steals: Stop stealing from late position.

**When to Use Each:**
```
GTO: 
- Unknown opponents
- Strong, adaptive opponents
- Studying/learning (GTO is baseline)
- High-stakes where meta-game matters

Exploitative:
- Known fish/rec players with clear leaks
- Live poker with physical reads
- Short-session games (not enough hands to exploit you back)
- When you have strong reads on specific tendencies
```

**The GTO Foundation:**
You must understand GTO before you can deviate from it intelligently. GTO sets the baseline; exploits adjust from that baseline.

---

## 2.4 Bluff-to-Value Ratios

**Definition:** The ratio of bluffs to value bets in your range at any decision point. Getting this ratio right makes you unexploitable.

**The Core Math:**
If you bet $X into a pot of $P, villain needs P+X equity to call profitably. They will call if your bluff frequency is high enough to make calling profitable.

**Optimal Bluff Ratio by Bet Size:**
```
Bet Size (pot%) | Value : Bluff ratio | Bluff % of range
----------------|---------------------|------------------
33% pot         | 2:1                 | 33%
50% pot         | 1.5:1               | 40%
75% pot         | 1.25:1              | 44%
100% pot        | 1:1                 | 50%
150% pot        | 0.75:1              | 57%
200% pot        | 0.67:1              | 60%
```

**Worked Example:**
You bet $100 into a $100 pot on the river. Villain gets 2:1 odds (33% equity needed).
For villain to be indifferent, you must bluff exactly 1 time for every 2 value bets.
Your range should be 33% bluffs, 67% value.

If you bluff MORE than 33%: villain profits by always calling.
If you bluff LESS than 33%: villain profits by always folding (you over-fold as a result).

**Why This Matters in Practice:**
River spots require constructing bluffing ranges deliberately. Don't randomly pick hands to bluff - use blockers and hands that can't win at showdown.

---

## 2.5 Continuation Betting (C-Bet)

**Definition:** A bet made on the flop by the preflop aggressor (the raiser). "Continuing" the story of preflop strength.

**C-Bet Sizing Guidelines:**
```
Board Type           | Sizing    | Reason
---------------------|-----------|-------
Dry/Disconnected     | 25-40%    | Low equity for draws, no need to charge
Wet/Coordinated      | 50-75%    | Charge draws, protect equity
Paired boards        | 33-50%    | High board interaction, often check back
Monotone boards      | 33-50%    | Check back often; nut advantage shifted
High card boards     | 33-50%    | Strong range interaction
```

**C-Bet Frequency (GTO approximations):**
- IP (in position) c-bet frequency: ~55-65%
- OOP c-bet frequency: ~45-55%
- 3-bet pots (IP): ~55-70%
- 3-bet pots (OOP): ~35-50%

**Board Texture Impact:**
- A-high dry board (A72r): Heavy c-bet advantage for PFR (range hits this board well).
- Low coordinated board (765): Defender's range benefits; PFR should check more.
- K-high board: Middling; depends on position and exact ranges.

**When to NOT C-Bet:**
1. Board smashes caller's range more than raiser's range.
2. Four or more players in the pot (risk too high, many hands to beat).
3. You have showdown value (thin value) on wet boards.
4. Your range advantage is minimal.

**Worked Example:**
You open BTN with AhJh, BB defends. Flop: Kd-8h-2c (dry).

This board is great for a c-bet:
- AJ has backdoor flush draw + overcards.
- Villain's BB defense range has many hands that miss this K-high board.
- A 33% pot c-bet gets folds from 55, 44, 33, 22 miss, 76, etc.
- If called, you have 6 outs to improve.

---

## 2.6 Check-Raising

**Definition:** Checking to your opponent, then raising when they bet. A powerful weapon used for value and as a bluff.

**When to Check-Raise for Value:**
1. You have a very strong hand that benefits from building the pot.
2. You're OOP and need to deny opponent's equity realization.
3. The board is wet enough that villain will c-bet wide.
4. You want protection AND value (e.g., top set on a flushy board).

**When to Check-Raise as Bluff:**
1. You have strong equity (semi-bluff with flush/straight draws).
2. The board is drawy (villain will fold many hands without pair+draw).
3. You have fold equity + backup equity.
4. You can represent a very strong range.

**Check-Raise Frequency:**
GTO check-raise frequencies on common flop textures:
- Very wet board (9s8s7c): OOP player c/r ~25-35% of range.
- Dry board (Ah7d2c): OOP player c/r ~5-10% of range.
- Paired board (Ks Kh 3d): OOP player c/r ~5-8% of range.

**Check-Raise Sizing:**
- Against a 33% pot c-bet: Raise to ~2.5-3x (making the pot ~9x the c-bet).
- Against a 50% pot c-bet: Raise to ~2.5x.
- Against a 75% pot c-bet: Raise to ~2-2.5x.
- Larger raises = more polarized range required.

**Worked Example:**
Pot: $20. You check OOP, villain bets $7 (35% pot). You check-raise to $22.

Villain must now call $15 more into a $42 pot = 26% equity needed.
If villain calls, they're committed to a high-SPR situation with likely a medium-strength hand.
Your check-raise range should include: top two pair, sets (for value), combo draws, flush draws (semi-bluff).

---

## 2.7 Donk Betting

**Definition:** Betting into the preflop aggressor from out of position before they have a chance to c-bet. Traditionally considered a mistake; modern theory has rehabilitated it.

**Classic View (wrong):** Donk betting is always bad - you give up the chance to check-raise and don't build the pot efficiently.

**Modern View (nuanced):** Donk betting is correct in specific spots:
1. When the board heavily favors the defender's range.
2. When your range has a significant nut advantage on the current board.
3. To protect equity when OOP.

**Example of Correct Donk Bet:**
You defend BB against BTN open. Flop: 8d-7h-2s. You donk bet.
- Your BB calling range contains many 8x, 7x, 87, 76, 65 hands.
- BTN's opening range has fewer 8x, 7x holdings.
- You have range advantage on this board; leading out exploits this.

**Example of Incorrect Donk Bet:**
You defend BB. Flop: Ah-Kd-Qc. You donk bet.
- BTN's range DESTROYS this board (AK, AQ, KQ, sets, AA, KK, QQ).
- Donk betting here loses you value (you won't get enough folds from their range) and looks polarized with little backup.

---

## 2.8 Probe Betting

**Definition:** A bet made by the out-of-position player on the turn (or river) after the in-position player checked behind on the previous street.

**When to Probe Bet:**
- IP player checking back the flop signals weakness/pot control.
- OOP player should now take the betting lead with their strong hands and some bluffs.
- Probe bet range: medium-strong made hands, draws, and hands that benefit from fold equity.

**Sizing:** Usually 50-75% of pot. Large enough to charge draws and get value.

**Logic:** When villain checks back IP, they're often holding medium-strength hands (second pairs, draws, weak top pairs). Leading out with a probe bet denies their free card and denies equity.

---

## 2.9 3-Betting, 4-Betting, 5-Betting

**Definitions:**
- 3-bet: A re-raise over an initial raise (preflop: open-raise counts as 2-bet, so 3-bet is the first re-raise).
- 4-bet: Re-raise over a 3-bet.
- 5-bet: Re-raise over a 4-bet (usually shove or near-shove territory).

**3-Bet Ranges by Position (6-max NL, 100BB):**
```
Position    | Vs BTN Open       | Vs EP Open
------------|-------------------|----------
BTN (vs CO) | QQ+, AK + bluffs  | QQ+, AK
CO (vs HJ)  | KK+, AK           | QQ+, AK
SB (vs BTN) | TT+, AKs + bluffs | QQ+, AK
BB (vs BTN) | TT+, AQs+ + bluffs| QQ+, AK
```

**Balanced 3-Bet Construction:**
A balanced 3-bet range has:
1. Value hands: QQ+, AK (always 3-bet for value)
2. Bluffs: Hands with blockers + playability (A2s-A5s, K5s, K4s, QJo)

Why A2s-A5s as bluffs? They have an ace blocker (reduces villain's AA/AK combos), have suited value (flush equity if called), and can't profitably call (wrong pot odds for implied odds).

**3-Bet Sizing:**
- In position: 3x the open (e.g., open $6, 3-bet to $18)
- Out of position: 3.5-4x (need to compensate for position disadvantage)
- From the blinds vs. late position steal: 3-4x

**4-Bet Ranges:**
When facing a 3-bet, construct a 4-bet range:
- Value: AA, KK (always), QQ (usually), AK (often)
- Bluffs: A5s, A4s (have blockers to AA/AK, surrender playability)
- Flatting range: TT, JJ, QQ (sometimes), AK (sometimes), AQs, KQs

**4-Bet Sizing:**
- IP: ~2.2-2.5x the 3-bet
- OOP: ~2.5-3x the 3-bet
- Example: Villain 3-bets to $18 → 4-bet to $40-45

**5-Bet:**
Almost always a shove or committed shove territory. Range: AA, KK, sometimes QQ.

**Worked Example - 3-Bet Bluff:**
BTN opens $5 (blinds $1/$2). You're in SB with A4s. 3-bet to $17.

- If BTN folds: Win $7 (the original pot). +$7.
- If BTN 4-bets: You fold A4s (it has done its job: won uncontested, or fold to 4-bet).
- If BTN calls: You have position (wait, no - you're SB, they're OOP to you postflop in 3-bet pot... wait, SB is OOP to BTN).
- If BTN calls and you're OOP: You have A4s with backdoor flush potential. C-bet select boards, give up on bad ones.

EV of this 3-bet bluff: Depends on BTN's fold frequency. If BTN folds 50%: EV = 0.5×$7 + 0.5×(call EV) = +$3.50 + call equity.

---

## 2.10 Squeezing

**Definition:** A 3-bet made when there has been an open AND one or more cold callers before you act. The cold callers are "squeezed" - they often cannot call profitably with their flat-calling range.

**Why Squeezing Works:**
1. Cold callers have a capped range (can't have QQ+ - they'd have 3-bet).
2. You need to fold only the original raiser AND all callers.
3. The pot is already larger, making your steal more profitable.
4. Cold callers often fold since they can't call wide with a 3-bet + potential re-raise behind.

**Squeeze Sizing:**
Larger than a standard 3-bet because:
- More players to isolate
- Pot is already bigger
- Formula: ~4-5x the open + (# callers × full open)

Example: UTG opens $6, two callers to you on BTN.
Squeeze to: ~$30-35 (5× the $6 open + accounting for callers in pot).

**Squeeze Bluff Hands:** A2s-A5s (blocker hands), suited hands with playability.

---

## 2.11 Isolation Raising

**Definition:** A raise made to isolate a weak player (limper or weak opener) heads-up.

**When to Iso-Raise:**
- A known fish limps or raises small.
- You have a hand that plays well heads-up.
- You have position on the fish.
- Removing other players from the pot increases your EV.

**Iso-Raise Sizing:**
Larger than standard: 3-4x the limp + 1x per caller.
Example: Fish limps $2, one more limper. Iso to: $2 × 4 + $2 = $10.

**Hand Selection:** Much wider when isolating fish than cold-opening (any two face cards, any pair, suited aces, suited connectors with position).

---

# 3. Hand Reading & Ranges

## 3.1 Preflop Range Construction

**Step 1: Assign a Default Range Based on Position and Action**

Opening ranges by position (approximate, 100BB 6-max NL):
```
UTG (14%): 22+, ATs+, AJo+, KJs+, KQo, QJs
HJ  (18%): 22+, A9s+, ATo+, KTs+, KJo+, QTs+, QJo, JTs
CO  (25%): 22+, A7s+, A9o+, K9s+, KTo+, Q9s+, QJo, J9s+, T9s, 98s
BTN (40%): 22+, A2s+, A7o+, K6s+, K9o+, Q8s+, J8s+, T8s+, 97s+, 87s, 76s, 65s, 54s, some other combos
SB  (30%): Depends heavily on BTN tendencies; typically 22+, A2s+, A5o+, K8s+, K9o+, Q9s+, JTs, T9s
BB  (defend): Very wide vs late position opens; ~48-52% of hands get pot odds to defend
```

**Step 2: Narrow Based on Postflop Action**

Each action narrows the range:
- Check: Removes strongest hands (which would bet for value/protection) and some bluffs.
- Bet: Weighted toward strong hands and bluffs; removes pure checking hands.
- Raise: Removes medium-strength hands; polarized toward nuts and bluffs.
- Call: Removes nuts (would raise) and pure air (would fold); medium-strength hands.
- Fold: Removes all but the folded hand (opponent leaves the hand).

**Step 3: Bayesian Updating**

Every action is new information. Each street, the range gets narrower.

---

## 3.2 How Ranges Narrow Postflop

**Example Hand:**
- BTN opens, BB defends.
- BB's defended range: roughly 37% of hands.
- Flop: Ah-Qd-5c (dry, high).

After villain (BB) checks the flop:
- Removes: AA (would check-raise often but might check), AQ (strong - might c/r), A5 (might c/r)
- Keeps: All missed hands, 55, Q5, KQ, KJ, JJ, TT, 99, some Ax

After villain calls a c-bet:
- Removes: All pure air (would fold)
- Removes: Strongest hands (would raise - sets, two pairs)
- Keeps: Ax (one pair hands), QQ, JJ (slowplays), flush draws (none here), straight draws

After villain checks the turn:
- Further removes: Hands that would lead or check-raise strong.
- Signals: Pot control, medium strength, or trapping.

By the river, villain's range is narrow enough to make precise decisions.

---

## 3.3 Board Texture Analysis

**Board Types:**
```
Type              | Example         | Key Features
------------------|-----------------|-------------------------------
Dry/Disconnected  | A-7-2 rainbow   | Few draws, range polarizing, raiser-favored
Wet/Coordinated   | 9-8-7 two-tone  | Many draws, defender-favored
Monotone          | K-8-3 one-suit  | Flush danger; careful c-betting
Paired            | K-K-7           | Both players have fewer full house combos
Two-tone          | A-J-4 two hearts| Flush draws present; charge more
High-card heavy   | A-K-Q           | Range hits hard; very strong hands dominate
Low-card runout   | 5-4-2           | Small pairs and connectors benefit
```

**Static vs. Dynamic Boards:**
- Static: Board is unlikely to change dramatically on later streets. Example: A-A-K. Equity runs well; less draw potential.
- Dynamic: Board changes meaning significantly on turn/river. Example: 9-8-7. Any 6, T, J, or spade (if two-tone) dramatically changes relative hand strength.

**Nut Advantage:**
The player whose range contains more of the nuts on a given board has nut advantage.

Example: BTN opens, BB defends. Flop: A-2-3 rainbow.
- BTN range contains A2s, A3s, 22, 33, A2o... many of the best hands.
- BB also defends A2s, A3s, 22-33, A4, A5...
- On this board, BB actually has a nut advantage (A4, A5 make the wheel; BTN opens fewer suited aces).
- BB should check-raise more; BTN should c-bet less frequently.

---

## 3.4 Blockers

**Definition:** Blockers are cards in your hand that reduce the probability villain holds certain hands.

**How Blockers Work:**
- If you hold Ah, villain cannot have AhAx, AhKh, AhQh, AhJh, etc.
- If you hold Kh, villain has fewer KK combos (4 → 3 remaining).

**Blocker Uses:**
1. **Bluffing:** Hold blockers to villain's calling hands.
   - Example: River bluff with Ah on a dry board. You block AhAx (some of villain's value range), and if board has a flush draw that missed, you block the nut flush.

2. **Hero-calling:** When you block villain's value hands.
   - Example: You call a river bet holding KcQc on a K-high board. You block KK (villain's nut hand), making it less likely villain has it.

3. **Folding:** Don't always use blockers to call. If villain's bluff range is tiny, blocking their value isn't enough.

**Top Blocker Hands for Bluffing:**
- Ax: Blocks AA, AK, AQ (opponent's value calling hands)
- Ks: Blocks KK, AK
- QQ: Blocks QQ+ (when 4-bet bluffing)
- Suited connectors that missed: Block a completed flush/straight

**Worked Example:**
You're on the river. Board: Ah-Qd-Jh-8s-2h. You have KhTh (missed flush, made straight).
You're considering a bluff.

- You hold Kh: Blocks KhKx (some of villain's nutted hands), and the Kh blocks the nut flush.
- Your KT also completed a King-high straight (K-Q-J-T-9... wait, no T is in your hand, board has Q-J, so K-Q-J-T-8 = the straight).
- But wait: you made the Broadway (A-K-Q-J-T) straight... A is on board, K in hand, Q-J on board... you need T for Broadway. You have T.
- So you actually have a STRAIGHT (Broadway) AND your Kh blocks the nut flush. You should VALUE BET, not bluff.

---

## 3.5 Nut Advantage

**Definition:** One player's range contains a higher proportion of the strongest possible hands (nuts) on a given board. This player should bet more often and for larger sizes.

**How Nut Advantage Affects Strategy:**
- Player with nut advantage: Should bet often, use large sizes (overbets).
- Player without nut advantage: Should check-call more, avoid large bluffs.

**Example:**
BTN vs BB, flop K-K-2 rainbow.

BTN's range: Opens with KK (6 combos), 22 (6 combos), K2s (4 combos).
BB's range: Defends KK (6 combos), 22 (6 combos), K2s (4 combos).

These are similar. But BTN also opens with KJo, KQo, KJs, KQs more often.
Meanwhile BB defends K2o, K3o, K4o (bottom of range Kx hands).

On K-K-2:
- Both have quads/boat potential.
- BTN has more KQ/KJ hands with kicker advantage when both have trips.
- Nut advantage is mild; moderate c-bet frequency appropriate.

Contrast with: BTN vs BB, flop A-2-3 rainbow.
- BTN opens A5s, A4s, A3s, A2s frequently.
- BB defends all these plus A4o-A2o.
- BB actually has MORE A-2-3-wheel combos (A4, A5 make wheel, and BB defends more suited/offsuit ax low cards).
- BB has nut advantage; should check-raise more.

---

# 4. Bet Sizing Theory

## 4.1 Value Bet Sizing

**Goal:** Extract maximum value from worse hands while minimizing losses when behind.

**Principles:**
1. Bet larger when you have a stronger hand vs. villain's range.
2. Bet larger when villain's range is weighted toward calling.
3. Bet smaller when villain's range is mostly folds (you want them to call).
4. Match sizing to the strength of YOUR hand relative to the BOARD.

**Sizing Framework:**
```
Hand Strength vs Range | Board Texture | Sizing
-----------------------|---------------|-------
Nuts on dry board      | Dry           | 50-75% (don't scare away)
Nuts on wet board      | Wet           | 75-100%+ (charge draws)
Strong but not nuts    | Any           | 50-75%
Thin value             | Dry           | 25-40% (maximize calls)
Thin value             | Wet           | Avoid (risk of raise)
```

**Worked Example:**
You have AA on a Kh-7d-2c board. Pot: $50.

Villain likely has: Some Kx, 77, 22, JJ, TT (strong hands they'll call with).
- Sizing: 60-70% pot ($30-35). Large enough to get 2+ streets of value.
- Too small (20%): Villain calls with too many weak hands; you make less money.
- Too large (pot): Villain folds all non-K hands; you lose value.

---

## 4.2 Bluff Sizing

**Principle:** Your bluffs must use the SAME SIZING as your value bets. If you use different sizes, observant opponents can use bet sizing as a tell.

**Why Same Sizing:**
- If you bet small only as bluffs: Villain folds to all big bets, calls all small bets = exploit.
- If you bet large only for value: Villain folds to large bets, calls small bets = exploit.
- Solution: Use same sizing for both value and bluffs at each spot.

**Worked Example:**
You decide to bet 75% pot on the river as your standard size. Your value hands with a 75% bet: top set, nut flush, two pair. Your bluff hands with a 75% bet: missed flush draw, missed straight draw.

Villain sees 75% bet and cannot determine if value or bluff purely from sizing.

---

## 4.3 Geometric Bet Sizing

**Definition:** Geometric sizing maximizes pot growth across multiple streets while using the same percentage of the remaining stack. It solves the problem of "how much to bet to put pressure across all streets."

**Formula:**
If you want to get all-in by the river in 3 streets, geometric sizing means each bet should be the same multiple of the pot.

```
Geometric multiplier = (Final Pot Target / Starting Pot)^(1/n)
where n = number of streets

For flop+turn+river shove:
Each bet should be ~√(SPR) × pot to put maximum pressure.
```

**Simplified Formula:**
For 3 streets with 10x pot to stack ratio:
- Each bet: ~33-40% pot. After 3 bets, entire stack is in.

**Worked Example:**
- $200 pot, $600 stacks. SPR = 3.
- You want to bet flop + shove turn.
- Flop bet: ~75% pot = $150. New pot: $500.
- Turn shove: All-in for ~$450 into $500 = ~90% pot.

This is "geometrically" efficient - each bet represents escalating commitment.

**Easier Rule:** If you want to put all the money in over N streets, make each street bet ≈ pot × [(SPR)^(1/N) - 1].

---

## 4.4 Overbets

**Definition:** Bets larger than the current pot. Used for polarization.

**When to Overbet:**
1. Your range has a significant nut advantage (more very strong hands than villain's range).
2. On blank turn/river cards that don't interact with villain's range.
3. To maximize value when villain has a medium-strength hand they'll pay off.
4. To bluff with maximum fold equity.

**Overbet Ranges (GTO approximate):**
- Value range: Top 15-25% of your continuing range.
- Bluff range: Very specific hands (missed draws, backdoor misses).
- These must be balanced to avoid exploitation.

**Worked Example:**
BTN vs BB. Flop K-5-2r. Turn: 3. River: J.

You hold KK (flopped top set, now full house on a runout with no obvious draws).
River: Overbet 150% pot. Villain's range at this point is mostly Kx, some 55, 22, JJ.
They will call with KQ, KJ, K9 (now two pair with the J river). Your overbet extracts maximum value from their calling hands.

---

## 4.5 Minimum Defense Frequency (MDF)

**Definition:** The minimum percentage of your range you must continue with (call or raise) to prevent opponent from profitably bluffing you with any two cards.

**Formula:**
```
MDF = Pot / (Pot + Bet)
```

**Table:**
```
Bet Size (% of pot) | MDF
--------------------|-----
25%                 | 80%
33%                 | 75%
50%                 | 67%
67%                 | 60%
75%                 | 57%
100%                | 50%
150%                | 40%
200%                | 33%
```

**Worked Example:**
Villain bets $100 into a $100 pot.
MDF = $100 / ($100 + $100) = 50%

You must continue with at least 50% of your range. If you fold more than 50%, villain profits by always bluffing.

**Important Nuance:**
- MDF is a theoretical lower bound based purely on break-even bluff frequency.
- In practice, you call with the hands that have enough equity.
- MDF doesn't tell you WHICH hands to call, only HOW MANY.
- Applied at range level: If villain bets 100% pot, you defend 50% of your range with the hands that have the most equity/showdown value.

---

## 4.6 Alpha (Breakeven Bluff Frequency)

**Definition:** The minimum fold frequency needed for a bet to break even as a pure bluff. Inverse of MDF.

**Formula:**
```
Alpha = Bet / (Pot + Bet)
```

**Table:**
```
Bet Size (% of pot) | Alpha (fold% needed)
--------------------|---------------------
25%                 | 20%
33%                 | 25%
50%                 | 33%
75%                 | 43%
100%                | 50%
150%                | 60%
200%                | 67%
```

**Worked Example:**
You're considering a $75 bluff into a $100 pot.
Alpha = $75 / ($100 + $75) = 43%.

Villain must fold more than 43% of the time for this bluff to profit. If villain folds 55%: EV positive. If villain folds 40%: EV negative.

**Note:** Alpha + MDF = 100%. They are two sides of the same coin.

---

# 5. Postflop Play

## 5.1 Street-by-Street Strategy Differences

**Flop:**
- Most hands are contested; ranges are wide.
- C-bet frequency: moderate (55-65%).
- Sizing: Usually smaller (33-50% pot on dry boards; 50-75% on wet boards).
- Goal: Define ranges, extract early value, deny equity to draws.
- Semi-bluffs are strongest here (two cards to come = maximum fold equity + equity).

**Turn:**
- Ranges have narrowed after flop action.
- Pot has grown; bets are now larger relative to stacks.
- Protect your strong hands (sets, two pairs) more aggressively.
- Bluff frequency: Lower than flop (more commitment required).
- Key decision: Should you bet again (double-barrel) or give up?
- Double-barrel with: Strong hands, nut draws, backdoor equity (backdoor flush that arrived).
- Give up with: Pure air, no equity, no fold equity.

**River:**
- No more cards to come; hands are fully defined.
- Every decision is purely about value vs. bluff.
- No semi-bluffs (no equity if called with a missed hand).
- Value bet with top 35-40% of your range (depending on sizing).
- Bluff with specifically selected hands (using blockers, hands that can't win showdown).
- Sizing: Often larger (67-100% pot) to maximize EV.
- MDF/Alpha fully applicable.

---

## 5.2 Slow Playing

**Definition:** Under-representing hand strength by checking or calling with a strong hand instead of betting/raising. Trapping an opponent.

**When Slow Playing is Correct:**
1. **Villain will bluff if you check:** Strong drawing boards where villain will fire c-bets.
2. **Board is unlikely to improve villain:** You have the nuts on a dry board with few outs.
3. **You need to balance your checking range:** GTO requires strong hands in your check range.
4. **Villain will fold to a raise:** If villain will fold most of their range to a raise, call to keep them in.

**When Slow Playing is Wrong:**
1. **Board is wet:** Many draws that villain could hit cheaply.
2. **Villain won't bluff:** Against passive players, slow playing loses value.
3. **You can build a bigger pot:** If villain will call/raise with many hands.
4. **Risk of being outdrawn is high:** Don't slow play a set on a 4-flush board.

**Worked Example (Correct Slow Play):**
You hold 55 on a A-A-5 board. You flopped a full house.
- Board is very dry (A-A-5 rainbow).
- Villain's range: Any Ax hand will stack off eventually; they will c-bet or bet turns.
- Correct play: Check-call flop, let them bet turns, raise river or call river bet.
- If you raise the flop: Villain folds everything but Ax, losing value from non-Ax hands.

**Worked Example (Wrong Slow Play):**
You hold 99 on a 9h-8h-7d board. You flopped top set.
- Board is extremely wet. Many draws: flush draws, straight draws, combo draws.
- A free card could give villain a flush (9 outs), straight (8+ outs), or both.
- CORRECT: Bet large (75-100%) immediately to deny equity. Don't slow play.
- Wrong: Checking gives villain free cards to outdraw your set.

---

## 5.3 Protection Betting

**Definition:** Betting not primarily for value, but to deny free cards and equity to villain's range.

**When to Protection Bet:**
- You have a strong but vulnerable hand (e.g., top pair on a wet board).
- Villain has many draws in their range.
- SPR is such that you can get it in if villain raises (and you want to).

**Example:**
You hold AhKd on a Kh-9h-8h board. Top pair, top kicker.
But board is monotone with flush draw + straight draw potential.

Protection bet: 75-100% pot. Forces villain to pay with: flush draws (one heart away from flush), straight draws (JT, T7, 76), combo draws.
If you check: Villain draws for free. On the turn, a heart, T, J, or 6 arrives and villain's marginal hand beats yours.

---

## 5.4 Multiway Pot Adjustments

**Definition:** When 3+ players see the flop, strategy changes significantly.

**Key Multiway Adjustments:**
1. **Value requirements increase:** In a 3-way pot, you need stronger hands to bet for value (more hands to beat, more hands that could have you beat).
2. **Bluff frequency decreases:** Bluffs must fold multiple players; success probability drops exponentially (50% × 50% = 25%).
3. **Draw equity decreases:** Your flush draw equity is diluted against multiple hands.
4. **Bet sizing can decrease:** Pot is already larger; smaller bets still charge draws adequately.
5. **Position becomes even more important.**

**Worked Example:**
Three-way pot. You hold Ah-Qh on Kh-Jh-2c.

- You have: Nut flush draw (9 outs) + nut straight draw (AhKhQhJh with T = Royal... actually no. You have AhQh, board shows KhJh2c. You need T for the straight. 4 outs. Plus flush draw 9 outs. Total: ~12 outs? With some overlap.)
- Actually: AhQh gives you top two pair potential... wait, board is K-J-2, you have A-Q, no pair.
- You have: Nut flush draw (9 outs - any heart) + gutshot to Broadway (need T, 4 outs, but some overlap with flush outs).
- Pot: $60 (three-way). Two players to act.

Against one player: 30% pot bet is reasonable to build pot.
Against two players: You risk one folding and one raising, OR both folding (fine) but if one calls and one raises, you're in trouble.
Multi-way recommendation: Check-call if behind, check-raise if you want to semi-bluff both out.

---

## 5.5 Street-by-Street Planning

**Concept:** Before betting, plan your line across ALL three streets. Ask:
1. What will I do on the turn if called? (Various board runouts)
2. What will I do on the river?
3. Am I building toward a natural all-in?

**Example Planning Process:**
- Flop: Ah-9d-3c. You have AA. Villain defends BB.
- Plan: Bet flop (value, protection), bet turn (most cards), bet/shove river.
- Which turn cards slow me down? A or 9 (full house concerns villain?), no. Board is dry.
- Any turn card I slow down on? Maybe a heart-heavy turn (some flush concerns... no it's rainbow flop).
- River sizing: If pot is $200 and stacks are $400 behind, shove river.

**The SPR-Based Decision Tree:**
```
SPR (Stack-to-Pot Ratio) | Implication
--------------------------|------------------
SPR < 2 (shallow)         | Commit with top pair+; many hands stack off
SPR 2-4 (medium)          | Two pair+ typically stack off; one pair needs caution
SPR 4-8 (deep)            | Sets/strong two pair for commitment; one pair = pot control
SPR 8+ (very deep)        | Only very strong hands (sets, nut straights, nut flush) are commitment hands
```

**SPR Formula:**
```
SPR = Effective Stack / Pot Size (after preflop action)
```

---

# 6. Tournament Concepts

## 6.1 ICM (Independent Chip Model)

**Definition:** ICM converts chip stacks into dollar equity based on prize pool distribution. Chips in tournaments are NOT worth their face value in dollars.

**Why ICM Matters:**
- In a cash game, 1 chip = $1.
- In a tournament, doubling your stack does NOT double your equity. The first chip is worth more than the marginal chip (because surviving = cashing).

**ICM Formula (simplified):**
Each player's equity = Sum of (probability of finishing in each position × prize for that position).

**Worked Example (3-player with $100 prize pool: 1st=$60, 2nd=$30, 3rd=$10):**
Player A: 6000 chips
Player B: 3000 chips
Player C: 1000 chips
Total: 10,000 chips

Player A's ICM equity:
- P(A wins) = 6000/10000 = 60% → contributes 60% × $60 = $36
- P(A 2nd) = complex calculation...
- Approximate: A's equity ≈ $45-47 (not $60 which 60% chips would suggest)

**Key ICM Takeaways:**
1. **Avoid losing your stack more than gaining chips.** Winning $500 in chips is worth less than the risk of losing your stack.
2. **Pay jumps are critical.** Near bubbles or pay jumps, survival has massive value.
3. **Short stacks are "free money."** When others are short, you gain equity when they bust without risking chips.
4. **Chip leader should be aggressive but not reckless.** Large stack can apply pressure but shouldn't gamble for marginal EV.

**ICM Pressure:**
Being the chip leader means you exert ICM pressure on smaller stacks. They must fold more than chip EV would suggest, because busting means losing money, while you gain equity from their bust without risking your stack.

---

## 6.2 Push/Fold Strategy

**Definition:** With small stacks (typically < 15-20BB), preflop strategy simplifies to: push all-in or fold. No standard raises.

**Nash Equilibrium Push/Fold Charts:**
These represent the optimal (unexploitable) pushing range vs. any calling range. Approximate:

```
Stack Size | BTN Push Range      | SB Push Range       | Any Position
-----------|---------------------|---------------------|-------------
20BB       | ~35% (88+, AJ+, KQ) | ~40% (77+, AT+, KQ) | Tight
15BB       | ~45% (77+, A7+, K9+)| ~55% (66+, A5+, K8+)| Medium
10BB       | ~70% (all pairs, A-any, KT+, QJ)         | Wider
7BB        | ~90%+               | ~95%+               | Very wide
5BB        | Any two cards from late position           | Push almost any
```

**Calling Ranges (vs. all-in push):**
Tighter than push ranges because you need equity to call.
- BB calling a SB push (10BB): ~TT+, AJ+, ATs
- BTN calling a UTG push: ~JJ+, AK

**Why Push/Fold?**
With < 15BB:
- 3-bet pots become too large relative to stack → no room to maneuver.
- Standard opens lead to forced decisions.
- Push/fold maximizes fold equity while maintaining clear all-in-or-fold framework.

---

## 6.3 Stack-to-Pot Ratio (SPR)

**Definition:** SPR = Effective Stack / Pot after preflop action.

**SPR and Commitment:**
```
SPR | Commitment Threshold
----|---------------------
< 1 | Pot committed; call any reasonable bet
1-2 | Top pair good enough to go with it
2-4 | Top pair is marginal; two pair+ for commitment
4-7 | Two pair marginal; sets/strong draws
7+  | Only nut hands; careful with one and two pair
```

**Worked Example:**
Blinds: $1/$2. BTN opens to $6. BB calls. Pot: $13. Stacks: $200 each.
SPR = $197 / $13 = 15.2 (very deep).

On Kd-9h-3c flop:
- BB checks, BTN bets $8. Pot: $21. BB calls. Pot: $29. Stacks ~$189.
- Turn: 4s. SPR now = 189/29 = 6.5.
- Still quite deep. Two pair+ for heavy commitment.

**SPR as a Planning Tool:**
Before betting, calculate target SPR to determine commitment threshold. If SPR=2 by the river, any reasonable two-pair+ commits.

---

## 6.4 Bubble Play

**Definition:** The bubble is the point where one more elimination means all remaining players cash. ICM pressure is maximized here.

**Bubble Strategy Adjustments:**
1. **Big stacks:** Abuse the bubble. Open very wide; opponents fold to preserve their cashing equity.
2. **Short stacks:** Tighten significantly near the bubble. One mistake = out.
3. **Medium stacks:** Most complex. Balance protecting stack vs. avoiding being blinded out.
4. **Shortest stack at the table:** Your pressure is leveraged by others' ICM concerns more than by your actual stack.

**The "Nash" Bubble Strategy:**
Every player at the table should play "Nash equilibrium" push/fold based on stacks and payout structure. Deviation from Nash costs EV.

**Effective Bubble Factor:**
Some solvers calculate a "bubble factor" multiplier. If the bubble factor is 1.4×, you need 1.4× the chip EV to justify a call (risk tolerance decreases by that factor).

---

## 6.5 Final Table Dynamics

**Pay Jump Awareness:**
Each player who busts increases remaining players' equity. Final table prizes escalate dramatically.

```
Example (9-player FT, $10,000 prize pool):
1st: $3,000
2nd: $2,000
3rd: $1,500
4th: $1,000
5th: $750
6th: $600
7th: $500
8th: $400
9th: $250
```

**Key Final Table Concepts:**
1. **Chip lead is dangerous:** Don't risk chip lead in marginal spots. Loss = catastrophic equity drop.
2. **Pay jump decisions:** Near a pay jump, survival > marginal chip EV.
3. **Short-stack dynamics:** Short stacks are always pushing/folding; others adjust calling ranges.
4. **3-handed and heads-up:** Ranges open dramatically. 3-handed plays like 6-max. HU is extremely wide.
5. **ICM deal-making:** At final tables, players may negotiate deals based on ICM equity. Understanding ICM lets you negotiate fairly.

---

# 7. Book Summaries & Key Lessons

## 7.1 "The Theory of Poker" - David Sklansky

**Core Concept: The Fundamental Theorem of Poker**
"Every time you play a hand differently from the way you would have played it if you could see all your opponents' cards, they gain; and every time you play your hand the same way you would have played it if you could see all their cards, they lose."

**Key Lessons:**

1. **Deception is essential but costly.** Slowplaying and bluffing cost money when they don't work. Only use deception when the long-run EV gain from deception exceeds the short-term loss.

2. **Semi-bluffing is more powerful than pure bluffing.** A semi-bluff (bet with a draw) wins two ways: fold equity + hit equity. Pure bluffs only win when villain folds.

3. **Free cards are dangerous.** When a player bets to deny a free card, they're protecting their equity. Allowing a free card is sometimes correct (to induce bluffs or balance range) but usually costly.

4. **The Balancing Act.** Play straightforwardly most of the time; deviate (bluff/slow play) when the meta-game advantage exceeds the tactical cost.

5. **Pot Odds are foundational.** Every calling decision should be viewed through pot odds. If you don't have sufficient equity, fold regardless of how strong your hand "feels."

6. **Position is paramount.** Sklansky emphasizes position as one of the most important structural advantages in poker.

7. **Starting hand selection.** The book's hand rankings (Sklansky groups) are foundational but were developed for limit hold'em; apply with modifications to NL.

**Unique Sklansky Concepts:**
- **The Defensive Bet:** Betting with a medium-strength hand to get a free showdown (opponent calls instead of raising = cheaper than checking and facing a bet).
- **Value of Deception:** Sometimes deliberately playing sub-optimally to confuse opponent's future decisions. The value must exceed the cost.

---

## 7.2 "Harrington on Hold'em" - Dan Harrington

**Core Framework: M-Ratio (The Harrington M)**
```
M = Stack Size / (Small Blind + Big Blind + Antes)
M = How many rounds until you're blinded out
```

**M-Zones:**
```
Zone       | M Value | Strategy
-----------|---------|-------------------------------
Green      | M > 20  | Full game; all strategies available
Yellow     | M 10-20 | Moderate pressure; open-raise or fold
Orange     | M 6-10  | Push/fold mode approaching; short-handed strategy
Red        | M 1-5   | Emergency; push or fold immediately
Dead Zone  | M < 1   | Must act immediately; all-in any reasonable hand
```

**Key Lessons:**

1. **M is more relevant than raw chip count.** A 10,000 chip stack means nothing without knowing the blinds.

2. **Effective M in multiway:** Harrington introduces "Effective M" which adjusts M for the number of players at the table.
   ```
   Effective M = M × (Number of Players / 10)
   ```

3. **Q-Ratio (relative chip position):** 
   ```
   Q = Stack / Average Stack
   ```
   Q > 1 = above average; Q < 1 = below average. Combines with M for full picture.

4. **Starting hand adjustments by M:**
   - Green zone: Normal hand selection.
   - Yellow zone: Tighten from early, widen from late.
   - Orange zone: Push/fold wider; look for spots to steal.
   - Red zone: Push with any two cards from late, decent hands from any position.

5. **Tournament progression:** Harrington maps the evolution of tournament play through the levels, emphasizing adaptation at each stage.

6. **Stop and Go:** With a short stack in position, call a bet preflop (instead of shoving), then shove any flop. Forces villain to call with two cards to come (instead of preflop, where they already have a read).

---

## 7.3 "Applications of No-Limit Hold'em" - Matthew Janda

**Core Philosophy: Thinking in Ranges and Frequencies**

Janda's book was among the first to systematically apply game theory to NL hold'em in a practical way.

**Key Concepts:**

1. **The Building Block Approach:** Every poker decision should be analyzed in terms of the overall strategy, not just the specific hand. Ask: "What is my range's strategy here?" not "What should I do with this hand?"

2. **Constructing Balanced Ranges:**
   - Value bets, calls, and bluffs must be balanced at correct ratios.
   - Build ranges top-down: assign strongest hands first, then fill in bluffs.

3. **Range Construction for 3-Bets:**
   - 3-bet range must include both value hands and bluffs.
   - Bluff selection: Hands with blocker value + some equity if called (AX suited low cards).
   - The ratio of value to bluff in 3-bet range depends on sizing.

4. **Bet Sizing and Range Polarization:**
   - When you use large bets, your range should be polarized (strong hands + bluffs; no medium hands).
   - When you use small bets, your range can be merged (include medium hands).
   - This is a foundational GTO principle.

5. **The C-Bet Framework:**
   - C-bet frequency + sizing are linked to board texture and range advantage.
   - Low dry boards: Check more often (defender has range advantage).
   - High dry boards: C-bet more often (aggressor has range advantage).

6. **River Play Fundamentals:**
   - River bluffs must be balanced precisely with river value bets.
   - Use hands that have no showdown value as bluffs.
   - Use blockers to reduce probability villain has calling hands.

7. **Responding to Aggression:**
   - Facing a 3-bet: Your flatting vs. 4-bet range must be balanced.
   - Facing a c-bet: Your calling range must meet MDF requirements.
   - Never overfold to aggression; never underfold.

**Janda's Unique Contribution:**
One of the first books to explicitly discuss bet sizing based on range polarization, and to connect GTO theory with practical poker decisions. A bridge between theory and application.

---

## 7.4 "The Mental Game of Poker" - Jared Tendler

**Core Philosophy: Poker Performance is a Mental Skill**

Tendler applies sports psychology to poker. Most players know the correct play; the problem is executing it under pressure, tilt, variance, and emotional states.

**Key Concepts:**

1. **Tilt:** Emotional disturbance that causes suboptimal play.
   - Types: Bad beat tilt, injustice tilt, mistake tilt, losing tilt, entitlement tilt, desperation tilt.
   - Each type has a specific trigger and solution.

2. **The Learning Model:** Skill acquisition goes through stages:
   - Unconscious Incompetence: Don't know what you don't know.
   - Conscious Incompetence: Know your weaknesses; making mistakes.
   - Conscious Competence: Making correct plays but requiring conscious effort.
   - Unconscious Competence: Optimal play becomes automatic.

3. **The Performance Zone:** There's an optimal emotional/arousal state for poker. Too calm = complacent; too emotional = tilting. Stay in the middle.

4. **Variance and the Long Run:**
   - Accept variance as inherent to poker.
   - Separate short-term results from long-term performance.
   - Track decisions, not results.

5. **Handling Bad Beats:**
   - A bad beat is information: your range was ahead; you got unlucky. That's the game.
   - Emotional response to bad beats is irrational and exploitable.

6. **Injustice Tilt:** The belief that you "deserve" to win when you've been playing well. Poker doesn't owe you wins. Correct play = correct EV; results follow over time.

7. **Stop-Loss:** Set a loss limit per session. If you hit it, stop. Prevents deep tilting.

8. **Pre-Session Ritual:** Prepare mentally before playing. Review concepts, get in the right headspace, set goals.

**Application for AI:** An AI doesn't tilt, but it can have systematic biases equivalent to tilt (overvaluing recent outcomes, anchoring to session results). The lesson: evaluate each decision in isolation based on EV, not recent history.

---

## 7.5 "Poker's 1%" - Ed Miller

**Core Philosophy: Most players have exploitable patterns. Find and fix yours.**

Miller's book focuses on "frequencies" - the concept that exploit in poker comes from playing too often or too rarely in specific spots.

**Key Concepts:**

1. **Frequency-Based Thinking:**
   - Poker mistakes are frequency-based: You call too often, fold too often, bet too often, or too rarely.
   - The GTO frequency for every action exists; deviating = exploitable.
   
2. **The 1% Edge:**
   - The 1% of players who understand frequencies exploit the other 99%.
   - Small frequency adjustments (fold 40% instead of 60% in a spot) generate enormous long-term EV.

3. **Key Frequency Benchmarks:**
   - Defend your BB: More than most players think (40-50% vs. most positions).
   - C-bet frequency: Not every flop (55-65% IP, less OOP).
   - River bluff frequency: Calibrate to bet size (33% bluffs for 100% pot bet).

4. **Hand Ranges as a Baseline:**
   - Miller argues most players play too straightforwardly (tell villain too much with their bets).
   - Introduce frequency variance: Sometimes check strong hands, sometimes bet medium hands.

5. **The Feedback Loop:**
   - Identify your most common mistake frequencies.
   - Fix the largest frequency leaks first (most EV gained per adjustment).
   - Continually refine.

6. **Stack-Off Frequencies:**
   - Miller provides guidance on which hands should commit stacks based on SPR.
   - Many players commit too often with one pair at deep SPR.

---

## 7.6 "Modern Poker Theory" - Michael Acevedo

**Core Philosophy: GTO as the foundation of modern poker strategy**

Acevedo's book is the most technically rigorous GTO text available. It synthesizes solver outputs with theoretical explanations.

**Key Concepts:**

1. **Nash Equilibrium in Practice:**
   - Every NL hand has a GTO solution. Solvers approximate this.
   - GTO is not "the best strategy" against bad players, but it's the baseline.

2. **Betting Frequencies from Solvers:**
   - Solvers show that IP player should bet 55-65% of the time on most boards.
   - OOP should check 55-70% of the time (be the responder).
   - These frequencies change dramatically by board texture.

3. **Node Locking:**
   - In solver analysis, "lock" opponent to a specific strategy to find your best counter-exploit.
   - Example: Lock villain to always-fold to river bets → your optimal response is to bluff very frequently.

4. **Multi-Street Game Trees:**
   - Full GTO analysis spans a game tree with billions of decision nodes.
   - Solvers approximate the solution within this tree.

5. **Solver Outputs vs. Human Application:**
   - Solvers mix strategies (randomize between bet and check with same hand).
   - Humans approximate by using heuristics that replicate the distribution.
   - Example: GTO says "bet QT 40% of the time and check 60%." Human: "I'll bet QT when villain is aggressive, check when they're passive."

6. **Range vs. Hand Decisions:**
   - Acevedo emphasizes that every hand in your range must have a prescribed strategy.
   - You can't just decide hand-by-hand; you must think about range implications.

7. **Preflop Opening Ranges:**
   - Acevedo provides exact GTO opening ranges by position based on solver outputs.
   - These are slightly wider than "traditional" ranges, especially from BTN/CO.

---

## 7.7 "Play Optimal Poker" - Andrew Brokos

**Core Philosophy: Practical application of GTO without requiring solvers**

Brokos ("Foucault" online) bridges GTO theory and practical application for working players.

**Key Concepts:**

1. **Conceptual GTO:** Understanding the WHY behind GTO strategies, not just memorizing solver outputs.

2. **Range Visualization:**
   - Before acting, visualize your ENTIRE range and how it interacts with the board.
   - Ask: "What does my range want to do here?" not just "What should this hand do?"

3. **The Check-Call Range:**
   - OOP player often has a strong check-call range to balance check-raises.
   - Mixing strong hands (calls) with medium hands (calls) creates a balanced calling range.

4. **River Polarization:**
   - On the river, ranges are naturally polarized (strong hands bet; medium hands check).
   - Understanding this helps predict villain's range from their river action.

5. **Applied Balance:**
   - Balance matters more in high-stakes vs. regs (who study and adjust).
   - Against fish, exploitative adjustments outperform balance.

6. **The Concept of "Indifference":**
   - At GTO, good plays make villain indifferent between options.
   - When you bluff at the correct frequency, villain gains 0 EV by always calling or always folding.

---

## 7.8 "The Grinder's Manual" - Peter Clarke

**Core Philosophy: Beating small and mid-stakes poker through solid fundamentals**

Clarke's book targets the working professional poker player and focuses on practical, exploitative strategy.

**Key Concepts:**

1. **The Grinder's Mindset:**
   - Treat poker as a business. Volume + edge = profit.
   - Emotional detachment from results is essential for grinding.

2. **Population Tendencies:**
   - At small stakes, most players have similar exploitable tendencies.
   - These tendencies: fold too much to 3-bets, don't adjust for position, c-bet too often, overfold to river bets.

3. **Exploiting Population Leaks:**
   - Small stakes: Bluff rivers more (population folds too much).
   - Small stakes: Call down tighter vs. rivers (population value-bets more than bluffs).
   - Small stakes: 3-bet wider in position (opens fold too often).

4. **C-Bet Strategy Against Fish:**
   - Fish call too much, fold too little. Result: Bluff c-bets less, value c-bet relentlessly.
   - Against nits: Bluff c-bets more; they fold to any pressure.

5. **Hand History Review:**
   - Clarke's process: Review every session's key hands.
   - Identify spots where you deviated from optimal.
   - Fix leaks systematically.

6. **Bankroll Management:**
   - 30 buy-ins for your stake (risk-averse).
   - Move down when below 20 buy-ins; move up when above 40.
   - Never risk more than 5% of bankroll in one session.

7. **Multi-Tabling Strategy:**
   - Grinding requires volume. Multi-tabling reduces decision time per hand.
   - Reduce tables when in complex spots or tilting.

---

## 7.9 "Mastering Small Stakes No-Limit Hold'em" - Jonathan Little

**Core Philosophy: Simple, exploitative strategies beat small stakes**

Little's book focuses on immediately applicable strategies for beating micro and small stakes games.

**Key Concepts:**

1. **Value Betting Relentlessly:**
   - Small stakes players call too much. Every strong hand should bet for value.
   - Don't slow play; bet 3 streets with strong hands.

2. **Simplified Preflop Ranges:**
   - Don't need complex balanced ranges at small stakes.
   - Open-raise strong hands; fold marginal hands.
   - 3-bet for value (QQ+, AK) much more often than as bluffs.

3. **Postflop Simplification:**
   - C-bet most flops with strong hands and flush/straight draws.
   - Check marginal hands to pot control.
   - Bluff only in clear, high-fold-equity spots.

4. **Avoiding Common Small Stakes Mistakes:**
   - Calling too much (calling stations): Be aggressive, not passive.
   - Bluffing too much: At small stakes, villains don't fold enough for many bluffs to work.
   - Slow playing: Build the pot early; don't wait for the river.

5. **Live Poker Tells:**
   - Little includes a section on using physical tells (betting patterns, timing, physical reads).
   - Apply population-level reads (most players at small stakes have similar patterns).

6. **Hand Selection for Profit:**
   - Play hands that make nut hands (sets, straights, flushes).
   - Avoid dominated hands (KJ vs. KK in villain's range, A7 vs. AK).

---

## 7.10 "Treat Your Poker Like a Business" - Dusty Schmidt

**Core Philosophy: Poker is a skill-based business. Run it like one.**

Schmidt ("Leatherass") was a high-volume online grinder and brings a professional's perspective.

**Key Concepts:**

1. **Hourly Rate Over Win Rate:**
   - Track bb/100 (big blinds per 100 hands) AND hourly rate.
   - Hourly rate = bb/100 × stack size × volume.
   - Optimize both: Higher win rate + higher volume = maximum profit.

2. **Volume is King:**
   - Grinding 100K hands/month builds statistically significant samples.
   - Variance is real; small samples lie. Run the volume.

3. **The Business Model:**
   - Treat buy-ins as operating capital.
   - Track wins, losses, expenses (software, coaching, staking).
   - Set performance metrics and hold yourself accountable.

4. **Game Selection:**
   - Choose tables with the most fish.
   - Avoid tables with strong regs unless your edge is significant.
   - The softest table at your stake is always best.

5. **Move Up, Move Down Decisively:**
   - When you have the edge and bankroll, move up.
   - Don't ego-play above your bankroll.
   - Moving down is not failure; it's smart risk management.

6. **Learning Investment:**
   - Pay for coaching, training sites, books.
   - Every $1 invested in skill development returns multiples.
   - Study off the table; play on the table.

7. **The Mindset of a Professional:**
   - Bad beats are cost of business.
   - Losses are temporary; skill edge is permanent.
   - Think in months and quarters, not sessions.

---

## 7.11 Additional Notable Books

### "Every Hand Revealed" - Gus Hansen
- Real-time hand analysis from a major tournament win.
- Key lesson: Aggressive, position-aware play can overcome wide hand selection if reads are strong.
- Demonstrates LAG (loose-aggressive) strategy in tournament context.

### "The Mathematics of Poker" - Bill Chen & Jerrod Ankenman
- Academic-level mathematical analysis of poker.
- Introduces AKQ game (simplified poker) to demonstrate GTO principles.
- Key lesson: Optimal strategies in simplified models translate to NL hold'em principles.
- Covers bankroll theory, EV calculations, frequency analysis.

### "How to Read Hands at No-Limit Hold'em" - Ed Miller
- Range-based analysis of specific hands.
- Key lesson: Read opponent's hand through logical elimination using range analysis.

### "Thinking in Bets" - Annie Duke
- Decision theory applied to poker and life.
- Key lesson: Decisions should be evaluated on process (correct reasoning) not outcome. Poker is a vehicle for understanding probabilistic decision-making.

### "Crushing the Microstakes" - Nathan Williams
- Practical exploitative strategy for the lowest stakes online.
- Key lesson: At microstakes, play straightforward value poker. Opponents don't fold enough for bluffs.

---

# 8. GTO & Solver Era

## 8.1 What Poker Solvers Are

**Definition:** Poker solvers are computer programs that compute Game Theory Optimal (Nash Equilibrium) strategies for No-Limit Hold'em scenarios. They solve the game tree to find strategies where neither player can unilaterally improve their EV.

**Major Solvers:**
- **PioSOLVER** (most widely used, most accurate): Desktop application. $249-$549. Used by top pros worldwide.
- **GTO+**: Cheaper alternative to Pio. Good for studying and practice.
- **Simple Postflop**: Cloud-based, no download required.
- **Monker Solver**: Handles preflop and multiway better than Pio.
- **Snowie**: First major solver; useful for beginners.
- **ICMIZER**: Specifically for tournament push/fold with ICM.
- **HRC (Hold'em Resources Calculator)**: Tournament ranges and ICM analysis.

**How Solvers Work:**
1. Input: Board texture, position, ranges for each player, bet sizes to consider.
2. Process: Iterative algorithm (usually Counterfactual Regret Minimization/CFR) that reduces regret until strategies converge to Nash Equilibrium.
3. Output: Frequencies for each action (bet, check, raise, fold) for EVERY hand in your range.

**What Solvers Show:**
- At GTO, both players achieve the same EV regardless of opponent's strategy.
- Solvers reveal mixed strategies (e.g., "Bet JTs 55% of the time, check 45%").
- Show how bet sizing affects optimal ranges.
- Reveal which hands make good bluffs vs. value bets.

---

## 8.2 Nash Equilibrium in Poker

**Definition:** A Nash Equilibrium is a set of strategies where no player can improve their EV by unilaterally changing their strategy, given the other player's strategy is fixed.

**Properties:**
1. At Nash Equilibrium, you break even against a perfect opponent.
2. Any deviation from Nash = opponent can exploit you.
3. Against a player already at Nash: No adjustment you make improves your EV.
4. Against a player deviating from Nash: Exploiting their deviation improves your EV.

**In Poker:**
- Nash Equilibrium = GTO strategy.
- Achieving exact Nash equilibrium in NL hold'em is computationally intractable for full game trees.
- Solvers approximate Nash by running until strategies converge (within exploitability threshold).

**The Prisoner's Dilemma of Poker:**
- If both players play GTO, both break even (minus rake).
- If one player plays exploitatively and the other plays GTO, the GTO player is unexploitable but doesn't exploit.
- If one player plays exploitatively correctly and the other plays a weak strategy, the exploitative player wins big.

**Practical Application:**
Against unknown strong players: Default to GTO approximation.
Against known weak players: Deviate to exploit their weaknesses.

---

## 8.3 Mixed Strategies

**Definition:** In GTO, the same hand is sometimes played differently (e.g., sometimes bet, sometimes check). This randomization prevents exploitation.

**Why Mixed Strategies Exist:**
If you always check with Ks-Qs on a K-Q-3 rainbow flop, villain can bet freely knowing you don't have a big hand when you check. But if you sometimes check top two pair, villain can't read your range as easily.

**GTO Mixed Strategy Example:**
With KdQd on K-Q-3r flop as OOP:
- GTO: Check 60% of the time, bet 40% of the time.
- Why? Keeping strong hands in your checking range protects your check.

**How to Implement Mixed Strategies (Humans):**
- Use "mixing rules" based on game situation (time, table dynamics, stack sizes).
- Or: Bet in spots with high protection need; check in spots where you want to induce.
- Or: Purely randomize using clock-second technique (odd = bet, even = check).

**For AI:** Exact mixed strategies can be computed. AI should implement mixed strategies precisely according to solver outputs or approximated GTO solutions.

---

## 8.4 Node Locking

**Definition:** In solver analysis, node locking forces one player to play a specific strategy at a specific decision point. This reveals the optimal counter-strategy.

**Uses:**
1. **Exploit analysis:** Lock villain to always fold to river bets → your optimal response maximizes bluff frequency.
2. **Leak finding:** Lock yourself to your actual strategy → solver shows your mistakes.
3. **Population analysis:** Lock to population tendencies → find optimal exploitative counter-strategy.

**Example:**
You believe live players fold 70% of the time to river bets (over-fold).
Node lock: Set villain's river call frequency to 30% (fold 70%).
Solver output: Your optimal river bluffing frequency skyrockets vs. this population.

---

## 8.5 How GTO Changed Modern Poker

**Pre-Solver Era (before ~2014):**
- Poker strategy based on intuition, pattern recognition, reads.
- Conventional wisdom: "Always c-bet." "Slowplay big hands." "Never check-raise as a bluff."
- Books like Harrington provided solid frameworks but weren't game-theory-based.

**Solver Revolution (2015-present):**

1. **C-bet frequency decreased:** Solvers showed we should c-bet far less often than traditional wisdom suggested. Checking good hands (to protect range) became standard.

2. **Bluffing frequencies increased (on some boards):** Many players under-bluffed rivers. Solvers revealed the correct river bluff frequency based on sizing.

3. **Small bet sizes revealed:** A 25-33% pot c-bet is often optimal on dry boards (not the traditional 2/3 pot).

4. **Large overbets validated:** Solvers confirmed overbets as correct in nut-advantage spots.

5. **Preflop ranges adjusted:** GTO preflop ranges are wider than traditional charts, especially from BTN/CO.

6. **Check-raising frequency increased:** Solvers showed OOP players should check-raise more aggressively on wet boards.

7. **3-bet bluffing standardized:** Solvers confirmed the value of balanced 3-bet ranges (not just value 3-bets).

**Key Solver-Era Outputs:**
- BTN vs BB, K-8-2r flop: BTN c-bets with ~45% freq, uses small size (25-33%).
- SB 3-bet pot, A-5-2r flop: SB bets very high frequency (80%+) on this board.
- BTN vs BB, 9-8-7 flop: OOP check-raises ~25-30% of range.
- River with nuts on dry board: Often correct to overbet (150%+).

---

## 8.6 Counterfactual Regret Minimization (CFR)

**The Algorithm Behind Solvers:**

CFR is an algorithm that iteratively computes Nash Equilibrium strategies by minimizing "regret" (how much better you could have done with a different strategy).

**How CFR Works:**
1. Initialize random strategies for all players.
2. Play through the game tree millions of times.
3. After each iteration, calculate "regret" for each action (how much more EV you'd have gotten with a different action).
4. Adjust strategy toward actions with positive regret.
5. Repeat until regret converges near zero = Nash Equilibrium.

**Variants:**
- CFR+ (faster convergence)
- Monte Carlo CFR (samples game tree, faster for large trees)
- Discounted CFR

**Why This Matters for HoH AI:**
If building a poker AI from scratch, CFR is the foundational algorithm for solving the game to Nash Equilibrium. Deep learning approaches (like DeepMind's Libratus or Pluribus) also use CFR at their core.

---

## 8.7 Libratus and Pluribus: AI Poker Milestones

**Libratus (Carnegie Mellon, 2017):**
- Beat 4 top human pros in heads-up NL hold'em over 120,000 hands.
- Used Abstraction + CFR algorithm.
- Key innovation: Re-solved game tree after each hand to avoid exploitation.
- Performance: Won by ~$1.7M in chips over 4 professional players.

**Pluribus (Facebook AI + CMU, 2019):**
- Beat top professionals in 6-player NL hold'em.
- First AI to beat multiple humans simultaneously at complex poker.
- Used blueprint strategy (CFR) + real-time search.
- Discovered: Limping is sometimes correct (contrary to conventional wisdom).
- Discovered: Very small c-bet sizes (1/3 pot) frequently optimal.
- Discovered: Multi-frequency mixed strategies necessary for unexploitability.

**Key Takeaways for HoH AI:**
1. CFR-based approaches solve poker; they're the gold standard.
2. Real-time search (re-solving during play) significantly improves performance.
3. AI can discover non-obvious strategies (limping, unusual bet sizes) that are theoretically correct.
4. Even imperfect GTO (abstracted game trees) beats human experts.

---

# 9. HoH-Relevant Applications

## 9.1 Texas Hold'em Complete Rules and Structure

**The Game:**
Texas Hold'em is a community card poker game for 2-10 players. Each player receives 2 private cards (hole cards). Five community cards are dealt face-up. Players make the best 5-card hand from any combination of their 2 hole cards and 5 community cards.

**Structure:**
1. **Blinds Posted:** SB and BB post forced bets.
2. **Preflop:** 2 hole cards dealt; betting round (UTG first, BTN last).
3. **Flop:** 3 community cards; betting round (SB/BB first, BTN last).
4. **Turn:** 4th community card; betting round.
5. **River:** 5th community card; final betting round.
6. **Showdown:** Best hand wins if multiple players remain.

**Hand Rankings (high to low):**
```
1. Royal Flush: A-K-Q-J-T (same suit)
2. Straight Flush: 5 consecutive same-suit cards
3. Four of a Kind: Four cards of same rank
4. Full House: Three of a kind + pair
5. Flush: Any 5 same-suit cards (not consecutive)
6. Straight: 5 consecutive cards (any suit)
7. Three of a Kind: Three cards of same rank
8. Two Pair: Two separate pairs
9. One Pair: Two cards of same rank
10. High Card: No pair/straight/flush
```

**Betting Options:**
- Check: Don't bet (only when no one has bet)
- Bet: Place chips into pot
- Call: Match previous bet
- Raise: Increase previous bet
- Fold: Surrender hand

**Common Game Formats:**
- Cash Game: Chips = real money; can rebuy anytime.
- Tournament: Fixed buy-in, escalating blinds, play until one player has all chips.
- Sit-and-Go: Small tournament (2-9 players) that starts when seats filled.

---

## 9.2 How TCG Elements Could Modify Poker Strategy

**Heroes of Holdem Poker + TCG Hybrid:**
HoH merges Texas Hold'em with trading card game elements. This creates unique strategic considerations.

**Potential Hole Card Bonus Systems:**

*If certain hole cards trigger bonuses (e.g., a "hero card" multiplies pot share):*

1. **Modified Equity Calculations:**
   - If AhKh gives +20% equity bonus, then AhKh has ~82-85% equity instead of ~65% vs 72o.
   - All equity calculations must factor in bonus modifiers.
   
2. **Modified Starting Hand Ranges:**
   - If bonus hands exist, opening ranges shift toward those hands.
   - Example: If any suited connector gives a "combo draw bonus," suited connectors become more valuable.

3. **Bonus Triggers and EV:**
   - If a royal flush bonus multiplies the pot by 10×: The EV of draws to royal flush changes dramatically.
   - Standard pot odds calculations must include "bonus expected value."
   
   ```
   Modified EV = (P_win × Pot × Multiplier) - (P_lose × Investment)
   ```

**Example: Multiplier Calculation**
- Pot: $100. You hold AdJd. Board: Kd-Qd-2c. Flush draw + gutshot (royal flush possible with Td).
- Standard odds: ~20% flush (any diamond), 4% royal flush.
- If royal flush multiplies pot by 10×: 
  ```
  Standard EV: 0.20 × $100 + ... = $20 equity
  Modified EV (royal bonus): 0.04 × $1000 + 0.16 × $100 + ... = $40 + $16 = $56
  ```
  Royal flush bonus nearly triples your equity in this spot.

---

## 9.3 RPG Elements and Poker Strategy

**Character Abilities in HoH:**
If characters have abilities that modify gameplay (e.g., "see one community card before betting," "reduce villain's hand strength"), these create entirely new strategic dimensions.

**Type 1: Information Abilities**
- Seeing a community card early: Dramatically changes flop/turn strategy.
- Equivalent to having a "tell" on the board: adjust ranges to account for known future cards.

**Type 2: Hand Strength Modifiers**
- If a character ability makes a pair count as two pair:
  - All equity calculations shift.
  - One pair hands become premium.
  - Pot odds/calling thresholds change.

**Type 3: Pot Modifiers**
- Abilities that add chips to the pot on certain conditions:
  - Modified pot equity: Include expected pot additions in EV calculations.
  - Strategic targeting: Play hands likely to trigger opponent's "add chips" ability.

**Type 4: Range Restriction Abilities**
- If a hero can "block" certain hand types (opponent can't have flushes):
  - Your bluffing/calling frequencies change dramatically.
  - Flush draws have no value to bluff when opponent is blocked from flushes.

---

## 9.4 Blockchain/NFT Integration and Poker Mechanics

**Unique Card Properties:**
If NFT cards have unique attributes (e.g., "rare" versions with stat boosts):

1. **Value-Modified Cards:** A "rare" Ace that gives +10% pot equity on win.
   - Opens new meta-game: Which rare cards are most valuable?
   - Affects market value of NFT cards based on in-game utility.

2. **Deckbuilding Mechanics:**
   - Pre-match deckbuilding (if applicable) creates pre-game strategy layer.
   - Optimal "deck" construction mirrors poker hand selection principles.

3. **Evolving Card State:**
   - If cards can level up or improve: Long-term strategy across sessions.
   - Decisions today affect future card capabilities.

---

## 9.5 Existing Poker + Card Game Hybrids

**Relevant Precedents:**

1. **Poker Quest:** 
   - PC roguelite combining poker hands with dungeon crawling.
   - Use poker hands to perform combat actions.
   - Lesson: Poker hand frequencies become combat frequency planning.

2. **One Eyed Jack:**
   - Card game where traditional poker hands trigger special abilities.
   - Similar to HoH's potential framework.

3. **Strip Poker Variants:**
   - Modified poker games with alternative stakes/rewards.
   - Demonstrates flexibility of core poker framework.

4. **Casino Wars / Hi-Lo:**
   - Simple card games derived from poker mechanics.
   - Simplified for casual play; lesson: Core poker math (probability, expected value) applies.

5. **Video Poker (Jacks or Better, Deuces Wild):**
   - Single-player poker variant with pay tables.
   - Optimal strategy derived entirely from EV calculations per hand.
   - Strategy changes dramatically with pay table modifications.
   - Lesson for HoH: Every rule change (bonus payout, modifier) requires recalculating EV.

---

## 9.6 AI Architecture Recommendations for HoH Poker AI

**For a Poker AI in the HoH Framework:**

**Option 1: CFR-Based (Pure Game Theory)**
- Compute GTO strategy using CFR algorithm.
- Works for standard poker; requires modification for TCG elements.
- Pros: Provably unexploitable; theoretically optimal.
- Cons: Computationally intensive; requires full game tree knowledge.

**Option 2: Deep Reinforcement Learning**
- Train neural network via self-play (like AlphaGo's approach).
- Reward signal: Chip EV per hand.
- Pros: Handles complex rule modifications naturally.
- Cons: Requires enormous training compute; black box reasoning.

**Option 3: Hybrid (Blueprint + Real-Time Search)**
- Pre-compute GTO blueprint via CFR.
- During play, use real-time search (subgame solving) for specific situations.
- This is how Pluribus works.
- Pros: Best of both; theoretically sound + computationally feasible.
- Cons: Complex implementation.

**Option 4: Rule-Based with Statistical Learning**
- Encode expert poker rules.
- Layer ML for opponent modeling.
- Pros: Interpretable; easier to debug.
- Cons: Rule-based systems are exploitable by smart opponents.

**Recommended Approach for HoH:**
1. Start with a rule-based system implementing this document's principles.
2. Layer in equity calculations for HoH-specific modifiers.
3. Train via self-play to discover emergent strategies.
4. Use opponent modeling to adapt to player tendencies.

---

## 9.7 Core Mathematical Constants for Poker AI

**Pre-computed Values Every Poker AI Needs:**

```python
# PREFLOP HAND EQUITIES (sample - full table in Pokerstove/EquiLab)
hand_equities = {
    "AA_vs_random": 0.852,
    "KK_vs_random": 0.825,
    "QQ_vs_random": 0.800,
    "JJ_vs_random": 0.775,
    "TT_vs_random": 0.750,
    "AKs_vs_random": 0.673,
    "AKo_vs_random": 0.654,
    "72o_vs_random": 0.349,  # worst hand
}

# OUTS TO EQUITY (flop to river, precise)
outs_to_equity = {
    1: 0.0426, 2: 0.0842, 3: 0.1249, 4: 0.1647,
    5: 0.2035, 6: 0.2413, 7: 0.2784, 8: 0.3145,
    9: 0.3497, 10: 0.3839, 11: 0.4172, 12: 0.4496,
    13: 0.4810, 14: 0.5116, 15: 0.5412
}

# MDF BY BET SIZE
def mdf(pot, bet):
    return pot / (pot + bet)

# ALPHA BY BET SIZE
def alpha(pot, bet):
    return bet / (pot + bet)

# REQUIRED EQUITY TO CALL
def pot_odds_equity(pot, call):
    return call / (pot + call)

# EV OF CALL
def ev_call(equity, pot_if_call, call_amount):
    return (equity * pot_if_call) - ((1 - equity) * call_amount)

# COMBO COUNTS
combos = {
    "pocket_pair": 6,    # e.g., AA, KK, 22
    "suited_unpaired": 4, # e.g., AKs
    "offsuit_unpaired": 12 # e.g., AKo
}
```

---

## 9.8 Key Heuristics for Rapid AI Decision-Making

**Quick Reference Decision Framework:**

```
PREFLOP DECISIONS:
1. Calculate position (EP/MP/LP/Blinds)
2. Calculate effective stack (in BB)
3. Apply opening range for position
4. If facing raise: Calculate 3-bet/call/fold EV
5. Apply ICM adjustment if tournament

FLOP DECISIONS:
1. Calculate equity vs villain's range
2. Determine board texture (wet/dry/paired)
3. Determine range advantage
4. C-bet? (Apply frequency threshold for texture)
5. Size bet (dry: 33%; wet: 67-75%)

TURN DECISIONS:
1. Re-evaluate equity after turn card
2. Update villain's range (flop action)
3. Double-barrel? (Only with: strong hand, nut draw, or backdoor equity arrived)
4. Size appropriately (larger than flop)

RIVER DECISIONS:
1. Determine if you have value or bluff
2. Check alpha: Does villain fold enough for bluff to profit?
3. Check MDF: Are you defending enough vs river bet?
4. Polarize sizing: Large (75-100% pot) for value and bluffs

CALLING DECISIONS:
1. Calculate pot odds required equity
2. Compare to actual equity vs villain's range
3. Add implied odds if appropriate
4. If equity > required: Call; otherwise fold

RAISING DECISIONS:
1. Calculate if raise gets enough folds (alpha)
2. Calculate if hand has value
3. Balance: Check raise/call ratio
4. Apply MDF thinking to villain's response
```

---

## 9.9 Glossary of Key Poker Terms for AI Reference

```
Term             | Definition
-----------------|------------------------------------------
VPIP             | Voluntarily Put Money in Pot (% of hands played)
PFR              | Preflop Raise frequency
AF               | Aggression Factor = (bets + raises) / calls
3Bet%            | Frequency of 3-betting when facing raise
Fold to 3Bet     | Frequency of folding to 3-bets
WTSD             | Went to Showdown %
W$SD             | Won money at showdown %
CBet             | Continuation bet (flop bet after preflop raise)
Fold to CBet     | How often villain folds to c-bets
HUD              | Heads-Up Display (player statistics overlay)
Reg              | Regular (experienced player)
Fish/Rec         | Recreational player (weaker)
Nit              | Extremely tight player
LAG              | Loose-Aggressive
TAG              | Tight-Aggressive
SB               | Small Blind
BB               | Big Blind
UTG              | Under the Gun (first to act)
BTN              | Button (dealer position)
CO               | Cutoff (one right of BTN)
HJ               | Hijack (two right of BTN)
SPR              | Stack-to-Pot Ratio
EV               | Expected Value
GTO              | Game Theory Optimal
ICM              | Independent Chip Model
MDF              | Minimum Defense Frequency
nut              | Best possible hand on current board
OESD             | Open-Ended Straight Draw
FD               | Flush Draw
Combo            | Combination (a specific two-card holding)
Block/Blocker    | Card(s) in your hand that reduce villain's combos
Polarized        | Range contains strong hands + bluffs (no medium)
Merged/Condensed | Range of medium-strength hands (no extremes)
Overbet          | Bet larger than the pot
Probe bet        | OOP bet on turn after IP checked back flop
Donk bet         | OOP bet into preflop aggressor
Check-raise      | Check, then raise after opponent bets
Squeeze          | 3-bet over an open + caller(s)
ISO              | Isolation raise
Stab             | Small bet to take down unclaimed pot
Value bet        | Bet expecting to be called by worse hands
Thin value       | Bet that gets called by hands close in strength
Float            | Call a c-bet to take pot away on later street
Barrel           | Bet on a street (double-barrel = bet flop + turn)
Give up          | Stop bluffing / check behind
```

---

## 9.10 Quick Reference: Hand Probability at a Glance

**Preflop Probabilities (2 cards dealt):**
```
Hand Type                | Probability
-------------------------|----------
Any pair                 | 5.88%
Pocket aces              | 0.45%
Any pair or better       | 5.88%
AK (suited or offsuit)   | 1.21%
Suited connector 65+     | ~2.1%
Any suited hand          | 23.5%
```

**Board Run-out Probabilities:**
```
Event                                    | Probability
-----------------------------------------|-----------
Board pairs by turn                      | ~41%
Board paired (after 3-card flop)         | ~17%
Flush possible on board (3-card flop)    | ~11.8%
Rainbow flop                             | ~39.8%
Two-tone flop                            | ~55%
Monotone flop                            | ~5.2%
```

**Showdown Odds for Key Match-ups:**
```
Situation                | Equity  
-------------------------|--------
AA vs KK                 | 82% / 18%
AA vs AK                 | 93% / 7%
AA vs 72o                | 88% / 12%
KK vs QQ                 | 82% / 18%
Pair vs 2 overcards      | 55% / 45%
Pair vs lower pair       | 80% / 20%
Flush draw vs top pair   | 35% / 65%
OESD vs overpair         | 32% / 68%
```

---

*Document compiled for Heroes of Holdem AI training. All examples use standard NL Hold'em rules. HoH-specific modifications must be layered on top of these foundational principles by adjusting equity calculations, EV formulas, and frequency thresholds to account for game-specific mechanics.*

*Version 1.0 | March 2026*
