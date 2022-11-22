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
    costs = core.Cost(result, g[0], l)
    effect = Effect(result, g[1], l)
    result.cost = costs
    result.effect = effect
    if len(result.zones) == 0:
        result.zones = [BATTLEFIELD_ZONE]
    t.abilities += [result]
    return True

EXTRACTORS = {
    extract_ability
}
