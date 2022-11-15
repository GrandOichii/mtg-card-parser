import json
from mtg import *
 
PATH = 'batch.json'
 
data = json.loads(open(PATH, 'r').read())
cards: list[Card] = []
for chunk in data:
    if 'card_faces' in chunk.keys():
        continue # ignore double faced cards for now
    cards += [Card.from_json(chunk)]
 
for card in cards:
    print(card.name)
    print('\t' + card.text + '\n')
