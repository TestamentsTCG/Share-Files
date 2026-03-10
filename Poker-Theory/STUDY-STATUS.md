# Pluribus Study - Status

**Last Updated:** 2026-03-10  
**Status:** COMPLETE - Full 10,000 Hand Analysis

---

## Hands Analyzed: 10,000 / 10,000 ✅

Dataset: Pluribus vs. world-class pros (6-handed, 50/100)  
Parsers: `~/poker-study/parse_hands.py` (original) | `~/poker-study/fix_stats.py` (extended)  
Output: `/Users/davidleroux/.openclaw/workspace/poker-study/pluribus-patterns.md`  
Stats: `~/poker-study/full_stats_corrected.json`

---

## Key Insights Summary (Full 10,000 Hands)

### Preflop
- **VPIP: 24.0% | PFR: 14.2%** - Tight-aggressive, raise-or-fold from EP
- Open raise: **2.0-2.5bb from ALL positions** - confirmed at scale, no position-based sizing
- **Limp frequency: 2.2%** (new finding - small mixed strategy from BTN/SB)
- Fold to raise: UTG 97.2%, HJ 95.2%, CO 91.5%, BTN 85.0%
- **BTN has a flatting range**: 10.7% call vs opens (was underestimated at 2k hands)
- 3-bet: **9.89bb average**, 4-bet: **25.4bb average**
- BB defend frequency: **35.3% call vs opens** (confirmed)

### Post-Flop
- Saw flop: **12.5%** of hands | Turn: 9.5% | River: 7.4%
- C-bet frequency: **58.6%** (revised from 62.5%)
  - Dry/broadway boards: 67-77% frequency, 63-71% pot size
  - Connected/low boards: 36-40% frequency
  - Rainbow ace-high: 40% frequency but **100% pot** when betting
- Turn bet: **36.9%** avg 71.5% pot
- River bet: **37.4%** avg **99% pot** (nearly full-pot average)
- **River overbets: 25.9% of Pluribus river bets** at avg **191% pot** (revised from 39%)

### New Patterns Discovered at 10k Hands
- **Check-raise (flop): 16.1%** of opportunities, avg 126% pot
- **Check-raise (turn): 7.4%** of opportunities, avg 123% pot
- **Check-raise (river): 11.4%** of opportunities, avg 194% pot
- **Probe bet: 34.2%** - fires turn into PF raiser after flop checks through
- **Triple barrel completion: 53.8%** - once betting flop+turn, usually completes river
- **Showdown frequency: 77.7%** of river hands
- **Showdown win rate: 47.6%** (near 50% = GTO equilibrium confirmation)

### Position Win Rates
- HJ: **+30.4 bb/100** | BTN: **+26.8 bb/100** | CO: **+4.8 bb/100**
- SB: **-20.2 bb/100** | UTG: **-18.1 bb/100** | BB: **-67.7 bb/100**
- Overall: -7.09 bb/100 (within variance for 10k hands vs world-class pros)

### The Defining Patterns (Confirmed and Expanded)
1. River strategy is maximally polarized: 50-75% pot OR 100%+ overbet. Nothing between.
2. Check-raises are frequent (16% flop) and massive (126-194% pot avg).
3. Probe bets fire 34% of the time when PF raiser shows weakness.
4. Triple barrel completion is high (54%) - Pluribus doesn't give up easily.
5. Near-zero small bets on river (0.3% of river bets under 40% pot).

---

## Study Document
Full analysis: `pluribus-patterns.md` (2,700+ lines)
- Parser code (full + condensed)
- Statistical summary tables - 2k and 10k comparison
- **Top 50 annotated instructive hands** (20 from run 1 + 30 from run 2)
- Key takeaways vs conventional wisdom
- Direct application guide for micro-stakes
- New sections: check-raise, probe bet, triple barrel, showdown analysis

---

## Files
| File | Description |
|------|-------------|
| `pluribus-patterns.md` | Main study document |
| `parse_hands.py` | Original parser (2k hands) |
| `fix_stats.py` | Extended parser (10k hands, bug-fixed) |
| `full_analysis.py` | First extended analysis attempt |
| `annotate_hands.py` | Hand annotation script |
| `full_stats_corrected.json` | Raw stats JSON (10k hands) |
| `hands_for_annotation.pkl` | Serialized hand objects |
| `annotated_hands_new.txt` | 30 new annotated hands |
| `phh-dataset/` | Raw .phh dataset (10,000 files) |

---

## Study Complete ✅

All 10,000 hands analyzed. Document pushed to `~/Share-Files/Poker-Theory/`.
