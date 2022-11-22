import re
import json

from mtg.core import *
from mtg.utils import *
from mtg.effect import *

import mtg.core as core

# class Extractor(JSONObject):
#     def __init__(self, l: Line, m: re.Match):
#         pass

# class AbilityExtractor(Extractor):
#     def __init__(self, l: Line, m: re.Match):
#         g = m.groups()
#         print(l.text)
#         # costs = mtg.Cost(g[0])
#         # effect = g[1]

def extract_ability(l: 'Line', m: re.Match):
    g = m.groups()
    print(l.text)
    costs = core.Cost(g[0]) # move line to cost 
    effect = Effect(costs, g[1]) # move line to effect - these both require the references (?)
    print(json.dumps(costs.to_json(), indent=4))
    # print(effect)

EXTRACTOR_MAP = {
    r"(.+): (.+)": extract_ability
}
