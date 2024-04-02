import html
import re
import requests
from collections import namedtuple
from datetime import datetime
from rich.console import Console


WeaponCatagory = namedtuple('WeaponCatagory', 'type url')
Weapon = namedtuple('Weapon', 'rank name')

weapon_catagories = [
    WeaponCatagory('Auto Rifles',           'https://www.thegamer.com/destiny-2-best-auto-rifles-ranked/'),
    WeaponCatagory('Bows',                  'https://www.thegamer.com/destiny-2-top-bows-ranked/'),
    WeaponCatagory('Fusion Rifles',         'https://www.thegamer.com/destiny-2-top-best-fusion-rifles-ranked/'),
    WeaponCatagory('Glaives',               'https://www.thegamer.com/destiny-2-glaive-ranked-best-worst/'),
    WeaponCatagory('Grenade Launchers',     'https://www.thegamer.com/destiny-2-grenade-launchers-ranked/'),
    WeaponCatagory('Hand Cannons',          'https://www.thegamer.com/destiny-2-best-hand-cannons-pve/'),
    WeaponCatagory('Linear Fusion Rifles',  'https://www.thegamer.com/destiny-2-linear-fusion-rifles-best-worst/'),
    WeaponCatagory('Machine Guns',          'https://www.thegamer.com/destiny-2-best-machine-guns-ranked/'),
    WeaponCatagory('Pulse Rifles',          'https://www.thegamer.com/destiny-2-best-pulse-rifles-ranked/'),
    WeaponCatagory('Rocket Launchers',      'https://www.thegamer.com/destiny-2-top-best-rocket-launchers-ranked/'),
    WeaponCatagory('Scout Rifles',          'https://www.thegamer.com/destiny-2-best-pve-scout-rifles-ranked/'),
    WeaponCatagory('Shotguns',              'https://www.thegamer.com/destiny-2-best-pvp-shotguns/'),
    WeaponCatagory('Sidearms',              'https://www.thegamer.com/destiny-2-best-sidearms/'),
    WeaponCatagory('Sniper Rifles',         'https://www.thegamer.com/destiny-2-best-pve-sniper-rifles-ranked/'),
    WeaponCatagory('Submachine Guns',       'https://www.thegamer.com/destiny-2-best-pve-smgs-ranked/'),
    WeaponCatagory('Swords',                'https://www.thegamer.com/destiny-2-top-swords-ranked/'),
    WeaponCatagory('Trace Rifles',          'https://www.thegamer.com/destiny-2-trace-rifle-ranked-best-worst/'),
]

owned_auto_rifles = [
    'centrifuse',
    'coronach-22',
    'hard light',
    'monte carlo',
    'old sterling',
    'quicksilver storm',
    'ros arago iv'
]

owned_combat_bows = [
    'le monarque',
    "leviathan's breath",
    'lunulata-4b',
    'pre astyanax iv',
    'trinity ghoul',
    'verglas curve',
]

owned_fusion_rifles = [
    'jötunn',
    'likely suspect',
    'merciless',
    'nox perennial v',
    'snorri fr5',
    'telesto',
    'tesselation',
]

owned_glaives = [
    'ecliptic distaff',
    'judgment of kelgorath',
    'the enigma',
]

owned_grenade_launchers = [
    'ex diris',
    'fighting lion',
    'hullabaloo',
    'parasite',
    "salvager's salvo",
    "salvation's grip",
    'the colony',
    'wild style',
    'witherhoard',
]

owned_hand_cannons = [
    'ace of spades',
    'austringer',
    'combined action',
    'crisis inverted',
    'pure poetry',
    'sunshot',
    'targeted redaction',
]

owned_linear_fusion_rifles = [
    'arbalest',
    'lorentz driver',
    'taipan-4fr',
    'the queenbreaker',
]

owned_machine_guns = [
    'heir apparent',
    'marcato-45',
    'recurrent impact',
    'thunderlord',
]

owned_pulse_rifles = [
    'graviton lance',
    'no time to explain',
    'Syncopation-53',
    'vigilance wing',
]

owned_rocket_launchers = [
    'crux termination iv',
    'deathbringer',
    "dragon's breath",
    'heretic',
    'the hothead',
    'the wardcliff coil',
    'two-tailed fox',
]

owned_scout_rifles = [
    "dead man's tale",
    'glissando-47',
    'jararaca-3sr',
    'night watch',
    'perses-d',
    'pleiades corrector',
    'pointed inquiry',
    'polaris lance',
    "skyburner's oath",
    'taraxippos',
]

owned_shotguns = [
    'dead weight',
    'duality',
    'hand in hand',
    'ragnhild-d',
    'retrofuturist',
    'the chaperone',
    'tractor cannon',
]

owned_sidearms = [
    'boudica-c',
    'empirical evidence',
    'senuna si6',
    "traveler's chosen",
    'trespasser',
]

