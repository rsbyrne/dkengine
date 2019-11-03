import time
import pickle
import os
import math

from . import tools
from . import selector
from . import history
from . import load

def start_game(deckName, deckPath = '.', savePath = 'saves', username = 'anonymous'):
    deck = load.load_deck(deckName, deckPath)
    if not os.path.isdir(savePath):
        os.mkdir(savePath)
    saveFiles = [file for file in os.listdir(savePath) if os.path.splitext(file)[1] == '.pkl']
    save_found = False
    for file in saveFiles:
        if username in file and deck[0]['name'] in file:
            save_found = True
    if save_found:
        gameObj = load_game(deck, username, savePath)
        gameObj.message("Loaded " + deckName + " as " + username)
    else:
        gameObj = Game(deck, username, savePath = savePath)
        gameObj.message("Started " + deckName + " as " + username)
    gameObj.start_session()

def load_game(*args, **kwargs):
    deck, username, memory = load._load_game(*args, **kwargs)
    return Game(deck, username, _loadmem = memory)

graphicsDict = {}
graphicsDict['start'] = "\n" + '''\n       \`*-.                    \n        )  _`-.                 \n       .  : `. .                \n       : _   '  \               \n       ; *` _.   `*-._          \n       `-.-'          `-.       \n         ;       `       `.     \n         :.       .        \    \n         . \  .   :   .-'   .   \n         '  `+.;  ;  '      :   \n         :  '  |    ;       ;-. \n         ; '   : :`-:     _.`* ;\n[bug] .*' /  .*' ; .*`- +'  `*' \n      `*-*   `*-*  `*-*'\n    '''
graphicsDict['celebration'] = "\n" +"""\n                                   .''.       """+"""\n       .''.      .        *''*    :_\/_:     . """+"""\n      :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'."""+"""\n  .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-"""+"""\n :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'"""+"""\n : /\ : :::::     *_\/_*     -= o =-  /)\    '  *"""+"""\n  '..'  ':::'     * /\ *     .'/.\'.   '"""+"""\n      *            *..*         :"""+"""\njgs     *"""+"""\n        *"""+"""\n"""
graphicsDict['downer'] = "\n" +"""\n                 /||\ """+"""\n                 |||| """+"""\n                 |||| """+"""\n                 |||| /|\ """+"""\n            /|\  |||| ||| """+"""\n            |||  |||| ||| """+"""\n            |||  |||| ||| """+"""\n            |||  |||| d|| """+"""\n            |||  |||||||/ """+"""\n            ||b._||||~~' """+"""\n            \|||||||| """+"""\n             `~~~|||| """+"""\n                 |||| """+"""\n                 |||| """+"""\n ~~~~~~~~~~~~~~~~||||~~~~~~~~~~~~~~ """+"""\n   \/..__..--  . |||| \/  .  .. """+"""\n \/         \/ \/    \/ """+"""\n         .  \/              \/    . """+"""\n . \/             .   \/     . """+"""\n    __...--..__..__       .     \/ """+"""\n \/  .   .    \/     \/    __..--.. """+"""\n"""
graphicsDict['quit'] = """\n\n           __..--''``\--....___   _..,_ \n       _.-'    .-/";  `        ``<._  ``-+'~=. \n   _.-' _..--.'_    \                    `(^) ) \n  ((..-'    (< _     ;_..__               ; `'   fL \n             `-._,_)'      ``--...____..-' \n"""
graphicsDict['star'] = "\n" +"""\n       ,    """+"""\n    \  :  /    """+"""\n `. __/ \__ .'    """+"""\n _ _\     /_ _    """+"""\n    /_   _\    """+"""\n  .'  \ /  `.    """+"""\n    /  :  \    hjw    """+"""\n       '    """+"""\n"""
graphicsDict['trophy'] = "\n" +"""\n             ___________"""+"""\n            '._==_==_=_.'"""+"""\n            .-\:      /-."""+"""\n           | (|:.     |) |"""+"""\n            '-|:.     |-'"""+"""\n              \::.    /"""+"""\n               '::. .'"""+"""\n                 ) ("""+"""\n               _.' '._"""+'''\n          jgs `"""""""`'''+"""\n"""
graphics = lambda key: print(graphicsDict[key])

