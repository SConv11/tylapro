from cmu_graphics import *
import model
import constants

upperBound = int(227*0.8)
lowerBound = int(931*0.8)
leftBound = int(184*0.8)
rightBound = int(1303*0.8)+1
boardWidth = rightBound - leftBound
boardHeight = lowerBound - upperBound

def redrawAll(app):
    drawBackground(app)

    if not app.gameStarted:
        drawHome(app)  
    else:
        if app.shopStarted:
            drawShop(app)
        elif app.gameOver:
            drawScore(app)
        elif app.roundStarted: 
            drawRound(app)

def drawBackground(app):
    drawImage('static/background.png', 0, 0, width=app.width, height=app.height)


def drawHome(app):
    drawRect(app.width//2, 350, 300, 100, align = 'center', fill = 'white')
    drawLabel('Tylapro', app.width//2, 350, size = 52, 
              fill = 'black', font = 'monospace', bold = True)
    
    drawRect(app.width//2, 600, 200, 75, align = 'center', fill = 'white')
    drawRect(app.width//2, 600, 190, 65, align = 'center', border = 'black', fill = None)
    drawLabel('Start', app.width//2, 600, size = 42, fill = 'black', font = 'monospace')


def drawRound(app):
    # top bar, timer as a shrinking bar
    drawLine(leftBound, upperBound+5, 
             leftBound + boardWidth * app.timeLeft / constants.timerLen,  upperBound+5, 
             fill = 'black', lineWidth = 10)
    


    # chips, mult
    # word row, cursor
    # cursor, vector, animation
    # change line
    pass

def drawShop(app):
    # shop, score, Run Info
    pass

def drawScore(app):
    pass