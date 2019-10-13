import os
import csv
import pickle
import json

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
    with open(filePath, 'r', newline = '') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for i, row in enumerate(csv_reader):
            if i == 0:
                header = row
            else:
                data.append(row)
    data = process_data(data)
    headerDict = {
        'name': header[0],
        'question_prompt': header[1],
        'tutorial_prompt': header[2]
        }
    deck = (headerDict, data)
    return deck

def process_data(deck):
    processed = []
    for row in deck:
        newrow = []
        newrow.append(deck[0]) # prompts
        newrow.append(deck[1]) # responses
        if len(newrow) > 2: # extras
            extras = '\n'.join(newrow[2:])
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
