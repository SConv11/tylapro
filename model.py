import cmu_graphics
import constants
import words
import string

def onAppStart(app):
    app.gameStarted = False
    app.stepsPerSecond = constants.stepsPerSecond



def startGame(app):
    # generate the run (bosses)
    app.runIndex = 0
    app.money = 0
    app.gameOver = False

    startRound(app)
    

def startRound(app):
    app.currentInput = '' # current word typed
    app.currentIndex = 0 # index of current word typing (+=1 when spacebar pressed)
    app.timeLeft = constants.timerLen # in second
    app.mistakeNum = 0
    app.mistakes = [] # index wrong words
    
    app.chips = 0
    app.streak = 0
    app.mult = 1

    app.roundStarted = False # Type to start
    app.roundEnded = False
    app.gameOver = False

    app.words = words.generateWordList(100)
    
    
# if round ends, wait for some time and get to the shop

def onStep(app):
    if app.roundStarted and not app.roundEnded:
        app.timeLeft -= 1/app.stepsPerSecond
        if app.timeLeft <= 0.01: app.roundEnded = True

def onMousePress(app, mouseX, mouseY):
    if not app.gameStarted: # on home page
        if app.width//2-200/2 <= mouseX <= app.width//2+200/2:
            if 600-75/2 <= mouseY <= 600+75/2:
                app.gameStarted = True

def onKeyPress(app, key):

    # control + backspace
    # long press backspace

    # backspace is locked after confirming a word (i.e. pressing space)

    if not app.roundStarted and not app.roundEnded:
        app.roundStarted = True

    if key == 'space':

        if app.currentInput != '':
            checkWord(app)
            app.currentInput = ''
            app.currentIndex += 1
            
    elif key in string.ascii_letters+'.,!?;:' :
        app.currentInput += key
    elif key == 'backspace': 
        app.currentInput = app.currentInput[:-1]
        
'''
Change balance (mult) here
'''
def checkWord(app):
    if app.currentInput == app.words[app.currentIndex]: 
        app.chips += constants.chipsPerWord
        app.streak += 1
        app.mult += 1
    else: 
        app.mistakeNum += 1
        app.mistakes.append( (app.currentIndex, app.currentInput) )
        app.streak = 0
        app.mult = max(app.mult/2, 1)

    