import os
import csv
import pickle
import json
import codecs
from collections import OrderedDict
from tools import hashID

scriptPath = os.path.abspath(os.path.dirname(__file__))

def load_deck(name, loadPath = '.'):
    extension = os.path.splitext(name)[1]
    if extension == '.json':
        raise Exception("Not supported currently.")
        # return load_deck_json(name, loadPath)
    elif extension == '.csv':
        return load_deck_csv(name, loadPath)
    elif extension == '' and loadPath == '.':
        loadDir = os.path.join(scriptPath, 'content')
        return load_deck_csv(name + '.csv', loadDir)
    else:
        raise Exception

# def load_deck_json(name, loadPath = '.'):
    # filePath = os.path.join(loadPath, name)
    # with open(filePath, 'r') as file:
    #     deck = json.load(file)
    # deck = tuple(deck)
    # for index, row in enumerate(deck[1]):
    #     deck[1][index] = tuple(row)
    # return deck

def load_deck_csv(name, loadPath = '.'):
    filePath = os.path.join(loadPath, name)
    data = []
    # with open(filePath, 'r', newline = '') as csv_file:
    with codecs.open(filePath, 'r', 'utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        for i, row in enumerate(csv_reader):
            if i == 0:
                superHeader = row[0].split(';')
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
    deck = process_data(data, header, superHeaderDict)
    return superHeaderDict, deck

def process_data(data, header, superHeader):
    deck = []
    assert not 'prerequisites' in superHeader and 'reversible' in superHeader
    context = superHeader['context']
    norm_context = context + ': ' + header[0] + ' --> ' + header[1]
    rev_context = context + ': ' + header[1] + ' --> ' + header[0]
    process_entry = lambda entry, delim: \
        tuple([subEntry.strip() for subEntry in entry.split(delim)])
    for row in data:
        prompts = process_entry(row[0], ';')
        responses = process_entry(row[1], ';')
        extras = OrderedDict(zip(
            [*header[2:], *header[:2]],
            [*row[2:], *row[:2]]
            ))
        for prompt in prompts:
            prereqs = []
            entry = ((norm_context, prompt, responses), prereqs, extras)
            deck.append(entry)
        if 'reversible' in superHeader:
            if eval(superHeader['reversible']):
                for response in responses:
                    prereqs = []
                    entry = ((rev_context, response, prompts), prereqs, extras)
                    deck.append(entry)
    if 'prerequisites' in superHeader:
        prereqCol = superHeader['prerequisites']
        hashIDs = dict([(c[0][1], hashID(c)) for c in cards])
        for data, prereqs, extras in deck:
            prereqs.extend([
                [hashIDs[c] for c in process_entry(cs, ',')]
                    for cs in process_entry(extras[prereqCol], ';')
                ])
    return deck

def load_memory(name, path):
    filepath = os.path.join(path, name)
    with open(filepath, 'rb') as file:
        memory = pickle.load(file)
    return memory

def _load_game(superHeader, deck, username, loaddir = '.', name = None):
    if name is None:
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
    return superHeader, deck, username, memory
