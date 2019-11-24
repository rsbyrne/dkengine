import time
import pickle
import os
import math

from . import tools
from . import selector
from . import history
from . import load

def start_game(deckName, deckPath = '.', savePath = 'saves', username = 'anonymous'):
    superHeader, deck = load.load_deck(deckName, deckPath)
    if not os.path.isdir(savePath):
        os.mkdir(savePath)
    saveFiles = [file for file in os.listdir(savePath) if os.path.splitext(file)[1] == '.pkl']
    save_found = False
    for file in saveFiles:
        if username in file and superHeader['name'] in file:
            save_found = True
    if save_found:
        gameObj = load_game(superHeader, deck, username, savePath)
        gameObj.message("Loaded " + deckName + " as " + username)
    else:
        gameObj = Game(superHeader, deck, username, savePath = savePath)
        gameObj.message("Started " + deckName + " as " + username)
    gameObj.start_session()

def load_game(*args, **kwargs):
    superHeader, deck, username, memory = load._load_game(*args, **kwargs)
    return Game(superHeader, deck, username, _loadmem = memory)

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
            superHeader,
            deck = None,
            username = 'default',
            _loadmem = None,
            savePath = 'saves',
            **kwargs
            ):

        self.username = username
        self.savePath = savePath
        self.superHeader = superHeader
        self.deck = deck

        if _loadmem is None:
            self._standard_init(**kwargs)
        else:
            self._load(_loadmem)
        self.history = history.History(self.memory['history'])
        self.options = self.memory['options']

        if 'ordered' in self.superHeader:
            self.ordered = eval(self.superHeader['ordered'])
        else:
            self.ordered = False
        if 'reversible' in self.superHeader:
            self.reversible = eval(self.superHeader['reversible'])
        else:
            self.reversible = False

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

    def _get_info(self, card):
        data, extras = card
        context, prompt, responses = data
        response = '; '.join(responses)
        response.rstrip()
        return context, prompt, response, extras

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

    def tutorial(self, card):
        self.message("\n")
        self.message("TUTORIAL")
        context, prompt, response, extras = self._get_info(card)
        self.message(extras)
        self.countdown(2)
        self.message(context)
        while True:
            self.message("Read and repeat:")
            typedback = input(prompt + '\n')
            if typedback == "exit" or typedback == "report":
                return typedback
            else:
                if typedback == prompt:
                    break
                else:
                    self.message("Try again.")
        while True:
            typedback = input(response + '\n')
            if typedback == "exit" or typedback == "report":
                return typedback
            else:
                if typedback == response:
                    self.graphics('star')
                    self.message("Gold star!")
                    outcome = None
                    return outcome
                else:
                    self.message("Try again.")

    def question(self, card):
        self.message("\n")
        self.message("QUESTION")
        context, prompt, response, extras = self._get_info(card)
        response
        starttime = time.time()
        attempts = 0
        self.message(context)
        self.message(prompt)
        self.countdown(2)
        while True:
            typedback = input("Answer:\n")
            if typedback == "exit":
                return typedback
            elif typedback == "report":
                self.report()
            elif typedback == "":
                self.message("Passed.")
                return self.tutorial(card)
            elif typedback == response:
                timelapsed = time.time() - starttime
                if self._process_outcome(timelapsed) == 0.:
                    self.message("Too slow.")
                    return self.tutorial(card)
                self.graphics('star')
                self.message("Correct!")
                self.message(extras)
                return timelapsed
            elif attempts == 0:
                attempts += 1
                self.message("Have a think...")
                self.countdown(2)
            elif attempts > 0:
                self.graphics('downer')
                self.message("Incorrect.")
                return self.tutorial(card)
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
