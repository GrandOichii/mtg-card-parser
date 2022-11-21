import json

from mtg.core import *

data = json.loads(open('cards.json', 'r').read())
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
    print(f' === {card.name} ===')
    t = CardText.parse(card.text)
    print('----')
print('FINISHED')