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
                superHeader = row
            elif i == 1:
                header = row
            else:
                data.append(row)
    superHeaderDict = {
        key: val \
            for key, val in [
                entry.split('=') \
                    for entry in superHeader \
                        if len(entry) > 0
                ]
        }
    data = process_data(data, header, superHeaderDict)
    deck = (superHeaderDict, header, data)
    return deck

def process_data(data, header, superHeader):
    processed = []
    for row in data:
        rowDict = {key: val for key, val in zip(header, row)}
        newrow = []
        newrow.append(superHeader['context'])
        for key in ['prompt', 'response', 'hook', 'pretags', 'cotags']:
            try:
                newrow.append(rowDict.pop(key))
            except:
                newrow.append('')
        newrow.append(superHeader['tutorial'])
        extrasList = [rowDict[key] for key in header if key in rowDict]
        extras = '\n'.join(extrasList)
        newrow.append(extras)
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
        superHeader, header, cards = deck
        filenameroot = username + '_' + superHeader['name']
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
