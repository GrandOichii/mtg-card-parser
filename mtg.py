'''
When [CARDNAME] (*), (*).
Whenever (*).
(*): (*) -- activated ability
Enchant (*)
As (*), (*).
At the (*) of (*), (*).

when - watches [CARDNAME] enter the battlefield
whenever - watches for other effects
'''
 
import json

IGNORE_TEXT = [
    ' (Draw a card, then discard a card. If you discarded a nonland card, put a +1/+1 counter on this creature.)',
    ' (Equipment, Auras you control, and counters are modifications.)',
    ' (It\'s an artifact with "{T}, Sacrifice this artifact: Add one mana of any color.")',
    ' (Create a Clue token. It\'s an artifact with "{2}, Sacrifice this artifact: Draw a card.)',
    ' (They\'re artifacts with "{T}, Sacrifice this artifact: Add one mana of any color.")',
    ' (The next time this creature would be destroyed, instead tap it, remove it from combat, and heal all damage on it.)'
]
 
CARDNAME_T = '[CARDNAME]'
 
COLORS = [
    'white',
    'blue',
    'black',
    'red',
    'green'
]
 
# WHITE_C = 'white'
# BLUE_C = ''
 
COLOR_PIP_MAP = {
    'white': 'W',
    'blue': 'U',
    'black': 'B',
    'red': 'R',
    'green': 'G'
}
 
class JSONObject:
    def to_json(self) -> dict:
        raise 'to_json NOT IMPLEMENTED'
 
    def from_json(d: dict):
        raise 'from_json NOT IMPLEMENTED'
 
class Card(JSONObject):
    def __init__(self) -> None:
        self.name: str = ''
        self.text: str = ''
    
    def from_json(d: dict):
        result = Card()
        result.name = d['name']
        result.text = d['oracle_text']
        result.format_text()
        return result

    def print(self):
        print(self.name)
        print(f'\t{self.text}\n')

    def format_text(self):
        # replace card name occurences
        self.text = self.text.replace(self.name, CARDNAME_T)
        # replace reminder text
        for i in IGNORE_TEXT:
            self.text = self.text.replace(i, '')

# effects that say 'if' or 'as long as'
class Cost(JSONObject):
    def parse(s: str):
        print(s)

class Tap(JSONObject):
    def __init__(self):
        pass
 
class ManaPip(Cost):
    def __init__(self, s: str) -> None:
        self.generic = 0
        self.color: str = ''
        self.lifeAltCost = 0
        self.alt: ManaPip = None
