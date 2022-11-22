import re

from mtg.core import *
from mtg.utils import *

MATCHERS: list

class Effect(JSONObject):
    def __init__(self, parent: 'Ability', s: str, l: 'Line'):
        self.parent = parent
        self.effects: list[EffectLine] = []
        lines = s[:-1].split('. ')
        for s in lines:
            found = False
            for matcher in MATCHERS:
                matched = matcher(self, s, l)
                if matched:
                    found = True
            if not found:
                self.effects += [EffectLine(self)]

    def to_json(self):
        result = []
        for effect in self.effects:
            result += [effect.to_json()]
        return result

class EffectLine(JSONObject):
    def __init__(self, parent: Effect):
        self.parent = parent

    def to_json(self):
        return {'type': 'UNKNOWN_EFFECT_LINE'}

'''
Draw cards
'''
class DrawCards_EffectLine(EffectLine):
    def __init__(self, parent: Effect):
        super().__init__(parent)
        self.amount: 'Amount' = None

    def to_json(self):
        return {
            'type': 'draw_cards_effect_line',
            'amount': self.amount.to_json()
        }

DRAW_CARDS_MATCHER = r'Draw (.+) cards'
def draw_cards_matcher(e: 'Effect', s: str, line: 'Line'):
    result = DrawCards_EffectLine(e)
    if s == 'Draw a card':
        amount = NumericAmount(1)
        result.amount = amount
        e.effects += [result]
        return True

    m = re.match(DRAW_CARDS_MATCHER, s)
    if not m:
        return False
    amount = m.groups()[0]
    if amount in NUMS:
        amount = NumericAmount(NUMS.index(amount))
        result.amount = amount
        e.effects += [result]
        return True
    # print('Draw:', m.groups()[0])
    return False

''''''


MATCHERS = [
    draw_cards_matcher
]
