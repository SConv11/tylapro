from cmu_graphics import *

def redrawAll(app):
    drawBackground(app)

    if not app.gameStarted:
        drawHome(app)  
    else:
        if app.roundStarted and not app.roundEnded:
            drawRound(app)
        elif app.roundEnded:
            drawShop(app)
        elif app.gameOver:
            drawScore(app)

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
    # top bar, timer as a shrinking bar, chips, mult
    # word row, cursor
    # cursor, vector, animation
    # change line
    pass

def drawShop(app):
    # shop, score, Run Info
    pass

def drawScore(app):
    pass