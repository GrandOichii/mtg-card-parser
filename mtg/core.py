import json
import re

from mtg.utils import *
from mtg.selectors import *
from mtg.extractors import *
import mtg.color as color
 
CARDNAME_T = '[CARDNAME]'

MANA_PIP_R = r'(\{[^E]\})'

REPLACE_REMINDER_R = r'(\(.+\))'

CARD_TYPES = [
    'creature',
    'land',
    'instant',
    'sorcery',
    'basic land'
] + color.COLORS

ABILITY_WORDS = [
    'Adamant — ',
    'Addendum — ',
    'Alliance — ',
    'Battalion — ',
    'Bloodrush — ',
    'Channel — ',
    'Chroma — ',
    'Cohort — ',
    'Constellation — ',
    'Converge — ',
    'Council’s dilemma — ',
    'Coven — ',
    'Delirium — ',
    'Domain — ',
    'Eminence — ',
    'Enrage — ',
    'Fateful hour — ',
    'Ferocious — ',
    'Formidable — ',
    'Grandeur — ',
    'Hellbent — ',
    'Heroic — ',
    'Imprint — ',
    'Inspired — ',
    'Join forces — ',
    'Kinship — ',
    'Landfall — ',
    'Lieutenant — ',
    'Magecraft — ',
    'Metalcraft — ',
    'Morbid — ',
    'Pack tactics — ',
    'Parley — ',
    'Radiance — ',
    'Raid — ',
    'Rally — ',
    'Revolt — ',
    'Spell mastery — ',
    'Strive — ',
    'Sweep — ',
    'Tempting offer — ',
    'Threshold — ',
    'Undergrowth — ',
    'Will of the council — '
]

