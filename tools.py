import hashlib

def hashID(card):
    cardstring = ''.join(card[:2])
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