class Game:

    def __init__(
            self,
            deck = None,
            username = 'default',
            _loadmem = None,
            savePath = 'saves',
            **kwargs
            ):

        self.username = username
        self.savePath = savePath
        self.superHeader, self.header, self.deck = deck

        if _loadmem is None:
            self._standard_init(**kwargs)
        else:
            self._load(_loadmem)
        self.history = history.History(self.memory['history'])
        self.options = self.memory['options']

        self.ordered = self.superHeader['ordered'] == 'True'
        self.reversible = self.superHeader['reversible'] == 'True'

        self.selector = selector.Selector(
            self.deck,
            self.history,
            ordered = self.ordered
            )


        self._update_attributes()

    def _standard_init(self, **kwargs):

        options = {
            }

        options.update(
            {key: kwargs[key] for key in \
            set(options).intersection(set(kwargs))}
            )

        self.memory = {
            'options': options,
            'history': []
            }

    def _load(self, _loadmem):
        self.memory = _loadmem

    def save(self, name = None, outputPath = None):
        self.message("Saving...")
        time_str = str(round(time.time()))
        if name is None:
            name = self.username \
                + '_' + self.superHeader['name'] \
                + '_' + time_str
        extension = '.pkl'
        if outputPath is None:
            outputPath = self.savePath
        filename = os.path.join(outputPath, name + extension)
        with open(filename, 'wb') as f:
            pickle.dump(self.memory, f, pickle.HIGHEST_PROTOCOL)
        self.message("Saved!")

    def message(self, text):
        print(text)

    def graphics(self, key):
        self.message(graphicsDict[key])

    def _get_info(self, card, qtype = 'question'):

        context, prompt, response, hook, pretag, cotag, tutorial, extra = card
        if qtype == 'question':
            instruction = context
        elif qtype == 'tutorial':
            instruction = tutorial
        else:
            instruction = ""

        return prompt, response, hook, instruction, extra

    def _update_attributes(self):
        pass

    def _process_outcome(self, outcome):
        grace_time = 3.
        if outcome is None:
            performance = 0.
        else:
            outcome = max(0., outcome - grace_time)
            outcome_power = math.log2(outcome + 1.)
            if outcome_power > 3.:
                performance = 0.
            else:
                performance = round(1. - (outcome_power / 3.), 2)
        return performance

    def _update_history(self, card, outcome):
        cardID = tools.hashID(card)
        performance = self._process_outcome(outcome)
        new_entry = (round(time.time()), cardID, performance)
        self.history.data.append(new_entry)
        self.memory['history'] = self.history.data
        self.history.update()

    def update(self, card, outcome):
        self._update_history(card, outcome)
        self._update_attributes()

    def countdown(self, secs):
        self.message('x')
        time.sleep(secs)
        self.message('>')
        # for sec in list(range(int(secs)))[::-1]:
        #     self.message('.')
        #     time.sleep(1)

    def tutorial(self, card, reversed = False):
        self.message("\n")
        self.message("TUTORIAL")
        question, answer, hook, instruction, extra = self._get_info(
            card,
            qtype = 'tutorial'
            )
        if reversed:
            oldquestion, oldanswer = question, answer
            question = oldanswer
            answer = oldquestion
        self.message(question)
        self.message(answer)
        self.message(hook)
        self.message(extra)
        self.countdown(3)
        self.message(instruction)
        while True:
            self.message("Prompt: " + question)
            response = input("Type the prompt:\n")
            if response == "exit" or response == "report":
                return response
            else:
                if response == question:
                    break
                else:
                    self.message("Try again.")
        while True:
            self.message("Response: " + answer)
            response = input("Now type the response:\n")
            if response == "exit" or response == "report":
                return response
            else:
                if response == answer:
                    self.graphics('star')
                    self.message("Gold star!")
                    outcome = None
                    return outcome
                else:
                    self.message("Try again.")

    def question(self, card):
        self.message("\n")
        self.message("QUESTION")
        question, answer, hook, instruction, extra = self._get_info(card)
        reversed = False
        if self.reversible:
            if selector.cointoss():
                oldquestion, oldanswer = question, answer
                question = oldanswer
                answer = oldquestion
                reversed = True
        starttime = time.time()
        attempts = 0
        self.message(instruction)
        self.message(question)
        self.countdown(3)
        while True:
            response = input("Answer:\n")
            if response == "exit":
                return response
            elif response == "report":
                self.report()
            elif response == answer:
                timelapsed = time.time() - starttime
                if self._process_outcome(timelapsed) == 0.:
                    self.message("Too slow.")
                    return self.tutorial(card, reversed)
                self.graphics('star')
                self.message("Correct!")
                self.message(extra)
                return timelapsed
            elif attempts == 0:
                self.message(hook)
                self.message("Have a think...")
                self.countdown(3)
            elif attempts > 0:
                if response == "":
                    self.message("Passed.")
                    return self.tutorial(card, reversed)
                else:
                    self.graphics('downer')
                    self.message("Incorrect.")
                    return self.tutorial(card, reversed)
            else:
                raise Exception

    def get_card(self):
        return self.selector.select()

    def report(self):
        self.message("Nothing to report")

    def question_loop(self):
        card = self.get_card()
        if not tools.hashID(card) in self.history.past_cards:
            self.graphics('trophy')
            self.message('New card unlocked!')
            outcome = self.tutorial(card)
        else:
            outcome = self.question(card)
        if outcome == 'exit':
            return "exit"
        else:
            self.update(card, outcome)
            return "continue"

    def start_session(self):
        self.message("Welcome back " + self.username + '!')
        self.graphics('start')
        status = 'continue'
        while status == 'continue':
            status = input("Press enter to continue or type 'exit' to exit.\n")
            if status == 'exit':
                break
            else:
                status = self.question_loop()
        self.save()
        self.graphics('quit')
        self.message("Have a break - have a kit kat.")