owned_sniper_rifles = [
    'adored',
    'borealis',
    'd.a.r.c.i.',
    'fugue-55',
    "izanagi's burden",
    'last foray',
    'luna regolith iii',
    'the supremacy',
    'whisper of the worm',
]

owned_submachine_guns = [
    'borrowed time',
    'forensic nightmare',
    'osteo striga',
    'parabellum',
    'pizzicato-22',
    'riskrunner',
    'the huckleberry',
    'the title',
]

owned_swords = [
    'black talon',
    'chivalric fire',
    'double-edged answer',
    'geodetic hsm',
    'nasreddin',
    'the lament',
]

owned_trace_rifles = [
    'appetence',
    'coldheart',
    'prometheus lens',
    'wavesplitter',
]

owned_weapons = (
    owned_auto_rifles +
    owned_combat_bows +
    owned_fusion_rifles +
    owned_glaives +
    owned_grenade_launchers +
    owned_hand_cannons +
    owned_linear_fusion_rifles +
    owned_machine_guns +
    owned_pulse_rifles +
    owned_rocket_launchers +
    owned_scout_rifles +
    owned_shotguns +
    owned_sidearms +
    owned_sniper_rifles +
    owned_submachine_guns +
    owned_swords +
    owned_trace_rifles
)

red_war_exotic_weapons = [
    'legend of acrius',
    'mida multi-tool',
    'outbreak perfected',
    'polaris lance',
    'rat king',
    'sleeper stimulant',
    'sturm',
    'whisper of the worm',
    'worldline zero',
]

forsaken_exotic_weapons = [
    'ace of spades',
    'always on time',
    'anarchy',
    'bad juju',
    "izanagi's burden",
    'jötunn',
    'le monarque',
    'lumina',
    'tarrabah',
    'the last word',
    'thorn',
    'truth',
]

shadowkeep_exotic_weapons = [
    "ariana's vow",
    'bastion',
    "devil's ruin",
    "leviathan's breath",
    'ruinous effigy',
    'symmetry',
    'the fourth horseman',
    "tommy's matchbook",
    "traveler's chosen",
    'witherhoard',
]

beyond_light_exotic_weapons = [
    "ager's scepter",
    'cryosthesia 77k',
    'duality',
    'lorentz driver',
    "ticuu's divination",
]

the_witch_queen_exotic_weapons = [
    'delicate tomb',
    'grand overture',
    'the maticore',
    'trespasser',
]

lightfall_exotic_weapons = [
    'centrifuse',
    'ex diris',
    'quicksilver storm',
    'verglas curve',
]

the_final_shape_exotic_weapons = [
    'tessellation',
]

legacy_weapons = [
    'adored',
    'ascendancy',
    'chain of command',
    'cry mutiny',
    'ecliptic distaff',
    "felwinter's lie",
    'last rite',
    'malediction',
    'null composure',
    'reckless endangerment',
    "salvager's salvo",
    'veles-x',
]

legacy_crucible_weapons = [
    'komodo-4fr',
    "luna's howl",
    'not forgotten',
    "redrix's broadsword",
    'revoker',
    'the mountaintop',
    'the recluse',
]

legacy_gambit_weapons = [
    '21% delirium',
    'exit strategy',
    'hush',
    'python',
]

legacy_vanguard_weapons = [
    'edgewise',
    'oxygen sr3',
]

gunsmith_focused_decoding_suros_weapons = [
    'cantata-57',
    'fioritura-59',
    'fugue-55',
    'pizzicato-22',
    'staccato-46',
    'syncopation-53',
]

gunsmith_focused_decoding_omolon_weapons = [
    'ammit ar2',
    'aurvandil fr6',
    'gallu rr3',
    'ogma pr6',
    'snorri fr5',
    'typhon gl5',
]

gunsmith_featured_weapons = [
    'whispering slab',
    "timelines' vertex",
    'austringer',
    'piece of mind',
    'palmyra-b',
]

vanguard_weapons = [
    'braytech osprey',
    'buzzard',
    'd.f.a.',
    'double-edged answer',
    'duty bound',
    'empty vessel',
    'fortissimo-11',
    "horror's least",
    'hung jury sr4',
    'loaded question',
    'luna regolith iii',
    'main ingrediant',
    "mindbender's ambition",
    'nameless midnight',
    'outrageous fortune',
    'plug one.1',
    'positive outlook',
    'pre astyanax iv',
    'prolonged engagement',
    'punching out',
    'pure poetry',
    'royal entry',
    'silicon neuroma',
    'strident whistle',
    'the comedian',
    'the hothead',
    'the last dance',
    "the militia's birthright",
    'the slammer',
    'the swarm',
    'the third axiom',
    'undercurrent',
    'uzume rr4',
    "warden's law",
    'wild style (adept)',
    'wild style',
    'windigo gl3',
    'xenoclast iv',
]

