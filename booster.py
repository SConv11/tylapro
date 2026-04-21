import string

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
        pass


# ---------- Kernels -------------------------------------------

class CarpeDiem(Kernel):
    def __init__(self):
        super().__init__('Carpe Diem',
                         'Allow 2 mistyped words before mult deducts',
                         10)
    def onMistake(self, app):
        pass


class Coffee(Kernel):
    def __init__(self):
        super().__init__('Coffee',
                         'More concentration, time slows down, +10s',
                         18)
    def onRoundStart(self, app):
        pass


class ChainReaction(Kernel):
    def __init__(self):
        super().__init__('Chain Reaction',
                         'Every time streak reaches a multiple of 5, mult +5',
                         20)
    def onCorrectWord(self, app, word):
        pass

class PunctuationPro(Kernel):
    def __init__(self):
        super().__init__('Punctuation Pro',
                         'Enable punctuation mode. Words with punctuation or '
                         'capitalized letters yield double chips',
                         12)
    def onRoundStart(self, app):
        pass
    def onCorrectWord(self, app, word):
        pass

class NativeSpeaker(Kernel):
    def __init__(self):
        super().__init__('Native Speaker',
                         'Expand the wordbank, words get harder, '
                         'chips per word +5',
                         15)
    def onRoundStart(self, app):
        pass

class KeepCalm(Kernel):
    def __init__(self):
        super().__init__('Keep Calm and Do Your Work',
                         'Regain half of lost mult if word is typed correctly '
                         'after a mistyped word',
                         8)
    # self.lastWasMistake
    def onCorrectWord(self, app, word):
        pass


class WritingSession(Kernel):
    def __init__(self):
        super().__init__('Writing Session',
                         'Every word you are going to type will appear twice',
                         15)
    def onRoundStart(self, app):
        pass


class ClearanceSale(Kernel):
    def __init__(self):
        super().__init__('Clearance Sale',
                         'Every kernel/macro gets a 25% discount',
                         20)
        # on Shop


class CompoundInterest(Kernel):
    def __init__(self):
        super().__init__('Compound Interest',
                         'After round ends, every $5 gives $1 interest',
                         12)
    def onRoundEnd(self, app):
        pass


class Wowel(Kernel):
    def __init__(self):
        super().__init__('Wowel',
                         'Wow, vowels! Every vowel typed gives +1 chip',
                         7)
    def onCorrectWord(self, app):
        pass


class ImportRandom(Kernel):
    def __init__(self):
        super().__init__('import random',
                         'At the start of the round, randomize the base chip '
                         'value (ranges from 0 to 10)',
                         5)
    def onRoundStart(self, app):
        pass


class BuyingPower(Kernel):
    def __init__(self):
        super().__init__('Buying Power',
                         'Every $5 held adds 1 base chip',
                         14)
    def onRoundStart(self, app):
        pass

# ------- Bosses -----------------------------------------

class DDL(Boss):
    def __init__(self):
        super().__init__('DDL', 'You only get half the time')


class OverheatUnderclock(Boss):
    def __init__(self):
        super().__init__('Overheat. Underclock.', 'Base chips are halved')


class ItIsWhatItIs(Boss):
    def __init__(self):
        super().__init__('It Is What It Is', 'No backspace')


class TheBigTheorem(Boss):
    def __init__(self):
        super().__init__('The Big Theorem', 'Double score requirements')


#------------------------------------------------------------------------------

KERNELS = [CarpeDiem(), Coffee(), ChainReaction(), PunctuationPro(),
           NativeSpeaker(), KeepCalm(), WritingSession(), ClearanceSale(),
           CompoundInterest(), Wowel(), ImportRandom(), BuyingPower()]

BOSSES = [DDL(), OverheatUnderclock(), ItIsWhatItIs(), TheBigTheorem()]

MACROS = [Macro(c) for c in string.ascii_lowercase]