FLAVOR_WORDS = [
    'Acid Breath — ',
    'Animate Walking Statue — ',
    'Antimagic Cone — ',
    'Archery — ',
    'Bardic Inspiration — ',
    'Beacon of Hope — ',
    'Bear Form — ',
    'Befriend Them — ',
    'Bewitching Whispers — ',
    'Binding Contract — ',
    'Brave the Stench — ',
    'Break Their Chains — ',
    'Charge Them — ',
    'Clever Conjurer — ',
    'Climb Over — ',
    'Combat Inspiration — ',
    'Cold Breath — ',
    'Cone of Cold — ',
    'Cunning Action — ',
    'Cure Wounds — ',
    'Dispel Magic — ',
    'Displacement — ',
    'Dissolve — ',
    'Distract the Guard — ',
    'Divine Intervention — ',
    'Dominate Monster — ',
    'Drag Below — ',
    'Engulf — ',
    'Fear Ray — ',
    'Fend Them Off — ',
    'Fight the Current — ',
    'Find a Crossing — ',
    'Flurry of Blows — ',
    'Foil Their Scheme — ',
    'Form a Party — ',
    'Gentle Repose — ',
    'Grant an Advantage — ',
    'Hide — ',
    'Interrogate Them — ',
    'Intimidate Them — ',
    'Journey On — ',
    'Keen Senses — ',
    'Learn Their Secrets — ',
    'Life Drain — ',
    'Lift the Curse — ',
    'Lightning Breath — ',
    'Magical Tinkering — ',
    'Make a Retreat — ',
    'Make Camp — ',
    'Poison Breath — ',
    'Pry It Open — ',
    'Psionic Spells — ',
    'Rappel Down — ',
    'Rejuvenation — ',
    'Rouse the Party — ',
    'Search the Body — ',
    'Search the Room — ',
    'Set Off Traps — ',
    'Siege Monster — ',
    'Smash It — ',
    'Smash the Chest — ',
    'Song of Rest — ',
    'Split — ',
    'Stand and Fight — ',
    'Start a Brawl — ',
    'Steal Its Eyes — ',
    'Stunning Strike — ',
    'Tail Spikes — ',
    'Teleport — ',
    'Tie Up — ',
    'Tragic Backstory — ',
    'Trapped! — ',
    'Two-Weapon Fighting — ',
    'Whirlwind — ',
    'Whispers of the Grave — ',
    'Wild Magic Surge — ',
    'Astral Projection — ',
    'Berserk — ',
    'Breathe Flame — ',
    'Create Undead — ',
    'Enrage — ',
    'Focus Beam — ',
    'Mystic Arcanum — ',
    'Negative Energy Cone — ',
    'Pact Boon — ',
    'Perfect Illumination — ',
    'Smash Relics — ',
    'Electric Thunder — ',
    'Fierce Punch — ',
    'Flash Kick — ',
    'Hadoken — ',
    'Hundred Hand Slap — ',
    'Iron Muscle — ',
    'Lightning Kick — ',
    'Rolling Attack — ',
    'Teleport — ',
    'Shoryuken — ',
    'Sonic Boom — ',
    'Spinning Piledriver — ',
    'Sumo Spirit — ',
    'Animate Chains — ',
    'Avoidance — ',
    'Bigby\'s Hand — ',
    'Blood Drain — ',
    'Body Thief — ',
    'Bribe the Guards — ',
    'Call for Aid — ',
    'Ceremorphosis — ',
    'Confounding Clouds — ',
    'Conjure Elemental — ',
    'Crown of Madness — ',
    'Death Ray — ',
    'Devour Intellect — ',
    'Disintegration Ray — ',
    'Enthralling Performance — ',
    'Feed — ',
    'Friends — ',
    'Gathered Swarm — ',
    'Gather Your Courage — ',
    'Gust of Wind — ',
    'Homunculus Servant — ',
    'Infesting Spores — ',
    'Keen Sight — ',
    'Lure the Unwary — ',
    'Mama\'s Coming — ',
    'Mantle of Inspiration — ',
    'Mold Harvest — ',
    'Natural Recovery — ',
    'Natural Shelter — ',
    'Pray for Protection — ',
    'Protection Fighting Style — ',
    'Psychic Blades — ',
    'Psychic Defense — ',
    'Run and Hide — ',
    'Scorching Ray — ',
    'Sleight of Hand — ',
    'Spiked Retribution — ',
    'Stall for Time — ',
    'Strike a Deal — ',
    'Threaten the Merchant — ',
    'Toxic Spores — ',
    'Vicious Mockery — ',
    'Weird Insight — ',
    'Wind Walk — ',
    'Aberrant Tinkering — ',
    'Buy Information — ',
    'Hire a Mercenary — ',
    'Hive Mind — ',
    'Horrific Symbiosis — ',
    'Loud Ruckus — ',
    'Mold Earth — ',
    'Probing Telepathy — ',
    'Project Image — ',
    'Sell Contraband — ',
    'Aim for the Wyvern — ',
    'Aim for the Cursed Amulet — ',
    'Calim Breath — ',
    'Fire a Warning Shot — ',
    'Gift of Tiamat — ',
    'Molting Exoskeleton — ',
    'Psionic Adept — ',
    'Rage Beyond Death — ',
    'Rejuvenation — ',
    'Wild Shape — ',
    'A Thousand Souls Die Every Day — ',
    'Advanced Species — ',
    'Aegis of the Emperor — ',
    'Allure of Slaanesh — ',
    'Arcane Life-support — ',
    'Architect of Deception — ',
    'Armor of Shrieking Souls — ',
    'Atomic Transmutation — ',
    'Battle Cannon — ',
    'Benediction of Omnissiah — ',
    'Berzerker — ',
    'The Betrayer — ',
    'Bio-plasmic Barrage — ',
    'Bio-Plasmic Scream — ',
    'Blade of Magnus — ',
    'Blood Chalice — ',
    'Bring it Down! — ',
    'Brood Telepathy — ',
    'Chainsword — ',
    'Chapter Master — ',
    'Children of the Cult — ',
    'Command Protocols — ',
    'Command Section — ',
    'Concealed Position — ',
    'Coruscating Flames — ',
    'Crushing Teeth — ',
    'Curse of the Walking Pox — ',
    'Daemon Sword — ',
    'Death Frenzy — ',
    'Devastating Charge — ',
    'Devourer of Souls — ',
    'Devouring Monster — ',
    'Drain Life — ',
    'Dynastic Advisor — ',
    'Dynastic Codes — ',
    'Dynastic Command Node — ',
    'Echo of the First Murder — ',
    'Elite Troops — ',
    'Endless Swarm — ',
    'Endurant — ',
    'Enmitic Exterminator — ',
    'Eternity Gate — ',
    'Executioner Round — ',
    'Exile Cannon — ',
    'Fabricator Claw Array — ',
    'Fallen Warrior — ',
    'Fast Healing — ',
    'Feeder Mandibles — ',
    'Field Reprogramming — ',
    'Fire of Tzeentch — ',
    'Flesh Flayer — ',
    'Flesh Hooks — ',
    'Frenzied Metabolism — ',
    'Frenzied Rampage — ',
    'Gatling Blaster — ',
    'Genestealer’s Kiss — ',
    'Genomic Enhancement — ',
    'Gift of Chaos — ',
    'Grand Strategist — ',
    'Grav-cannon — ',
    'Guardian Patrols — ',
    'Harbinger of Despair — ',
    'Healing Tears — ',
    'Heavy Power Hammer — ',
    'Heavy Rock Cutter — ',
    'Hunt for Heresy — ',
    'Hyperfang Round — ',
    'Hyperphase Threshers — ',
    'Hypertoxic Miasma — ',
    'Inquisition Agents — ',
    'Invasion Beams — ',
    'Jolly Gutpipes — ',
    'Leading from the Front — ',
    'Locus of Slaanesh — ',
    'Lord of Chaos — ',
    'Lord of the Pyrrhian Legions — ',
    'Lord of Torment — ',
    'Mark of the Chaos Ascendant — ',
    'Martyrdom — ',
    'Mage Hand — ',
    'Master of Machines — ',
    'Master Tactician — ',
    'Matter Absorption — ',
    'Medicus Ministorum — ',
    'Multi-threat Eliminator — ',
    'My Will Be Done — ',
    'Neurotraumal Rod — ',
    'Phaeron — ',
    'Phalanx Commander — ',
    'Pheromone Trail — ',
    'Plasma Incinerator — ',
    'Polymorphine — ',
    'Praesidium Protectiva — ',
    'Primarch of the Death Guard — ',
    'Prince of Chaos — ',
    'Prismatic Gallery — ',
    'Proclamator Hailer — ',
    'Protector — ',
    'Psychic Abomination — ',
    'Psychic Stimulus — ',
    'Rapacious Hunger — ',
    'Rapid Regeneration — ',
    'Rapid-fire Battle Cannon — ',
    'Relentless Mind — ',
    'Repair Barge — ',
    'Reverberating Summons — ',
    'Rites of Banishment — ',
    'Rogue Trader — ',
    'Rosarius — ',
    'Rot Fly — ',
    'Ruinous Ascension — ',
    'Sarcophagus — ',
    'Scavenge the Dead — ',
    'Secrets of the Soul — ',
    'The Seven-fold Chant — ',
    'Shieldwall — ',
    'Shrieking Gargoyles — ',
    'Sigil of Corruption — ',
    'Skilled Outrider — ',
    'Skyswarm — ',
    'Sonic Blaster — ',
    'Sorcerous Elixir — ',
    'Sorcerous Inspiration — ',
    'Spawn Termagants — ',
    'Sphere of the Void Dragon — ',
    'Spiritual Leader — ',
    'Split — ',
    'Spore Chimney — ',
    'Stowage — ',
    'Strategic Coordinator — ',
    'Strive — ',
    'Subterranean Assault — ',
    'Summary Execution — ',
    'Suppressing Fire — ',
    'Symphony of Pain — ',
    'Synapse Creature — ',
    'Synaptic Disintegrator — ',
    'Targeting Relay — ',
    'Terror from the Deep — ',
    'Three Autostubs — ',
    'Titanic — ',
    'Transdimensional Scout — ',
    'Translocation Protocols — ',
    'Ultima Founding — ',
    'Unearthly Power — ',
    'Unquestionable Wisdom — ',
    'Vanguard Species — ',
    'Veil of Time — ',
    'Void Shields — ',
    'Warp Blast — ',
    'The Will of the Hive Mind — ',
    'Warp Vortex — ',
    'Wraith Form — ',
    'Xenos Cunning — '
]

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
        self.text = re.sub(REPLACE_REMINDER_R, '', self.text)

        # START_TEXT_R = r'.+ — '
        # r = re.match(START_TEXT_R, self.text)
        # if not r:
        #     return
        # orig = self.text
        # self.text = self.text.replace(r.group(), '', 1)
        # g = r.group()
        # t = self.text
        # return
        for i in ABILITY_WORDS + FLAVOR_WORDS:
            self.text = self.text.replace(i, '')

