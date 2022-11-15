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
        result.text = result.text.replace(result.name, CARDNAME_T)
        return result

    def print(self):
        print(self.name)
        print(f'\t{self.text}\n')
 
# effects that say 'if' or 'as long as'
class Condition(JSONObject):
    pass
 
class ManaPip(Condition):
    def __init__(self) -> None:
        pass

class CostPart(JSONObject):
    pass
 
