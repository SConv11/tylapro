# Wordbanks are taken directly from https://github.com/monkeytypegame/monkeytype

import json
import random

def generateWordList(numWords, hard=False, punc = False) -> list[str]:

    if hard: filename = 'english_5k.json'
    else: filename = 'english.json'

    with open(filename, 'r') as f:
        wordbank = json.load(f)["words"]

    res = random.choices(wordbank, k=numWords)

    if punc:
        res[0] = res[0][0].upper() + res[0][1:]
        for i in range(len(res)-1):
            if random.random() < 0.3: 
                res[i] += random.choice(['.', ',', '!', '?', ';', ':'])
            if res[i][-1] in ['.', '!', '?']: 
                res[i+1] = res[i+1][0].upper() + res[i+1][1:]
        res[-1] += random.choice(['.', '!', '?'])

    return res


# print(generateWordList(100, hard=True))
# print('--------------------------------------------------------------------')
# print(generateWordList(100))
# print('--------------------------------------------------------------------')
# print(generateWordList(100, punc=True))