class Cost(JSONObject):
    def __init__(self, s: str):
        self.options: list[list[CostPart]] = []
        # self.costs: list[CostPart] = []
        for option in s.split(' or '):
            costs = []
            for cs in option.split(', '):
                costs += [CostPart.parse(cs)]
            self.options += [costs]

    def to_json(self):
        result = []
        for option in self.options:
            a = []
            for cost in option:
                a += [cost.to_json()]
            result += [a]
        return result
        
class CostPart(JSONObject):
    def parse(s: str) -> 'Cost':
        if s == '{T}':
            return Tap()
        if s == '{Q}':
            return Untap()
        if s == '{E}':
            return Energy()
        m = re.findall(MANA_PIP_R, s)
        if m:
            return ManaPipGroup(m)
        result = CostPart()
        return result

class Energy(JSONObject):
    def to_json(self):
        return {'type': 'energy'}

class ManaPip(JSONObject):
    def __init__(self):
        self.lifeAltCost = -1
        self.alt: ManaPip = None
    
    def parse(s: str) -> 'ManaPip':
        if s == 'X':
            return XManaPip()
        if s == 'S':
            return SnowManaPip()
        if s == 'C':
            return ColorlessManaPip()
        if s in list(color.COLOR_PIP_MAP.values()):
            return ColoredManaPip(s)
        return GenericManaPip(s)

    def get_str(self):
        return ''

    def to_str(self):
        result = self.get_str()
        # print(dir(self))
        if self.alt:
            result += '/' + self.alt.get_str()
        return result

