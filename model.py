from cmu_graphics import *
import constants
import words
import string
import random
import booster
import view

def onAppStart(app):
    app.gameStarted = False
    app.stepsPerSecond = constants.stepsPerSecond
    app.roundStarted = False
    app.shopStarted = False
    app.gameOver = False
    app.won = False
    app.roundEnding = False
    app.endTimer = 0
    app.lastStats = None

    app.scoreMultiplier = 1
    app.scoreRequirement = [500, 1200, 2800, 6000, 12000]



def startGame(app):
    # generate the run (bosses)
    app.runIndex = 0
    app.money = 0
    app.gameOver = False
    app.won = False
    app.boosters = []
    # one boss on the final round; other rounds have no boss
    app.bossSequence = ([None] * (len(app.scoreRequirement) - 1)
                        + [random.choice(booster.BOSSES)])

    startRound(app)
    

def startRound(app):
    app.currentInput = '' # current word typed
    app.currentIndex = 0 # index of current word typing (+=1 when spacebar pressed)
    app.timeLeft = constants.timerLen # in second
    app.mistakeNum = 0
    app.mistakes = dict() # index wrong words

    app.chips = 0
    app.streak = 0
    app.mult = 1
    app.chipsPerWord = constants.chipsPerWord
    
    app.lastMistakeLoss = 0
    app.punctuationMode = False
    app.hardMode = False
    app.doubleWords = False
    app.noBackspace = False
    app.scoreMultiplier = 1

    app.timerStarted = False # Type to start

    app.currentBoss = app.bossSequence[app.runIndex]

    for b in app.boosters:
        b.onRoundStart(app)
    if app.currentBoss is not None:
        app.currentBoss.onRoundStart(app)

    # capture the real round-duration after boosters/boss modify app.timeLeft
    app.roundStartTimer = app.timeLeft

    app.words = words.generateWordList(100, hard = app.hardMode, punc = app.punctuationMode)
    if app.doubleWords:
        app.words = [w for word in app.words for w in (word, word)]
    
    rebuildLines(app)
    app.currentLineIndex = 0

    app.roundStarted = True

    

def startShop(app):
    # Pool = unowned kernels + unowned macros, weighted so macros are rarer.
    # Weighted sampling without replacement: after each pick, pop both the
    # chosen item and its weight so it can't be selected again.
    kernelPool = [k for k in booster.KERNELS if k not in app.boosters]
    macroPool  = [m for m in booster.MACROS  if m not in app.boosters]
    pool    = kernelPool + macroPool
    weights = ([constants.kernelWeight] * len(kernelPool)
               + [constants.macroWeight] * len(macroPool))

    app.shopItems = []
    for _ in range(min(constants.shopSize, len(pool))):
        idx = random.choices(range(len(pool)), weights=weights, k=1)[0]
        app.shopItems.append(pool.pop(idx))
        weights.pop(idx)

    app.shopSold = set()
    app.shopStarted = True


def rebuildLines(app):
    app.lines = splitIntoLines(app.words, 700, constants.charWidth)
    app.lineStartIndices = []
    count = 0
    for line in app.lines:
        app.lineStartIndices.append(count)
        count += len(line)
    
# Greedy word-wrap: accumulates pixel width (character count + 1 space) and
# starts a new line whenever the next word would exceed boardWidth.
def splitIntoLines(words, boardWidth, charWidth):
    currentLine = []
    res = []
    currentWidth = 0
    for word in words:
        currentWidth += (len(word) + 1) * charWidth
        if currentWidth <= boardWidth: currentLine.append(word)
        else:
            res.append(currentLine)
            currentLine = [word]
            currentWidth = (len(word) + 1) * charWidth
    res.append(currentLine)
    return res

    
# if round ends, wait for some time and get to the shop

