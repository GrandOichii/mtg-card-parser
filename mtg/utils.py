
class JSONObject:
    def to_json(self):
        return {'type': 'CANT PARSE'}
        return {'type': 'UNKNOWN_COST'}
        raise Exception('to_json NOT IMPLEMENTED')
 
    def from_json(d: dict):
        raise Exception('from_json NOT IMPLEMENTED')
 

NUMS = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
    'eleven',
    'twelve',
    'thirteen',
    'fourteen',
    'sixteen',
    'seventeen',
    'eighteen',
    'nineteen',
    'twenty'
]

class Amount(JSONObject):
    def __init__(self):
        pass

class NumericAmount(JSONObject):
    def __init__(self, amount: int) -> None:
        super().__init__()
        self.amount = amount

    def to_json(self):
        return {
            'type': 'numeric_amount',
            'amount': self.amount
        }