class SnowManaPip(ManaPip):
    def get_str(self):
        return 'S'

class ColorlessManaPip(ManaPip):
    def get_str(self):
        return 'C'

class XManaPip(ManaPip):
    def __init__(self):
        super().__init__()

    def get_str(self):
        return 'X'

class GenericManaPip(ManaPip):
    def __init__(self, s: str):
        super().__init__()
        self.value: int = int(s)

    def get_str(self):
        return str(self.value)

class ColoredManaPip(ManaPip):
    def __init__(self, s: str):
        super().__init__()
        self.color: str = s

    def get_str(self):
        return self.color

class ManaPipGroup(CostPart):
    def __init__(self, l: list[str]):
        self.pips: list[ManaPip] = []
        for le in l:
            self.pips += [ManaPip.parse(le[1:-1])]

    def to_json(self) -> dict:
        result = {"type": "mana_cost"}
        pips = []
        for pip in self.pips:
            pips += [pip.to_str()]
        result['pips'] = pips
        return result

class Tap(JSONObject):
    def to_json(self) -> dict:
        return {"type": "tap"}

class Untap(JSONObject):
    def to_json(self) -> dict:
        return {"type": "untap"}

class CardText(JSONObject):
    def __init__(self):
        self.orig_text = ''
        self.abilities: list = []

    def parse(text: str):
        result = CardText()
        result.orig_text = text
        lines = []
        for line in text.split('\n'):
            lines += [Line.parse(line)]
        for line in lines:
            line.extract_to(result)
        return result

# class Ability(JSONObject):
#     def __init__(self):
#         self.costs: list = []
#         self.effects: list = []
#         self.zones: list = []
#         self.isMana: bool = False

PARENTHESIS_R = r'(\"[^\"]+\")'
SUB_PARENTHESIS_R = r'(\'[^\']+\')'

def parenthesis_matching(l: 'Line'):
    found = re.findall(PARENTHESIS_R, l.text)
    if not found:
        found = re.findall(SUB_PARENTHESIS_R, l.text)
        if not found:
            return
    for f in found:
        key = f'%l{len(l.sublines)}%'
        l.text = l.text.replace(f, key, 1)
        line = f[1:-1]
        l.sublines += [Line.parse(line)]

def card_type_matching(line: str, acc: int=0) -> tuple[str, list]:
    m = re.search(CARD_TYPES_R, line)
    if not m:
        return line, []
    s = m.groups()[0] + 'card'
    ts = m.groups()[0][:-1].split(', ')
    result = []
    key = f'%{acc}%'
    result += [{
        'type': 'card_types',
        'types': ts
    }]
    res_line = line.replace(s, key, 1)
    res_line, n = card_type_matching(res_line, acc+1)
    if n:
        result += n
    return res_line, result

def card_type_matching(l: 'Line'):
    selected = 'card'
    generate_selectors(selected, CARD_TYPES, l)

MATCH_FUNCS = [
    parenthesis_matching,
    card_type_matching
]

class Line(JSONObject):
    def __init__(self):
        self.text = ''
        self.sublines: list[Line] = []
        self.selectors: list[Selector] = []

    def parse(line: str) -> 'Line':
        result = Line()
        result.text = line
        for f in MATCH_FUNCS:
            f(result)
        return result

    def extract_to(self, t: CardText):
        for r, f in EXTRACTOR_MAP.items():
            m = re.match(r, self.text)
            if not m: continue
            f(self, m)