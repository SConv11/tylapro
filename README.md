# Tylapro


**Concept:** A roguelike typing game inspired by Balatro's scoring system.

**Core Gameplay:**
- Fixed timer per round, words appear and the player types them
- Each correctly typed word = chips
- Streak multiplier: for the nth consecutive correct word, mult += n
- Typo = miss, which penalizes mult (halve or similar, exact formula TBD for balancing)
- Final score = chips × mult (per-word vs end-of-round calculation still undecided)

**Roguelike Structure:**
- Rounds get progressively harder
- Boss encounters with unique mechanics
- Between-round shop where players acquire boosters

**Boosters (details TBD):**
- Could be passive (persistent), consumable (one-time), or upgrade-style
- Interact with knobs like word length, streak thresholds, timer, typo forgiveness, mult scaling, etc.
- Specific booster ideas not yet discussed

**Technical Setup:**
- Python, using cmu_graphics (required for MVC)
- VSCode + GitHub repository
- Multi-file structure: main, model, view, words, boosters, constants
- Word bank from a curated text file for difficulty control
