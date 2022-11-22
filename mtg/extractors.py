import re
import json

from mtg.core import *
from mtg.utils import *
from mtg.effect import *

import mtg.core as core

def extract_ability(l: 'Line', t: 'CardText'):
    m = re.match(r"(.+): (.+)", l.text)
    if not m:
        return False
    g = m.groups()
    result = core.Ability()
    costs = core.Cost(g[0], l) # move line to cost 
    effect = Effect(result, g[1], l) # move line to effect - these both require the references (?)
    result.cost = costs
    result.effect = effect
    # print(l.text)
    # print(json.dumps(effect.to_json(), indent=4))
    # print(effect)
    t.abilities += [result]
    return True

EXTRACTORS = {
    extract_ability
}
