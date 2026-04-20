# Cheat mode? Console?


# Plans
- 5 rounds. Boss at the final round
  
- first round: 500 points , 60 wpm, 2-3 mistakes
- second round: 1200
- third round: 2800
- fourth round: 6000
- fifth round (boss): 12000

- Base Pay - $10
- Full Streak - $5 (all words are correctly typed)

- Four random kernel/macro available at every shop. (b/c we don't have "refresh shop") (We need weights for kernels & macros)

- *Sell the kernels? If we have this function, we can try infinite rounds. Infinite rounds also needs a non-hard-code score system*

# Kernels

- Carpe Diem $10
  allow 2 mistyped words before mult deducts

- Coffee $18
  More Concentration, time slow down, +10s

- Chain Reaction $20
  Every time streak reaches multiple of 5, mult +5

- Punctuation Pro $12
  Enable punctuation mode. All words with punctuation or capitalized letters yields double chips

- Native Speaker $15
  Expand the wordbank, words get harder, chips per word +5

- Keep Calm and Do Your Work $8
  Regain half of lost mult if word is typed correctly after mistyped word

- Writing Session $15
  Every word you are going to type will appear twice

- Clearance Sale $20
  Every kernel/macro gets a 25% discount. 

- Compound Interest $12
  After round ends, every $5 gives $1 interest

- Wowel $7
  Wow, vowels!. Every vowel typed gives +1 chip

- import random $5
  at the start of the round, randomize the base chip value (ranges from 0 to 10)

- Buying Power $14
  Every $5 held adds 1 base chip.

# Boss
- DDL
  You only get half time

- Overheat. Underclock.
  Base chips are halfed

- It Is What It Is
  No backspace

- The Big Theorem
  Double Score Requirements. 

# Macros
- for c in string.ascii_lowerkeys:
  if c in word: chip +2 

  26 macro, one macro for each letter. 
  $4 each. 

# How to model kernel/macros?
booster class

name, description, cost

- passiveBooster
  - app.params = dict that stores chipsperword/time that initialize with values in constants. app.params change according to boosters held. model use constants from app.params

- triggeredBooster
  - use if some where, but also use **hook** (*class methods that can be directly called in model.py*)

  onRoundStart(app) (not in checkwords)
  onCorrectWord(app)
  onMistake(app)