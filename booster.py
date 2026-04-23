import string
import random

# AI is partly used for forming all these class. 
# I had these info in a markdown file. 
# and used AI to rewrite them into these classes. 
# since they are essentially all repetitive and copy paste work.

# The "Hook" mechanism is proposed by AI. 
# i.e. store all the booster mechanisms in method of booster class
# and call the methods through the hook

# All functions and class structures related
# to booster mechanisms are written on my own.

class Booster:
    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost

    # Hooks
    def onRoundStart(self, app): pass
    def onRoundEnd(self, app): pass
    def onCorrectWord(self, app, word): pass
    def onMistake(self, app): pass


class Kernel(Booster):
    pass


class Boss(Booster):
    def __init__(self, name, description):
        super().__init__(name, description, cost=None)


class Macro(Booster):
    # for now, difference between macro is the letter.
    def __init__(self, letter):
        super().__init__(f"Macro '{letter}'",
                         f"For every word containing '{letter}', chip +2",
                         4)
        self.letter = letter
    def onCorrectWord(self, app, word):
        if self.letter in word.lower():
            app.chips += 2


# ---------- Kernels -------------------------------------------

class CarpeDiem(Kernel):
    def __init__(self):
        super().__init__('Carpe Diem',
                         'Allow 2 mistyped words before mult deducts',
                         10)
        self.freeMistakes = 2
    def onRoundStart(self, app):
        self.freeMistakes = 2
    def onMistake(self, app):
        if self.freeMistakes > 0:
            app.mult += app.lastMistakeLoss
            self.freeMistakes -= 1


class Coffee(Kernel):
    def __init__(self):
        super().__init__('Coffee',
                         'More concentration, time slows down, +10s',
                         18)
    def onRoundStart(self, app):
        app.timeLeft += 10


class ChainReaction(Kernel):
    def __init__(self):
        super().__init__('Chain Reaction',
                         'Every time streak reaches a multiple of 5, mult +5',
                         20)
    def onCorrectWord(self, app, word):
        if app.streak > 0 and app.streak % 5 == 0:
            app.mult += 5

class PunctuationPro(Kernel):
    def __init__(self):
        super().__init__('Punctuation Pro',
                         'Enable punctuation mode. Words with punctuation or '
                         'capitalized letters yield 10 more chips',
                         12)
    def onRoundStart(self, app):
        app.punctuationMode = True
    def onCorrectWord(self, app, word):

        found = False
        for c in word:
            if c in '.,!?;:' or c.isupper():
                found = True
                break

        if found:
            app.chips += 10

class NativeSpeaker(Kernel):
    def __init__(self):
        super().__init__('Native Speaker',
                         'Expand the wordbank, words get harder, '
                         'chips per word +15',
                         15)
    def onRoundStart(self, app):
        app.hardMode = True
        app.chipsPerWord += 15

class KeepCalm(Kernel):
    def __init__(self):
        super().__init__('Keep Calm and Do Your Work',
                         'Regain half of lost mult if word is typed correctly '
                         'after a mistyped word',
                         8)
        self.lastWasMistake = False
        self.lastLoss = 0
    def onRoundStart(self, app):
        self.lastWasMistake = False
        self.lastLoss = 0
    def onMistake(self, app):
        self.lastWasMistake = True
        self.lastLoss = app.lastMistakeLoss
    def onCorrectWord(self, app, word):
        if self.lastWasMistake:
            app.mult += self.lastLoss / 2
            self.lastWasMistake = False
            self.lastLoss = 0


class WritingSession(Kernel):
    def __init__(self):
        super().__init__('Writing Session',
                         'Every word you are going to type will appear twice',
                         15)
    def onRoundStart(self, app):
        app.doubleWords = True




class CompoundInterest(Kernel):
    def __init__(self):
        super().__init__('Compound Interest',
                         'After round ends, every $5 gives $1 interest',
                         12)
    def onRoundEnd(self, app):
        app.money += app.money // 5


class Wowel(Kernel):
    def __init__(self):
        super().__init__('Wowel',
                         'Wow, vowels! Every vowel typed gives +1 chip',
                         7)
    def onCorrectWord(self, app, word):
        app.chips += sum([1 for c in word.lower() if c in 'aeiou'])


class ImportRandom(Kernel):
    def __init__(self):
        super().__init__('import random',
                         'At the start of the round, randomize the base chip '
                         'value (ranges from 0 to 10)',
                         5)
    def onRoundStart(self, app):
        app.chipsPerWord = random.randint(0, 10)


class BuyingPower(Kernel):
    def __init__(self):
        super().__init__('Buying Power',
                         'Every $5 held adds 1 base chip',
                         14)
    def onRoundStart(self, app):
        app.chipsPerWord += app.money // 5

# ------- Bosses -----------------------------------------

class DDL(Boss):
    def __init__(self):
        super().__init__('DDL', 'You get 5 seconds less')
    def onRoundStart(self, app):
        app.timeLeft -= 5


class OverheatUnderclock(Boss):
    def __init__(self):
        super().__init__('Overheat. Underclock.', 'Base chips are halved')
    def onRoundStart(self, app):
        app.chipsPerWord = max(app.chipsPerWord // 2, 1)


class ItIsWhatItIs(Boss):
    def __init__(self):
        super().__init__('It Is What It Is', 'No backspace')
    def onRoundStart(self, app):
        app.noBackspace = True


class TheBigTheorem(Boss):
    def __init__(self):
        super().__init__('The Big Theorem', 'Double score requirements')
    def onRoundStart(self, app):
        app.scoreMultiplier = 2


#------------------------------------------------------------------------------

KERNELS = [CarpeDiem(), Coffee(), ChainReaction(), PunctuationPro(),
           NativeSpeaker(), KeepCalm(), WritingSession(),
           CompoundInterest(), Wowel(), ImportRandom(), BuyingPower()]

BOSSES = [DDL(), OverheatUnderclock(), ItIsWhatItIs(), TheBigTheorem()]

MACROS = [Macro(c) for c in string.ascii_lowercase]
