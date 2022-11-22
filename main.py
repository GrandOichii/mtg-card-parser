import json

from mtg.core import *

CARDS_PATH = 'cards.json'

data = json.loads(open(CARDS_PATH, 'r').read())
cards: list[Card] = []
for chunk in data:
    if 'card_faces' in chunk.keys():
        continue
    if chunk['set_name'].startswith('Un') or chunk['set'].startswith('cmb'):
        continue
    try:
        cards += [Card.from_json(chunk)]
        cards[len(cards)-1].orig = chunk
    except:
        print(json.dumps(chunk, indent=4))

for card in cards:
    # print(card.text)
    if not 'Draw' in card.text: continue
    t = CardText.parse(card.text)
    print(card.name)
    print('\t' + card.text)
    print('PARSED:')
    print(json.dumps(t.to_json(), indent=4))
    print('===')
print('FINISHED')