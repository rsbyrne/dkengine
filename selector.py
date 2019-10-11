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

    def retrieve_random_card(self, cardList = None):
        if cardList is None:
            cardList = [
                card \
                    for card in self.cardIDs.keys() \
                        if not card in self.history.get_last(5)
                ]
            if len(cardList) == 0:
                print("Choosing random card from all cards.")
                cardList = self.cardIDs.keys()
        return random.choice(cardList)

    def retrieve_random_past_card(self):
        legit_past_cards = [
            card \
                for card in self.history.past_cards \
                    if not card in self.history.get_last(5)
            ]
        if len(legit_past_cards) > 0:
            print("Choosing random card from past cards.")
            return self.retrieve_random_card(legit_past_cards)
        else:
            return self.retrieve_random_card()

    def retrieve_new_card(self):
        unseen_cards = [
            card \
                for card in self.cardIDs.keys() \
                    if not card in self.history.past_cards
            ]
        if len(unseen_cards) > 0:
            print("Choosing random card from unseen cards.")
            return self.retrieve_random_card(unseen_cards)
        else:
            return self.retrieve_random_card()

    def retrieve_worst_lambda(self):
        lambdaList = sorted(
            self.history.latest_lambdas.items(),
            key = lambda item: item[1]
            )
        cardList = [item[0] for item in lambdaList]
        cardList = [
            card \
                for card in [item[0] for item in lambdaList] \
                    if not card in self.history.get_last(5)
            ]
        if len(cardList) > 0:
            print("Choosing card based on highest lambda value.")
            return cardList[-1]
        else:
            return self.retrieve_random_past_card()

    def new_card_condition(self):
        return all(cointosses(3))

    def _select(self):
        self.update()
        if self.new_card_condition():
            return self.retrieve_new_card()
        else:
            if cointoss():
                return self.retrieve_worst_lambda()
            else:
                return self.retrieve_random_past_card()

    def select(self):
        selectedID = self._select()
        selected = self.cardIDs[selectedID]
        return selected