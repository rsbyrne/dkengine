import time
import pickle
import os
import random
import hashlib
import sys
import os
import json
import csv

scriptPath = os.path.abspath(os.path.dirname(__file__))

def start_game(deckName, deckPath = '.', savePath = '.', username = 'anonymous'):
    deck = load_deck(deckName, deckPath)
    saveFiles = [file for file in os.listdir(savePath) if os.path.splitext(file)[1] == '.pkl']
    save_found = False
    for file in saveFiles:
        if username in file and deck[0]['name'] in file:
            save_found = True
    if save_found:
        gameObj = load_game(deck, username, savePath)
        gameObj._message("Loaded " + deckName + " as " + username)
    else:
        gameObj = Game(deck, username, savePath = savePath)
        gameObj._message("Started " + deckName + " as " + username)
    gameObj.start_session()

graphicsDict = {}
graphicsDict['start'] = "\n" + '''\n       \`*-.                    \n        )  _`-.                 \n       .  : `. .                \n       : _   '  \               \n       ; *` _.   `*-._          \n       `-.-'          `-.       \n         ;       `       `.     \n         :.       .        \    \n         . \  .   :   .-'   .   \n         '  `+.;  ;  '      :   \n         :  '  |    ;       ;-. \n         ; '   : :`-:     _.`* ;\n[bug] .*' /  .*' ; .*`- +'  `*' \n      `*-*   `*-*  `*-*'\n    '''
graphicsDict['celebration'] = "\n" +"""\n                                   .''.       """+"""\n       .''.      .        *''*    :_\/_:     . """+"""\n      :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'."""+"""\n  .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-"""+"""\n :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'"""+"""\n : /\ : :::::     *_\/_*     -= o =-  /)\    '  *"""+"""\n  '..'  ':::'     * /\ *     .'/.\'.   '"""+"""\n      *            *..*         :"""+"""\njgs     *"""+"""\n        *"""+"""\n"""
graphicsDict['downer'] = "\n" +"""\n                 /||\ """+"""\n                 |||| """+"""\n                 |||| """+"""\n                 |||| /|\ """+"""\n            /|\  |||| ||| """+"""\n            |||  |||| ||| """+"""\n            |||  |||| ||| """+"""\n            |||  |||| d|| """+"""\n            |||  |||||||/ """+"""\n            ||b._||||~~' """+"""\n            \|||||||| """+"""\n             `~~~|||| """+"""\n                 |||| """+"""\n                 |||| """+"""\n ~~~~~~~~~~~~~~~~||||~~~~~~~~~~~~~~ """+"""\n   \/..__..--  . |||| \/  .  .. """+"""\n \/         \/ \/    \/ """+"""\n         .  \/              \/    . """+"""\n . \/             .   \/     . """+"""\n    __...--..__..__       .     \/ """+"""\n \/  .   .    \/     \/    __..--.. """+"""\n"""
graphicsDict['quit'] = """\n\n           __..--''``\--....___   _..,_ \n       _.-'    .-/";  `        ``<._  ``-+'~=. \n   _.-' _..--.'_    \                    `(^) ) \n  ((..-'    (< _     ;_..__               ; `'   fL \n             `-._,_)'      ``--...____..-' \n"""
graphicsDict['star'] = "\n" +"""\n       ,    """+"""\n    \  :  /    """+"""\n `. __/ \__ .'    """+"""\n _ _\     /_ _    """+"""\n    /_   _\    """+"""\n  .'  \ /  `.    """+"""\n    /  :  \    hjw    """+"""\n       '    """+"""\n"""
graphicsDict['trophy'] = "\n" +"""\n             ___________"""+"""\n            '._==_==_=_.'"""+"""\n            .-\:      /-."""+"""\n           | (|:.     |) |"""+"""\n            '-|:.     |-'"""+"""\n              \::.    /"""+"""\n               '::. .'"""+"""\n                 ) ("""+"""\n               _.' '._"""+'''\n          jgs `"""""""`'''+"""\n"""
graphics = lambda key: print(graphicsDict[key])

def hashID(card):
    cardstring = ''.join(card)
    cardID = int(hashlib.sha256(cardstring.encode('utf-8')).hexdigest(), 16) % 10**8
    return cardID

def load_deck(name, loadPath = '.'):
    extension = os.path.splitext(name)[1]
    print(name, loadPath, extension)
    if extension == '.json':
        return load_deck_json(name, loadPath)
    elif extension == '.csv':
        return load_deck_csv(name, loadPath)
    elif extension == '' and loadPath == '.':
        loadDir = os.path.join(scriptPath, 'content')
        return load_deck_csv(name + '.csv', loadDir)
    else:
        raise Exception

def load_deck_json(name, loadPath = '.'):
    filePath = os.path.join(loadPath, name)
    with open(filePath, 'r') as file:
        deck = json.load(file)
    deck = tuple(deck)
    for index, row in enumerate(deck[1]):
        deck[1][index] = tuple(row)
    return deck

