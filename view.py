# draw everything. 
# only redrawall

# timer bar
# cursor, vector, animation
# change line

def redrawAll(app):
    drawBackground(app)

    if not app.roundStarted and not app.roundEnded:
        drawHome(app)
    elif app.roundedStarted and not app.roundEnded:
        drawRound(app)
    elif app.roundEnded:
        drawShop(app)
    elif app.gameOver:
        drawScore(app)

def drawBackground(app):


def drawHome(app):

def drawRound(app):
    # top bar, timer as a shrinking bar, chips, mult
    # word row, cursor

def drawShop(app):
    # shop, score, the run

def drawScore(app):
