timerLen = 20 # 20s per round
chipsPerWord = 5
stepsPerSecond = 30

width = int(1487 * 0.8)
height = int(1116 * 0.8)

fontSize = 26
charWidth = 16

scoreRequirement = [500, 1200, 2800, 6000, 10000]

# Shop item draw weights (macros are individually less likely than kernels
# so the 26 macros don't dominate the 4-slot shop)
kernelWeight = 1.0
macroWeight = 0.3
shopSize = 4