def load_deck_csv(name, loadPath = '.'):
    filePath = os.path.join(loadPath, name)
    data = []
    with open(filePath, 'r', newline = '') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for i, row in enumerate(csv_reader):
            if i == 0:
                header = row
            else:
                data.append(row)
    data = [tuple(row) for row in data]
    headerDict = {
        'name': header[0],
        'question_prompt': header[1],
        'tutorial_prompt': header[2]
        }
    deck = (headerDict, data)
    return deck

def load_game(deck, username, loaddir = '.', name = None):
    if name is None:
        header, cards = deck
        filenameroot = username + '_' + header['name']
        filenames = [
            name for name in os.listdir(loaddir) \
            if filenameroot in name
            ]
        assert len(filenames), \
            "No save file found for this deck and user."
        filename = list(sorted(filenames))[-1] # i.e. load latest
    else:
        filename = name
    filepath = os.path.join(loaddir, filename)
    with open(filepath, 'rb') as file:
        memory = pickle.load(file)
    game = Game(deck, username, _loadmem = memory)
    return game

class Game:

    def __init__(
            self,
            deck = None,
            username = 'default',
            _loadmem = None,
            savePath = '.',
            **kwargs
            ):

        self.username = username
        self.savePath = savePath
        self.header, self.deck = deck

        if _loadmem is None:
            self._standard_init(**kwargs)
        else:
            self._load(_loadmem)
        for key, val in self.options.items():
            setattr(self, key, val)

        # !!! PLACEHOLDER !!!
        self.extra = {card: None for card in self.deck}

    def _standard_init(self, **kwargs):

        self.options = {
            'target_MATTR': 5.,
            'initial_cards': 10,
            'new_cards_at_a_time': 5,
            'recency_limit': 5,
            'random': True,
            'attempts_permitted': 2,
            }

        self.options.update(
            {key: kwargs[key] for key in \
            set(self.options).intersection(set(kwargs))}
            )
        for key, val in self.options.items():
            setattr(self, key, val)

        self.history = []

        self.memory = {
            'options': self.options,
            'history': self.history
            }

    def _load(self, _loadmem):
        self.memory = _loadmem
        for key, val in self.memory.items():
            setattr(self, key, val)

    def save(self, name = None, outputPath = None):
        self._message("Saving...")
        time_str = str(time.time())[:-8]
        if name is None:
            name = self.username \
                + '_' + self.header['name'] \
                + '_' + time_str
        extension = '.pkl'
        if outputPath is None:
            outputPath = self.savePath
        filename = os.path.join(outputPath, name + extension)
        with open(filename, 'wb') as f:
            pickle.dump(self.memory, f, pickle.HIGHEST_PROTOCOL)
        self._message("Saved!")

    def _message(self, text):
        print(text)

    def _get_info(self, card, qtype = 'question'):

        question, answer = card
        if qtype == 'question':
            prompt = self.header['question_prompt']
        elif qtype == 'tutorial':
            prompt = self.header['tutorial_prompt']
        else:
            prompt = "No prompt!"
        extra = self.extra[card]

        return question, answer, prompt, extra

    def _update_history(self, card, outcome):
        cardID = hashID(card)
        new_entry = (round(time.time()), cardID, outcome)
        self.history.append(new_entry)

    def tutorial(self, card):
        self._message("\n")
        self._message("TUTORIAL")
        question, answer, prompt, extra = self._get_info(
            card,
            qtype = 'tutorial'
            )
        self._message(prompt)
        self._message(question)
        self._message(answer)
        while True:
            response = input("Practice: ")
            if response == "exit" or response == "report":
                return response
            else:
                if response == answer:
                    graphics('star')
                    self._message("Gold star!")
                    outcome = None
                    return outcome
                else:
                    self._message("Try again.")

    def question(self, card):
        self._message("\n")
        self._message("QUESTION")
        question, answer, prompt, extra = self._get_info(card)
        starttime = time.time()
        attempts = 0
        self._message(prompt)
        self._message(question)
        while True:
            response = input("Answer: ")
            if response == "exit":
                return response
            elif response == "report":
                self.report()
            elif response == answer:
                graphics('star')
                self._message("Correct!")
                if not extra is None:
                    self._message(extra)
                timelapsed = round(time.time() - starttime)
                return timelapsed
            elif response == "":
                self._message("Passed.")
                return self.tutorial(card)
            elif not attempts < self.attempts_permitted:
                graphics('downer')
                self._message("Incorrect.")
                return self.tutorial(card)
            else:
                self._message("Try again.")

    def choose_random_card(self):
        return random.choice(self.deck)

    def choose_card(self):
        return self.choose_random_card()
    
    def report(self):
        self._message("Nothing to report")

    def start_session(self):
        self._message("Play fair and have fun!")
        graphics('start')
        while True:
            card = self.choose_card()
            outcome = self.question(card)
            if outcome == 'exit':
                break
            else:
                self._update_history(card, outcome) 
        self.save()
        graphics('quit')
        self._message("Rest up - you've earned it!")
