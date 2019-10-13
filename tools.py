import hashlib
import os
import csv

def hashID(card):
    card = list(sorted(card[:2]))
    cardstring = ''.join(card)
    cardID = int(hashlib.sha256(cardstring.encode('utf-8')).hexdigest(), 16)
    return cardID

def make_cardHistories(history):
    cardDict = {}
    for unixtime, cardID, score in history:
        if not cardID in cardDict:
            cardDict[cardID] = []
        cardDict[cardID].append((unixtime, score))
    for key in cardDict:
        cardDict[key] = sorted(cardDict[key])
    return cardDict

def make_cardHistory(cardID, history):
    cardDict = make_cardDict(history)
    if cardID in cardDict:
        return make_cardDict(history)[cardID]
    else:
        return None

def make_csv_from_quizObj(quizObj):
    header, deck = quizObj
    fileName = header['name'] + '.csv'
    outputPath = os.path.join(__file__, 'content')
    filePath = os.path.join(outputPath, fileName)
    with open(filePath, 'w', newline = '') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([val for key, val in sorted(header.items())])
        csv_writer.writerows(deck)
