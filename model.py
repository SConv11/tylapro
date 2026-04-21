from cmu_graphics import *
import constants
import words
import string

def onAppStart(app):
    app.gameStarted = False
    app.stepsPerSecond = constants.stepsPerSecond
    app.roundStarted = False
    app.shopStarted = False
    app.gameOver = False
    app.roundEnding = False
    app.endTimer = 0



def startGame(app):
    # generate the run (bosses)
    app.runIndex = 0
    app.money = 0
    app.gameOver = False

    startRound(app)
    

def startRound(app):

    '''
    Redo. 
    app.params?
    for booster in boosters that I currently hold, 
    run booster.onRoundStart
    '''

    app.currentInput = '' # current word typed
    app.currentIndex = 0 # index of current word typing (+=1 when spacebar pressed)
    app.timeLeft = constants.timerLen # in second
    app.mistakeNum = 0
    app.mistakes = dict() # index wrong words
    
    
    app.chips = 0
    app.streak = 0
    app.mult = 1

    app.timerStarted = False # Type to start

    app.words = words.generateWordList(100)
    app.lines = splitIntoLines(app.words, 700, constants.charWidth)

    app.lineStartIndices = []
    count = 0
    for line in app.lines:
        app.lineStartIndices.append(count)
        count += len(line)
    app.currentLineIndex = 0

    app.roundStarted = True
    
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
            app.roundEnding = False
            app.roundStarted = False
            app.shopStarted = True

def onMousePress(app, mouseX, mouseY):
    if not app.gameStarted: # on home page
        if app.width//2-200/2 <= mouseX <= app.width//2+200/2:
            if 600-75/2 <= mouseY <= 600+75/2:
                app.gameStarted = True
                startGame(app)


'''
MAKE SURE YOU ARE USING ENGLISH KEYBOARD
'''
def onKeyPress(app, key):
    # control + backspace
    # long press backspace

    # backspace is locked after confirming a word (i.e. pressing space)

    if app.roundEnding:
        return

    if app.roundStarted and not app.timerStarted:
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
    elif key == 'backspace': 
        app.currentInput = app.currentInput[:-1]
        

def checkWord(app):
    'redo. same as above'
    if app.currentInput == app.words[app.currentIndex]: 
        app.chips += constants.chipsPerWord
        app.streak += 1
        app.mult += 1
    else: 
        app.mistakeNum += 1
        app.mistakes[app.currentIndex] =  app.currentInput
        app.streak = 0
        app.mult = max(app.mult/2, 1)

    