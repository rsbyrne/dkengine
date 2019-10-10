from . import tools
from . import analysis

def get_last(cards, n):
    last_n = cards[-min(len(cards), n):]
    return last_n

class History:

    def __init__(
            self,
            data = []
            ):

        self.data = data

        self.update()

    def update(self):

        self.card_histories = tools.make_cardHistories(self.data)

        self.card_lambdas = analysis.observe_all_lambdas(self)
        self.latest_lambdas = {}
        for key, val in self.card_lambdas.items():
            if len(val) > 0:
                self.latest_lambdas[key] = val[-1]

        self.time_IDs = list(sorted([(row[0], row[1]) for row in self.data]))
        self.past_cards = []
        for timeID, cardID in self.time_IDs[::-1]:
            if not cardID in self.past_cards:
                self.past_cards.append(cardID)
        self.past_cards = self.past_cards[::-1]

    def get_last(self, n):
        return get_last(self.past_cards, n)