def onStep(app):
    if app.roundStarted and app.timerStarted and not app.roundEnding:
        app.timeLeft -= 1/app.stepsPerSecond
        if app.timeLeft <= 0:
            app.timeLeft = 0
            app.roundEnding = True
            app.endTimer = app.stepsPerSecond * 2

    if app.roundEnding:
        app.endTimer -= 1
        if app.endTimer <= 0:
            finalScore = app.chips * app.mult
            required = (app.scoreRequirement[app.runIndex]
                        * app.scoreMultiplier)

            correctWords = app.currentIndex - app.mistakeNum
            timeElapsed = max(app.roundStartTimer - app.timeLeft, 0.001)
            app.lastStats = {
                'chips':    app.chips,
                'mult':     app.mult,
                'score':    finalScore,
                'mistakes': app.mistakeNum,
                'accuracy': correctWords / max(app.currentIndex, 1),
                'wpm':      correctWords * 60 / timeElapsed,
            }

            app.roundEnding = False
            app.roundStarted = False

            if finalScore >= required:
                # Win: award base pay + full-streak bonus, then run hooks
                app.money += 10
                if app.mistakeNum == 0:
                    app.money += 5

                for b in app.boosters:
                    b.onRoundEnd(app)
                if app.currentBoss is not None:
                    app.currentBoss.onRoundEnd(app)

                if app.runIndex == len(app.scoreRequirement) - 1:
                    # Beat the final boss
                    app.won = True
                    app.gameOver = True
                else:
                    startShop(app)
            else:
                # Did not meet score requirement
                app.won = False
                app.gameOver = True

def onMousePress(app, mouseX, mouseY):
    if not app.gameStarted: # on home page
        if view.getHomeButton(app).contains(mouseX, mouseY):
            app.gameStarted = True
            startGame(app)
        return

    if app.gameOver:
        if view.getScoreButton(app).contains(mouseX, mouseY):
            startGame(app)
        return

    if app.shopStarted:
        itemButtons, nextBtn = view.getShopButtons(app)
        for i, btn in enumerate(itemButtons):
            if btn.contains(mouseX, mouseY):
                if i in app.shopSold:
                    return
                item = app.shopItems[i]
                if app.money >= item.cost:
                    app.money -= item.cost
                    app.boosters.append(item)
                    app.shopSold.add(i)
                return
        if nextBtn.contains(mouseX, mouseY):
            app.shopStarted = False
            app.runIndex += 1
            startRound(app)


'''
MAKE SURE YOU ARE USING ENGLISH KEYBOARD
'''
def onKeyPress(app, key):
    # control + backspace
    # long press backspace

    # backspace is locked after confirming a word (i.e. pressing space)

    if not app.roundStarted:
        return
    if app.roundEnding:
        return

    if not app.timerStarted:
        app.timerStarted = True

    if key == 'space':

        if app.currentInput != '':
            checkWord(app)
            app.currentInput = ''
            app.currentIndex += 1
            nextLine = app.currentLineIndex + 1
            if (nextLine < len(app.lineStartIndices) and
                app.currentIndex >= app.lineStartIndices[nextLine]):
                app.currentLineIndex = nextLine
            
    elif key in string.ascii_letters+'.,!?;:' :
        app.currentInput += key
    elif key == 'backspace' and not app.noBackspace:
        app.currentInput = app.currentInput[:-1]


def checkWord(app):
    word = app.words[app.currentIndex]
    if app.currentInput == word: # onCorrectWord
        app.chips += app.chipsPerWord
        app.streak += 1
        app.mult += 1
        for b in app.boosters:
            b.onCorrectWord(app, word)
        if app.currentBoss is not None:
            app.currentBoss.onCorrectWord(app, word)
    else: # onMistake
        app.mistakeNum += 1
        app.mistakes[app.currentIndex] = app.currentInput
        app.streak = 0
        prevMult = app.mult
        app.mult = max(app.mult/2, 1)  # halve mult on mistake, floor at 1
        app.lastMistakeLoss = prevMult - app.mult
        for b in app.boosters:
            b.onMistake(app)
        if app.currentBoss is not None:
            app.currentBoss.onMistake(app)

    