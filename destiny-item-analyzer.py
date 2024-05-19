#!/usr/bin/env python3

import asyncio
import aiobungie
from configparser import ConfigParser
import html
import json
import os
import re
import requests
from collections import namedtuple
from datetime import datetime
from rich.console import Console


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

WeaponCatagory = namedtuple('WeaponCatagory', 'type owned_weapons url')
Weapon = namedtuple('Weapon', 'rank name')

weapon_catagories = [
    WeaponCatagory('Auto Rifle',          [], 'https://www.thegamer.com/destiny-2-best-auto-rifles-ranked/'),
    WeaponCatagory('Combat Bow',          [], 'https://www.thegamer.com/destiny-2-top-bows-ranked/'),
    WeaponCatagory('Fusion Rifle',        [], 'https://www.thegamer.com/destiny-2-top-best-fusion-rifles-ranked/'),
    WeaponCatagory('Glaive',              [], 'https://www.thegamer.com/destiny-2-glaive-ranked-best-worst/'),
    WeaponCatagory('Grenade Launcher',    [], 'https://www.thegamer.com/destiny-2-grenade-launchers-ranked/'),
    WeaponCatagory('Hand Cannon',         [], 'https://www.thegamer.com/destiny-2-best-hand-cannons-pve/'),
    WeaponCatagory('Linear Fusion Rifle', [], 'https://www.thegamer.com/destiny-2-linear-fusion-rifles-best-worst/'),
    WeaponCatagory('Machine Gun',         [], 'https://www.thegamer.com/destiny-2-best-machine-guns-ranked/'),
    WeaponCatagory('Pulse Rifle',         [], 'https://www.thegamer.com/destiny-2-best-pulse-rifles-ranked/'),
    WeaponCatagory('Rocket Launcher',     [], 'https://www.thegamer.com/destiny-2-top-best-rocket-launchers-ranked/'),
    WeaponCatagory('Scout Rifle',         [], 'https://www.thegamer.com/destiny-2-best-pve-scout-rifles-ranked/'),
    WeaponCatagory('Shotgun',             [], 'https://www.thegamer.com/destiny-2-best-pve-shotguns/'),
    WeaponCatagory('Sidearm',             [], 'https://www.thegamer.com/destiny-2-best-sidearms/'),
    WeaponCatagory('Sniper Rifle',        [], 'https://www.thegamer.com/destiny-2-best-pve-sniper-rifles-ranked/'),
    WeaponCatagory('Submachine Gun',      [], 'https://www.thegamer.com/destiny-2-best-pve-smgs-ranked/'),
    WeaponCatagory('Sword',               [], 'https://www.thegamer.com/destiny-2-top-swords-ranked/'),
    WeaponCatagory('Trace Rifle',         [], 'https://www.thegamer.com/destiny-2-trace-rifle-ranked-best-worst/'),
]
weapon_types = [weapon_catagory.type for weapon_catagory in weapon_catagories]

config = ConfigParser()
config.read('destiny-item-analyzer.ini')
API_KEY = config['DEFAULT']['ApiKey']
USERNAME = config['DEFAULT']['UserName']

client = aiobungie.Client(API_KEY)
console = Console(highlight=False)

http_headers = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}
weapon_name_pattern = r'<h2 id="(.*?)">\s?<span class="item-num">(.*?)\s?</span>\s?<span>(.*?)</span>\s?</h2>'


async def get_manifest():
    filename = 'destiny-item-analyzer'
    if not os.path.isfile(f'{filename}.json'):
        console.print(f'Downloading manifest to {filename}.json ...')
        await client.rest.download_json_manifest(file_name = filename)
    with open(f'{filename}.json', "r") as file:
        manifest = json.loads(file.read())
        return list(manifest["DestinyInventoryItemDefinition"].values())


async def get_profile(membership_id, membership_type):
    return await client.fetch_profile(
        membership_id,
        membership_type,
        components=[
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.PROFILE_INVENTORIES,
        ],
    )


async def get_equipment(membership_id, membership_type, character_id):
    character = await client.fetch_character(
        membership_id,
        membership_type,
        character_id,
        components=[
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.CHARACTER_EQUIPMENT,
        ],
    )
    character_class = str(character.character.class_type).title()
    console.print(f'Getting equipment for {character_class} ...')
    return character.equipment


def catagorize_equipment(equipment, manifest) -> None:
    for item in equipment:
        manifest_item = [
            manifest_item
            for manifest_item in manifest
            if manifest_item['hash'] == item.hash
        ][0]
        item_name = manifest_item['displayProperties']['name']
        item_type = manifest_item['itemTypeDisplayName']
        if item_type in weapon_types:
            weapon_catagories[weapon_types.index(item_type)].owned_weapons.append(item_name)


