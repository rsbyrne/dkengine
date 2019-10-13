import os
import csv
import pickle
import json
import codecs

scriptPath = os.path.abspath(os.path.dirname(__file__))

def load_deck(name, loadPath = '.'):
    extension = os.path.splitext(name)[1]
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
    # with open(filePath, 'r', newline = '') as csv_file:
    with codecs.open(filePath, 'r', 'utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for i, row in enumerate(csv_reader):
            if i == 0:
                header = row
            else:
                data.append(row)
    data = process_data(data)
    headerDict = {
        key: val \
            for key, val in [entry.split('=') for entry in header]
        }
    deck = (headerDict, data)
    return deck

def process_data(data):
    processed = []
    for row in data:
        newrow = []
        newrow.append(row[0]) # prompts
        newrow.append(row[1]) # responses
        if len(row) > 2: # extras
            extras = '\n'.join(row[2:])
            newrow.append(extras)
        else:
            newrow.append('')
        newrow = tuple(newrow)
        processed.append(newrow)
    return processed

def load_memory(name, path):
    filepath = os.path.join(path, name)
    with open(filepath, 'rb') as file:
        memory = pickle.load(file)
    return memory

def _load_game(deck, username, loaddir = '.', name = None):
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
    memory = load_memory(filename, loaddir)
    return deck, username, memory