drifter_weapons = [
    'albruna-d',
    'bad omens',
    'borrowed time',
    'bottom dollar',
    'breakneck',
    'crowd pleaser',
    'dead weight',
    'gnawing hunger',
    'herod-c',
    'laser painter',
    'night watch',
    'qua xaphan v',
    'servant leader',
    'trinary system',
    'trust',
    'yesteryear',
]

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
headers = {
    "user-agent": user_agent,
}

console = Console(highlight=False)

console.print(f'[bold]Best weapons in Destiny 2 - TheGamer.com[/bold]')
console.print(f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}')
console.print('')

for weapon_catagory in weapon_catagories:
    console.print(f'[bold]{weapon_catagory.type}[/bold]')
    console.print(f'[underline blue]{weapon_catagory.url}[/underline blue]')

    response = requests.get(weapon_catagory.url, headers = headers)
    if response.status_code != 200:
        console.print(f'[red]Unsuccessful. status_code = {response.status_code}[/red]')
        console.print('')
        continue

    response_body = response.text.replace('\n', ' ').replace('\r', '')

    pattern = r'<h2 id="(.*?)">\s?<span class="item-num">(.*?)\s?</span>\s?<span>(.*?)</span>\s?</h2>'

    weapons = []
    for match in re.finditer(pattern, response_body):
        weapon_rank = int(match.group(2))
        weapon_name = html.unescape(match.group(3))
        weapons.append(Weapon(rank = weapon_rank, name = weapon_name))

    def sort_weapons_by_rank(weapon):
        return weapon.rank

    weapons = sorted(weapons, key = sort_weapons_by_rank)

    for weapon in weapons:
        weapon_text = f'{weapon.name}'
        if weapon.name.lower() in owned_weapons:
            weapon_text = f'[underline]{weapon_text}[/underline]'
        if weapon.name.lower() in red_war_exotic_weapons:
            weapon_text = f'{weapon_text} ([yellow]Exotic Archive - Red War Exotics[/yellow])'
        if weapon.name.lower() in forsaken_exotic_weapons:
            weapon_text = f'{weapon_text} ([yellow]Exotic Archive - Forsaken Exotics[/yellow])'
        if weapon.name.lower() in shadowkeep_exotic_weapons:
            weapon_text = f'{weapon_text} ([yellow]Exotic Archive - Shadowkeep Exotics[/yellow])'
        if weapon.name.lower() in beyond_light_exotic_weapons:
            weapon_text = f'{weapon_text} ([yellow]Exotic Archive - Betond Light Exotics[/yellow])'
        if weapon.name.lower() in the_witch_queen_exotic_weapons:
            weapon_text = f'{weapon_text} ([yellow]Exotic Archive - The Witch Queen Exotics[/yellow])'
        if weapon.name.lower() in lightfall_exotic_weapons:
            weapon_text = f'{weapon_text} ([yellow]Exotic Archive - Lightfall Exotics[/yellow])'
        if weapon.name.lower() in the_final_shape_exotic_weapons:
            weapon_text = f'{weapon_text} ([yellow]Exotic Archive - The Final Shape Exotics[/yellow])'
        if weapon.name.lower() in legacy_weapons:
            weapon_text = f'{weapon_text} ([purple]Exotic Archive - Legacy[/purple])'
        if weapon.name.lower() in legacy_crucible_weapons:
            weapon_text = f'{weapon_text} ([purple]Exotic Archive - Legacy Crucible[/purple])'
        if weapon.name.lower() in legacy_gambit_weapons:
            weapon_text = f'{weapon_text} ([purple]Exotic Archive - Legacy Gambit[/purple])'
        if weapon.name.lower() in legacy_vanguard_weapons:
            weapon_text = f'{weapon_text} ([purple]Exotic Archive - Legacy Vanguard[/purple])'
        if weapon.name.lower() in gunsmith_focused_decoding_suros_weapons:
            weapon_text = f'{weapon_text} ([purple]Gunsmith - Focused Decoding - Suros[/purple])'
        if weapon.name.lower() in gunsmith_focused_decoding_omolon_weapons:
            weapon_text = f'{weapon_text} ([purple]Gunsmith - Focused Decoding - Omolon[/purple])'
        if weapon.name.lower() in gunsmith_featured_weapons:
            weapon_text = f'{weapon_text} ([purple]Gunsmith - Featured[/purple])'
        if weapon.name.lower() in vanguard_weapons:
            weapon_text = f'{weapon_text} ([blue]Vanguard[/blue])'
        if weapon.name.lower() in drifter_weapons:
            weapon_text = f'{weapon_text} ([green]Drifter[/green])'
        console.print(f'{weapon.rank:02d} - {weapon_text}')

    console.print('')

exit(0)
