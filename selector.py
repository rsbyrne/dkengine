import random

from . import tools

def cointoss():
    random.seed()
    return random.random() > 0.5

def cointosses(n):
    return [cointoss() for i in range(n)]

class Selector:

    def __init__(self, deck, history):
        self.deck = deck
        self.history = history
        self.cardIDs = {
            tools.hashID(card): card \
                for card in self.deck
            }

    def update(self):
        pass

    def exclude(self, cardID):
        conditions = []
        conditions.append(cardID in self.history.get_last(5))
        conditions.append(self.history.latest_lambdas[cardID] < 1.)
        if any(conditions):
            return True
        return False

    def choose_random_card(self, cardList):
        return random.choice(cardList)

    def _select(self):
        self.update()
        lambdaList = sorted(
            self.history.latest_lambdas.items(),
            key = lambda item: item[1]
            )[::-1]
        for cardID, lambdaVal in lambdaList:
            if not self.exclude(cardID):
                print("Choosing card based on lambda value.")
                return cardID
        unseen_cards = [
            card \
                for card in self.cardIDs.keys() \
                    if not card in self.history.past_cards
            ]
        if all(cointosses(1)) and len(unseen_cards) > 0:
            print("Choosing random card from unseen cards.")
            return self.choose_random_card(unseen_cards)
        legit_past_cards = [
            card \
                for card in self.history.past_cards \
                    if not card in self.history.get_last(5)
            ]
        if len(legit_past_cards) > 0:
            print("Choosing random card from past cards.")
            return self.choose_random_card(legit_past_cards)
        print("Choosing random card from all cards.")
        return self.choose_random_card(self.cardIDs.keys())

    def select(self):
        selectedID = self._select()
        selected = self.cardIDs[selectedID]
        return selected