async def main():
    console.print('')
    console.print(f'[bold]Best weapons in Destiny 2 - TheGamer.com[/bold]')
    console.print(f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}')
    console.print('')

    async with client.rest:
        manifest = await get_manifest()

        console.print(f'Getting profile for {USERNAME} ...')
        for user in await client.search_users(USERNAME):
            for membership in user.memberships:
                profile = await get_profile(membership.id, membership.type)

                # Build lists of all of the weapons that the characters have equipped.
                for character_id in profile.characters:
                    equipment = await get_equipment(membership.id, membership.type, character_id)
                    catagorize_equipment(equipment, manifest)
                
                # Add to the lists all of the weapons in the vault.
                console.print(f'Getting equipment in the vault ...')
                catagorize_equipment(profile.profile_inventories, manifest)

    for weapon_catagory in weapon_catagories:
        console.print('')
        console.print(f'[bold]{weapon_catagory.type}[/bold]')
        console.print(f'[underline blue]{weapon_catagory.url}[/underline blue]')
        console.print('')

        response = requests.get(weapon_catagory.url, headers = http_headers)
        if response.status_code != 200:
            console.print(f'[red]Unsuccessful. status_code = {response.status_code}[/red]')
            console.print('')
            continue

        response_body = response.text.replace('\n', ' ').replace('\r', '')

        best_weapons = []
        for match in re.finditer(weapon_name_pattern, response_body):
            best_weapon_rank = int(match.group(2))
            best_weapon_name = html.unescape(match.group(3))
            best_weapons.append(Weapon(rank = best_weapon_rank, name = best_weapon_name))

        def sort_best_weapons_by_rank(best_weapon):
            return best_weapon.rank

        for best_weapon in sorted(best_weapons, key = sort_best_weapons_by_rank):
            best_weapon_name = best_weapon.name.strip()
            best_weapon_name_lowered = best_weapon_name.lower()

            owned_weapons = [owned_weapon.lower() for owned_weapon in weapon_catagory.owned_weapons]

            if best_weapon_name_lowered in owned_weapons:
                best_weapon_name = f'[underline]{best_weapon_name}[/underline]'
            if best_weapon_name_lowered in red_war_exotic_weapons:
                best_weapon_name = f'{best_weapon_name} ([yellow]Exotic Archive - Red War Exotics[/yellow])'
            if best_weapon_name_lowered in forsaken_exotic_weapons:
                best_weapon_name = f'{best_weapon_name} ([yellow]Exotic Archive - Forsaken Exotics[/yellow])'
            if best_weapon_name_lowered in shadowkeep_exotic_weapons:
                best_weapon_name = f'{best_weapon_name} ([yellow]Exotic Archive - Shadowkeep Exotics[/yellow])'
            if best_weapon_name_lowered in beyond_light_exotic_weapons:
                best_weapon_name = f'{best_weapon_name} ([yellow]Exotic Archive - Beyond Light Exotics[/yellow])'
            if best_weapon_name_lowered in the_witch_queen_exotic_weapons:
                best_weapon_name = f'{best_weapon_name} ([yellow]Exotic Archive - The Witch Queen Exotics[/yellow])'
            if best_weapon_name_lowered in lightfall_exotic_weapons:
                best_weapon_name = f'{best_weapon_name} ([yellow]Exotic Archive - Lightfall Exotics[/yellow])'
            if best_weapon_name_lowered in the_final_shape_exotic_weapons:
                best_weapon_name = f'{best_weapon_name} ([yellow]Exotic Archive - The Final Shape Exotics[/yellow])'
            if best_weapon_name_lowered in legacy_weapons:
                best_weapon_name = f'{best_weapon_name} ([purple]Exotic Archive - Legacy[/purple])'
            if best_weapon_name_lowered in legacy_crucible_weapons:
                best_weapon_name = f'{best_weapon_name} ([purple]Exotic Archive - Legacy Crucible[/purple])'
            if best_weapon_name_lowered in legacy_gambit_weapons:
                best_weapon_name = f'{best_weapon_name} ([purple]Exotic Archive - Legacy Gambit[/purple])'
            if best_weapon_name_lowered in legacy_vanguard_weapons:
                best_weapon_name = f'{best_weapon_name} ([purple]Exotic Archive - Legacy Vanguard[/purple])'
            if best_weapon_name_lowered in gunsmith_focused_decoding_suros_weapons:
                best_weapon_name = f'{best_weapon_name} ([purple]Gunsmith - Focused Decoding - Suros[/purple])'
            if best_weapon_name_lowered in gunsmith_focused_decoding_omolon_weapons:
                best_weapon_name = f'{best_weapon_name} ([purple]Gunsmith - Focused Decoding - Omolon[/purple])'
            if best_weapon_name_lowered in gunsmith_featured_weapons:
                best_weapon_name = f'{best_weapon_name} ([purple]Gunsmith - Featured[/purple])'
            if best_weapon_name_lowered in vanguard_weapons:
                best_weapon_name = f'{best_weapon_name} ([blue]Vanguard[/blue])'
            if best_weapon_name_lowered in drifter_weapons:
                best_weapon_name = f'{best_weapon_name} ([green]Drifter[/green])'

            console.print(f'{best_weapon.rank:02d} - {best_weapon_name}')

    console.print('')

if __name__ == '__main__':
    asyncio.run(main())
