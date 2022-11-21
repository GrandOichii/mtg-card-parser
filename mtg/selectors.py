import re

from mtg.utils import *
from mtg.core import *

class Selector(JSONObject):
    def __init__(self, selected: str, options: list[str]):
        self.selected: str = selected
        self.options: list[str] = options
        
def generate_selectors(selected: str, options: list[str], l: 'Line'):
    r = '((?:(?:'
    for i, t in enumerate(options):
        if i != 0:
            r += '|'
        r += f'\\b{t}\\b|\\bnon{t}\\b'
    r += r')[,]? )+)' + selected
    matches = re.finditer(r, l.text) # replace with finditer
    if not matches:
        return
    for m in matches:
        s = m.groups()[0] + selected
        ts = m.groups()[0][:-1].split(', ')
        key = f'%s{len(l.selectors)}%'
        l.text = l.text.replace(s, key, 1)
        l.selectors += [Selector(selected, ts)]
    if len(list(matches)) >= 2:
        return
    return