from mtg.core import *
from mtg.utils import *

MATCHERS: list

class Effect(JSONObject):
    def __init__(self, costs: 'Cost', s: str):
        self.costs = costs
        lines = s.split('. ')
        for matcher in MATCHERS:
            matched = matcher(self)
            if matched: break

DRAW_CARDS_MATCHER = r'Draw (.+) cards'
def draw_cards_matcher(e: 'Effect', line: str):
    
    return True

MATCHERS = [
    draw_cards_matcher
]

