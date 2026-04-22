from cmu_graphics import *
import model
import constants
import booster

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


def getHomeButton(app):
    return Button(app.width // 2, 600, 200, 75, label='Start')


def drawHome(app):
    drawRect(app.width // 2, 350, 300, 100, align='center', fill='white')
    drawLabel('Tylapro', app.width // 2, 350, size=52,
              fill='black', font='monospace', bold=True)

    btn = getHomeButton(app)
    btn.draw(labelSize=42)
    # inset border for visual depth
    drawRect(btn.cx, btn.cy, btn.w - 10, btn.h - 10,
             align='center', border='black', fill=None)

def drawRound(app):
    # top bar, timer as a shrinking bar
    drawLine(leftBound, upperBound+5,
             leftBound + boardWidth * app.timeLeft / constants.timerLen,  upperBound+5,
             fill = 'black', lineWidth = 10)

    drawWords(app) # and drawCursor integrated within
    drawChipMult(app)

    if app.roundEnding:
        drawRect(app.width//2, app.height//2, 400, 100, align='center', fill='black', opacity=80)
        drawLabel("TIME'S UP!", app.width//2, app.height//2,
                  size=40, fill='white', bold=True, font='monospace')


def drawChipMult(app):
    y = 270
    drawRect(app.width//2, y, 30, 30, align = 'center', fill = 'white')
    drawLabel('X', app.width//2, y, bold = True, size = 30, font = 'monospace')

    drawRect(app.width//2 - 250, y, 300, 100, align = 'center', fill = 'white')
    drawLabel(f'Chip: {app.chips}', app.width//2 - 250, y, align = 'center',
              bold = True, size = 40, font = 'monospace')
    
    drawRect(app.width//2 + 250, y, 300, 100, align = 'center', fill = 'white')
    drawLabel(f'Mult: {app.mult}', app.width//2 + 250, y, align = 'center',
              bold = True, size = 40, font = 'monospace')



# Renders words character-by-character: past mistakes show per-char diff
# (black=correct, red=wrong, gray=missing); current word also draws the cursor.
def drawWords(app): # and drawCursor integrated within
    drawRect(app.width//2, 500, 800, 300, align = 'center', fill = 'white')
    lineLeft, lineTop, lineHeight = app.width//2-350, 400+50, 40

    startLine = max(0, app.currentLineIndex - 1)
    wordIndex = app.lineStartIndices[startLine]
    
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

    

class Button:
    def __init__(self, cx, cy, w, h, label=''):
        self.cx, self.cy = cx, cy
        self.w, self.h = w, h
        self.label = label

    def contains(self, mx, my):
        return (self.cx - self.w / 2 <= mx <= self.cx + self.w / 2 and
                self.cy - self.h / 2 <= my <= self.cy + self.h / 2)

    def draw(self, fill='white', border='black',
             labelColor='black', labelSize=22, bold=False):
        drawRect(self.cx, self.cy, self.w, self.h,
                 align='center', fill=fill, border=border)
        if len(self.label)>0:
            drawLabel(self.label, self.cx, self.cy,
                      size=labelSize, fill=labelColor,
                      font='monospace', bold=bold)

# Written by AI

SHOP_CARD_W, SHOP_CARD_H = 200, 200
SHOP_CARD_Y = 500
SHOP_CARD_GAP = 20
NEXT_BTN_W, NEXT_BTN_H = 220, 70

# Written by AI

# Computes centered card positions for a variable number of shop items. 
# Create var / obj under button class
def getShopButtons(app):
    n = len(app.shopItems)
    totalW = n * SHOP_CARD_W + max(0, n - 1) * SHOP_CARD_GAP
    leftX = (app.width - totalW) / 2
    itemButtons = []
    for i in range(n):
        cx = leftX + i * (SHOP_CARD_W + SHOP_CARD_GAP) + SHOP_CARD_W / 2
        itemButtons.append(Button(cx, SHOP_CARD_Y, SHOP_CARD_W, SHOP_CARD_H))
    nextBtn = Button(app.width - NEXT_BTN_W / 2 - 30,
                     app.height - NEXT_BTN_H / 2 - 30,
                     NEXT_BTN_W, NEXT_BTN_H, label='Next Round')
    return itemButtons, nextBtn


# NOT written by AI. Looks fun so I did it myself lol.
# Visual boundary for boosters. Auto line break
def wrapText(text, maxChars):
    lines = []
    curLine = ''
    for word in text.split():
        next = (curLine + ' ' + word) if len(curLine)>0 else word
        if len(next) <= maxChars:
            curLine = next
        else:
            if len(curLine)>0: lines.append(curLine)
            curLine = word
    if len(curLine)>0: lines.append(curLine)
    return lines


# Written by AI
def drawShop(app):
    # --- header: title + money ---
    drawLabel(f'Round {app.runIndex + 1} Complete',
              app.width // 2, 220,
              size=32, bold=True, font='monospace', fill='white')

    drawRect(900, 220, 100, 50, align='center', fill='white')
    drawLabel(f'${app.money}', 900, 220,
              size=28, bold=True, font='monospace')

    # --- next round preview (boss banner if applicable) ---
    nextIdx = app.runIndex + 1
    if nextIdx < len(app.scoreRequirement):
        nextReq = app.scoreRequirement[nextIdx]
        drawLabel(f'Next: Round {nextIdx + 1}    Target: {nextReq}',
                  app.width // 2, 260,
                  size=22, font='monospace', fill='white')
        nextBoss = app.bossSequence[nextIdx]
        if nextBoss is not None:
            # drawRect(app.width // 2, 160, 820, 80,
            #          align='center', fill='darkRed', border='yellow',
            #          borderWidth=3)
            drawLabel(f'BOSS: {nextBoss.name}' +', '+ nextBoss.description,
                      app.width // 2, 300,
                      size=22, bold=True, fill='yellow', font='monospace')


    # --- last-round stats strip ---
    if app.lastStats is not None:
        s = app.lastStats
        stats = [
            ('Chips',    f'{int(s["chips"])}'),
            ('Mult',     f'{s["mult"]:.1f}'),
            ('Score',    f'{int(s["score"])}'),
            ('Mistakes', f'{s["mistakes"]}'),
            ('Accuracy', f'{s["accuracy"] * 100:.0f}%'),
            ('WPM',      f'{s["wpm"]:.0f}'),
        ]
        statsY = 360
        slotW = boardWidth / (len(stats) + 1)
        for i, (k, v) in enumerate(stats):
            x = leftBound + slotW * (i + 1)
            drawLabel(k, x, statsY - 14, size=22,
                      font='monospace', fill='white')
            drawLabel(v, x, statsY + 12, size=18, bold=True,
                      font='monospace', fill='white')

    # --- item cards ---
    itemButtons, nextBtn = getShopButtons(app)
    for i, btn in enumerate(itemButtons):
        item = app.shopItems[i]
        sold = i in app.shopSold
        affordable = app.money >= item.cost

        fill = 'lightGray' if sold else ('white' if affordable else 'pink')
        btn.draw(fill=fill)


        descLabel = wrapText(item.name, 18)
        baseY = btn.cy-btn.h/2 + 30
        for li, line in enumerate(descLabel):
            drawLabel(line, btn.cx, baseY + li * 16, 
                      size=20, bold=True, font='monospace', align='center')
        # drawLabel(item.name, btn.cx, btn.cy - btn.h / 2 + 30,
        #           size=20, bold=True, font='monospace', align='center')

        descLines = wrapText(item.description, 18)
        baseY = btn.cy - 10 - (len(descLines) - 1) * 8
        for li, line in enumerate(descLines):
            drawLabel(line, btn.cx, baseY + li * 16,
                      size=16, font='monospace', align='center')

        drawLabel(f'${item.cost}', btn.cx, btn.cy + btn.h / 2 - 28,
                  size=26, bold=True, font='monospace',
                  fill='green' if affordable else 'red')

        if sold:
            drawLabel('SOLD', btn.cx, btn.cy,
                      size=52, bold=True, fill='red', font='monospace')

    # --- owned boosters strip ---
    # Chip-packing: draw booster name badges left-to-right; if the next chip
    # would overflow maxX, show "+N more" and stop.
    ownedY = 680
    drawLabel(f'Owned ({len(app.boosters)}):',
              leftBound + 30, ownedY-40,
              size=18, bold=True, font='monospace',
              fill='white', align='left')
    # kernels first, macros last (sorted is stable so purchase order kept within each group)
    ordered = sorted(app.boosters, key=lambda b: isinstance(b, booster.Macro))

    charPx = 10         # approximate glyph width at size 16 monospace
    sidePad = 16
    minChipW = 70
    x = 180
    maxX = rightBound - 30  # leave room for the Next Round button
    drawn = 0
    for b in ordered:
        chipW = max(len(b.name) * charPx + sidePad, minChipW)
        if x + chipW > maxX:
            remaining = len(app.boosters) - drawn
            if remaining > 0:
                drawLabel(f'+{remaining} more', x, ownedY,
                          size=16, fill='white',
                          font='monospace', align='left')
            break
        drawRect(x + chipW / 2, ownedY, chipW, 30,
                 align='center', fill='white', border='black')
        drawLabel(b.name, x + chipW / 2, ownedY,
                  size=16, font='monospace')
        x += chipW + 8
        drawn += 1

    # --- next-round button ---
    nextBtn.draw(fill='seaGreen', labelColor='white',
                 labelSize=22, bold=True)




def getScoreButton(app):
    return Button(app.width // 2, app.height - 80, 220, 60, label='Play Again')

def drawScore(app):
    text = 'YOU WIN!' if app.won else 'GAME OVER'
    color = 'green' if app.won else 'red'
    drawLabel(text, app.width // 2, 300,
              size=72, bold=True, font='monospace', fill=color)

    roundReached = app.runIndex + 1
    totalRounds = len(app.scoreRequirement)
    drawLabel(f'Round {roundReached} / {totalRounds}',
              app.width // 2, 400,
              size=28, font='monospace', fill='white')

    if app.lastStats is not None:
        s = app.lastStats
        stats = [
            ('Score',    f'{int(s["score"])}'),
            ('Chips',    f'{int(s["chips"])}'),
            ('Mult',     f'{s["mult"]:.1f}x'),
            ('Mistakes', f'{s["mistakes"]}'),
            ('Accuracy', f'{s["accuracy"] * 100:.0f}%'),
            ('WPM',      f'{s["wpm"]:.0f}'),
        ]
        cardW, cardH = 125, 90
        gap = 20
        totalW = len(stats) * cardW + (len(stats) - 1) * gap
        startX = (app.width - totalW) / 2
        y = 500
        for i, (label, val) in enumerate(stats):
            cx = startX + i * (cardW + gap) + cardW / 2
            drawRect(cx, y, cardW, cardH, align='center', fill='white', border='black')
            drawLabel(label, cx, y - 18, size=18, font='monospace', fill='black')
            drawLabel(val, cx, y + 16, size=26, bold=True, font='monospace', fill='black')

    btn = getScoreButton(app)
    btn.draw(fill='seaGreen', labelColor='white', labelSize=26, bold=True)





# ---------------------------------------------------------------
# Debug harness for drawShop.

# Written by AI

# Run `python view.py` from the project root to preview the shop
# with mock state. Click cards to buy, click Next Round to reroll
# the mock shop, press 'r' to reset to the seeded preview.
# ---------------------------------------------------------------
if __name__ == '__main__':
    import booster as _b
    import random as _r

    def _setupShopState(app):
        app.gameStarted   = True
        app.shopStarted   = True
        app.gameOver      = False
        app.roundStarted  = False
        app.roundEnding   = False
        app.won           = False

        # after round 4; next round is the final boss — banner shows
        app.runIndex         = 3
        app.money            = 15
        app.scoreRequirement = [500, 1200, 2800, 6000, 12000]
        app.bossSequence     = [None, None, None, None, _b.BOSSES[0]]
        app.lastStats = {
            'chips': 820, 'mult': 12.5, 'score': 10250,
            'mistakes': 3, 'accuracy': 0.87, 'wpm': 62,
        }
        # mix: affordable / unaffordable / sold / cheap
        app.shopItems = [_b.KERNELS[0], _b.KERNELS[1],
                         _b.MACROS[4],  _b.MACROS[18]]
        app.shopSold  = {2}
        app.boosters  = [_b.KERNELS[5], _b.MACROS[0], _b.MACROS[7]]

    def onAppStart(app):
        _setupShopState(app)

    def onMousePress(app, mx, my):
        itemButtons, nextBtn = getShopButtons(app)
        for i, btn in enumerate(itemButtons):
            if btn.contains(mx, my):
                if i in app.shopSold: return
                item = app.shopItems[i]
                if app.money >= item.cost:
                    app.money -= item.cost
                    app.boosters.append(item)
                    app.shopSold.add(i)
                return
        if nextBtn.contains(mx, my):
            # reroll shop for repeat inspection; keep other state
            pool = list(_b.KERNELS) + list(_b.MACROS)
            app.shopItems = _r.sample(pool, 4)
            app.shopSold = set()

    def onKeyPress(app, key):
        if key == 'r':
            _setupShopState(app)

    runApp(width=constants.width, height=constants.height)