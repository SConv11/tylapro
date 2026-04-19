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
    
    drawWords(app) # and drawCursor integrated within
    
    # chips, mult
    # word row, cursor
    # cursor, vector, animation
    # change line


def drawWords(app): # and drawCursor integrated within
    drawRect(app.width//2, 500, 800, 400, align = 'center', fill = 'white')
    lineLeft, lineTop, lineHeight = app.width//2-350, 400+50, 40
    currentLineIndex = 0
    count = 0

    # which line am I at right now
    for i in range(len(app.lines)):
        line = app.lines[i]
        count += len(line)
        if count > app.currentIndex:
            currentLineIndex = i
            break
    
    wordIndex = 0
    startLine = max(0, currentLineIndex -1)
    for i in range(0, startLine):
        wordIndex += len(app.lines[i])
    
    # draw each line
    for row in range(3):
        lineIndex = startLine + row
        if lineIndex < 0 or lineIndex >= len(app.lines): continue

        x = lineLeft
        y = lineTop + row * lineHeight

        for word in app.lines[lineIndex]:
            # future words
            if wordIndex > app.currentIndex: 
                drawLabel(word + ' ', x, y, size = constants.fontSize, 
                      font = 'monospace', align = 'left', fill = 'gray')
            
            # past words
            elif wordIndex < app.currentIndex: 
                if wordIndex in app.mistakes:
                    input = app.mistakes[wordIndex]
                    
                    for i in range(len(word)):
                        if i >= len(input):
                            drawLabel(word[i], x+i*constants.charWidth, y, 
                                      size = constants.fontSize, font = 'monospace', 
                                      align = 'left', fill = 'gray')
                        elif input[i] == word[i]:
                            drawLabel(input[i], x+i*constants.charWidth, y, 
                                      size = constants.fontSize, font = 'monospace', 
                                      align = 'left', fill = 'black')
                        else:
                            drawLabel(input[i], x+i*constants.charWidth, y, 
                                      size = constants.fontSize, font = 'monospace', 
                                      align = 'left', fill = 'red')

                else: drawLabel(word + ' ', x, y, size = constants.fontSize, 
                      font = 'monospace', align = 'left', fill = 'black')
            
            # current word. draw cursor as well. 
            else: 
                    for i in range(len(word)):
                        if i >= len(app.currentInput):
                            drawLabel(word[i], x+i*constants.charWidth, y, 
                                      size = constants.fontSize, font = 'monospace', 
                                      align = 'left', fill = 'gray')
                        elif app.currentInput[i] == word[i]:
                            drawLabel(app.currentInput[i], x+i*constants.charWidth, y, 
                                      size = constants.fontSize, font = 'monospace', 
                                      align = 'left', fill = 'black')
                        else:
                            drawLabel(app.currentInput[i], x+i*constants.charWidth, y, 
                                      size = constants.fontSize, font = 'monospace', 
                                      align = 'left', fill = 'red')
                    
                    cursorX = x + len(app.currentInput) * constants.charWidth
                    drawLine(cursorX, y-20, cursorX, y+20)

            wordIndex += 1
            x += (len(word) + 1) * constants.charWidth

    

def drawShop(app):
    # shop, score, Run Info
    pass

def drawScore(app):
    pass