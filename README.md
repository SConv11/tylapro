# Tylapro

A roguelike typing game inspired by Balatro's scoring system. Type words to earn chips, build a multiplier through streaks, and survive 5 rounds — including a final boss.

## How to Play

Run `python main.py`. Make sure you are using an **English keyboard layout**.

- Words appear on screen. Type them and press **Space** to confirm.
- Typing starts the timer. You have **20 seconds** per round.
- **Correct word:** chips +5, streak +1, mult +1
- **Mistype:** streak resets, mult is halved (floor 1)
- **Final score = chips × mult**. Meet the target to advance.
- Between rounds, visit the shop to buy boosters with earned money.

## Scoring & Progression

| Round | Target Score |
|-------|-------------|
| 1     | 500         |
| 2     | 1,200       |
| 3     | 2,800       |
| 4     | 6,000       |
| 5     | 12,000      |

Round 5 always features a randomly chosen **Boss** with a debuff. Beat it to win.

Failing to meet the target ends the run immediately.

## Shop

After each round (except the last), you earn money and enter a shop:

- **Base pay:** $10 per round won; +$5 bonus for a perfect run (zero mistakes)
- The shop offers up to 4 items drawn from the booster pool (kernels weighted higher than macros)
- Items already owned are excluded from the pool

## Boosters

### Kernels (active modifiers)

| Name | Effect | Cost |
|------|--------|------|
| Carpe Diem | First 2 mistakes don't penalize mult | $10 |
| Coffee | +10 seconds to the round timer | $18 |
| Chain Reaction | Every 5-word streak milestone gives mult +5 | $20 |
| Punctuation Pro | Enables punctuation mode; punctuated/capitalized words yield double chips | $12 |
| Native Speaker | Hard word bank, chips per word +10 | $15 |
| Keep Calm and Do Your Work | Regain half of lost mult on the next correct word after a mistake | $8 |
| Writing Session | Every word appears twice in sequence | $15 |
| Compound Interest | After a round, every $5 held earns $1 interest | $12 |
| Wowel | Each vowel in a correctly typed word gives +1 chip | $7 |
| import random | Base chip value is randomized (0–10) at round start | $5 |
| Buying Power | Every $5 held adds 1 to base chips per word | $14 |

### Macros

One macro exists for each letter of the alphabet (a–z). Each costs $4.

> **Macro 'x'** — For every word containing the letter *x*, chip +2.

### Bosses (final round only)

| Name | Debuff |
|------|--------|
| DDL | Round timer is halved |
| Overheat. Underclock. | Base chips per word are halved |
| It Is What It Is | Backspace is disabled |
| The Big Theorem | Score requirement is doubled |

## Word Banks

Word lists are sourced from [monkeytype](https://github.com/monkeytypegame/monkeytype):

- `english.json` — standard difficulty
- `english_5k.json` — hard mode (Native Speaker kernel)

## Project Structure

```
main.py        entry point (runApp)
model.py       game state and event handlers
view.py        all drawing logic; Button class
booster.py     Booster/Kernel/Macro/Boss classes and instances
words.py       word list generation
constants.py   tuning values (timer, chips, weights, screen size)
```

## Dependencies

- Python 3
- [cmu_graphics](https://academy.cs.cmu.edu/desktop)

## Developer Cheat Mode
To be continued...
