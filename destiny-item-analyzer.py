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


RED_WAR_EXOTIC_WEAPONS = [
    'legend of acrius',
    'mida multi-tool',
    'polaris lance',
    'rat king',
    'sleeper stimulant',
    'sturm',
    'worldline zero',
]

FORSAKEN_EXOTIC_WEAPONS = [
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

SHADOWKEEP_EXOTIC_WEAPONS = [
    'bastion',
    "devil's ruin",
    "eriana's vow",
    "leviathan's breath",
    'ruinous effigy',
    'symmetry',
    'the fourth horseman',
    "tommy's matchbook",
    "traveler's chosen",
    'witherhoard',
]

BEYOND_LIGHT_EXOTIC_WEAPONS = [
    "ager's scepter",
    'cryosthesia 77k',
    'duality',
    'lorentz driver',
    "ticuu's divination",
]

THE_WITCH_QUEEN_EXOTIC_WEAPONS = [
    'delicate tomb',
    'grand overture',
    'the maticore',
    'trespasser',
]

LIGHTFALL_EXOTIC_WEAPONS = [
    'centrifuse',
    "dragon's breath",
    'ex diris',
    'quicksilver storm',
    'verglas curve',
    'wicked implement',
]

THE_FINAL_SHAPE_EXOTIC_WEAPONS = [
    'tessellation',
]

LEGACY_WEAPONS = [
    'adored',
    'ascendancy',
    'chain of command',
    'chivalric fire',
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

LEGACY_CRUCIBLE_WEAPONS = [
    'komodo-4fr',
    "luna's howl",
    'not forgotten',
    "redrix's broadsword",
    'revoker',
    'the mountaintop',
    'the recluse',
]

LEGACY_GAMBIT_WEAPONS = [
    '21% delirium',
    'exit strategy',
    'python',
]

LEGACY_VANGUARD_WEAPONS = [
    'edgewise',
    'oxygen sr3',
]

GUNSMITH_FOCUSED_DECODING_SUROS_WEAPONS = [
    'cantata-57',
    'coronach-22',
    'fioritura-59',
    'fugue-55',
    'pizzicato-22',
    'staccato-46',
    'syncopation-53',
]

GUNSMITH_FOCUSED_DECODING_FIELD_FORGED_WEAPONS = [
    'battle scar',
    'hand in hand',
    'harsh language',
    'nasreddin',
]

GUNSMITH_FEATURED_WEAPONS = [
    'chrysura melo',
    'true prophecy',
    'seventh seraph si-2',
    'far future',
    "tempation's hook",
]

VANGUARD_FOCUSED_DECODING_WEAPONS = [
    'double-edged answer',
    'luna regolith iii',
    'nameless midnight',
    'origin story',
    'positive outlook',
    'prolonged engagement',
]

VANGUARD_FOCUSED_DECODING_NIGHTFALL_WEAPONS = [
    'pre astyanax iv',
    'scintillation',
    'shadow price',
    'the slammer',
    'undercurrent',
    'uzume rr4',
    "warden's law",
    "warden's law (adept)",
    'wild style',
]

VANGUARD_FOCUSED_DECODING_LEGACY_VANGUARD_OPS_WEAPONS = [
    'empty vessel',
    'fortissimo-11',
    'main ingrediant',
    'outrageous fortune',
    'punching out',
    'pure poetry',
    'royal entry',
    'strident whistle',
    'the last dance',
    'the third axiom',
    'xenoclast iv',
]

VANGUARD_FOCUSED_DECODING_LEGACY_NIGHTFALL_WEAPONS = [
    'braytech osprey',
    'buzzard',
    'd.f.a.',
    'duty bound',
    "horror's least",
    'hung jury sr4',
    'loaded question',
    "mindbender's ambition",
    'plug one.1',
    'silicon neuroma',
    'the comedian',
    'the hothead',
    "the militia's birthright",
    'the swarm',
    'wendigo gl3',
]

DRIFTER_FOCUSED_DECODING_WEAPONS = [
    'albruna-d',
    'breakneck',
    'hush',
    'laser painter',
    'qua xaphan v',
    'trust',
]

DRIFTER_FOCUSED_DECODING_LEGACY_WEAPONS = [
    'bad omens',
    'borrowed time',
    'bottom dollar',
    'crowd pleaser',
    'dead weight',
    'herod-c',
    'gnawing hunger',
    'night watch',
    'servant leader',
    'trinary system',
    'yesteryear',
]

WeaponCatagory = namedtuple('WeaponCatagory', 'type url')
Weapon = namedtuple('Weapon', 'rank name')

WEAPON_CATAGORIES = [
    WeaponCatagory('Auto Rifle',          'https://www.thegamer.com/destiny-2-best-auto-rifles-ranked/'),
    WeaponCatagory('Combat Bow',          'https://www.thegamer.com/destiny-2-top-bows-ranked/'),
    WeaponCatagory('Fusion Rifle',        'https://www.thegamer.com/destiny-2-top-best-fusion-rifles-ranked/'),
    WeaponCatagory('Glaive',              'https://www.thegamer.com/destiny-2-glaive-ranked-best-worst/'),
    WeaponCatagory('Grenade Launcher',    'https://www.thegamer.com/destiny-2-grenade-launchers-ranked/'),
    WeaponCatagory('Hand Cannon',         'https://www.thegamer.com/destiny-2-best-hand-cannons-pve/'),
    WeaponCatagory('Linear Fusion Rifle', 'https://www.thegamer.com/destiny-2-linear-fusion-rifles-best-worst/'),
    WeaponCatagory('Machine Gun',         'https://www.thegamer.com/destiny-2-best-machine-guns-ranked/'),
    WeaponCatagory('Pulse Rifle',         'https://www.thegamer.com/destiny-2-best-pulse-rifles-ranked/'),
    WeaponCatagory('Rocket Launcher',     'https://www.thegamer.com/destiny-2-top-best-rocket-launchers-ranked/'),
    WeaponCatagory('Scout Rifle',         'https://www.thegamer.com/destiny-2-best-pve-scout-rifles-ranked/'),
    WeaponCatagory('Shotgun',             'https://www.thegamer.com/destiny-2-best-pve-shotguns/'),
    WeaponCatagory('Sidearm',             'https://www.thegamer.com/destiny-2-best-sidearms/'),
    WeaponCatagory('Sniper Rifle',        'https://www.thegamer.com/destiny-2-best-pve-sniper-rifles-ranked/'),
    WeaponCatagory('Submachine Gun',      'https://www.thegamer.com/destiny-2-best-pve-smgs-ranked/'),
    WeaponCatagory('Sword',               'https://www.thegamer.com/destiny-2-top-swords-ranked/'),
    WeaponCatagory('Trace Rifle',         'https://www.thegamer.com/destiny-2-trace-rifle-ranked-best-worst/'),
]
WEAPON_TYPES = [weapon_catagory.type for weapon_catagory in WEAPON_CATAGORIES]

HTTP_HEADERS = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/125.0.0.0 ' +
        'Safari/537.36',
}
WEAPON_NAME_PATTERN = r'<h2 id="(.*?)">\s?<span class="item-num">(.*?)\s?</span>\s?<span>(.*?)</span>\s?</h2>'


async def get_manifest(console, client, downloaded_manifest_version):
    online_manifest_version = await client.rest.fetch_manifest_version()

    filename = 'destiny-item-analyzer'
    manifest_is_downloaded = os.path.isfile(f'{filename}.json')

    if not (manifest_is_downloaded and online_manifest_version == downloaded_manifest_version):
        if manifest_is_downloaded:
            console.print(f'Deleting outdated manifest file ...')
            os.remove(f'{filename}.json')

        console.print(f'Downloading new manifest file ...')
        await client.rest.download_json_manifest(file_name = filename)

        config = ConfigParser()
        config.read('destiny-item-analyzer.ini')
        config['MANIFEST']['downloaded_version'] = online_manifest_version
        config.write(open('destiny-item-analyzer.ini', 'w'))

    with open(f'{filename}.json', "r") as file:
        manifest = json.loads(file.read())
        return list(manifest["DestinyInventoryItemDefinition"].values())


async def get_profile(client, membership_id, membership_type):
    return await client.fetch_profile(
        membership_id,
        membership_type,
        components=[
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.PROFILE_INVENTORIES,
        ],
    )


async def get_inventory(console, client, membership_id, membership_type, character_id):
    character = await client.fetch_character(
        membership_id,
        membership_type,
        character_id,
        components=[
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.CHARACTER_INVENTORY,
        ],
    )
    character_class = str(character.character.class_type).title()
    console.print(f'Getting inventory for {character_class} ...')
    return character.inventory


async def get_equipment(console, client, membership_id, membership_type, character_id):
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


def catagorize_equipment(console, equipment, manifest, owned_weapons) -> None:
    for item in equipment:
        manifest_items = [
            manifest_item
            for manifest_item in manifest
            if manifest_item['hash'] == item.hash
        ]
        if len(manifest_items) == 0:
            console.print(f'[yellow]Item not found in manifest: {item.hash}[/yellow]')
            continue

        manifest_item = manifest_items[0]

        item_name = manifest_item['displayProperties']['name']
        if 'itemTypeDisplayName' not in manifest_item:
            continue
        item_type = manifest_item['itemTypeDisplayName']
        if item_type in WEAPON_TYPES:
            owned_weapons[item_type].append(item_name)


async def main():
    console = Console(highlight=False)

    console.print('')
    console.print(f'[bold]Best weapons in Destiny 2 - TheGamer.com[/bold]')
    console.print('')

    config = ConfigParser()
    config.read('destiny-item-analyzer.ini')

    api_key = config['DEFAULT']['api_key']
    username = config['DEFAULT']['username']
    downloaded_manifest_version = config['MANIFEST']['downloaded_version']

    owned_weapons = {weapon_type: [] for weapon_type in WEAPON_TYPES}

    client = aiobungie.Client(api_key)
    async with client.rest:
        manifest = await get_manifest(console, client, downloaded_manifest_version)

        console.print(f'Getting profile for {username} ...')
        for user in await client.search_users(username):
            for membership in user.memberships:
                profile = await get_profile(client, membership.id, membership.type)

                # Build lists of all of the weapons that the characters have equipped.
                for character_id in profile.characters:
                    inventory = await get_inventory(console, client, membership.id, membership.type, character_id)
                    catagorize_equipment(console, inventory, manifest, owned_weapons)
                    equipment = await get_equipment(console, client, membership.id, membership.type, character_id)
                    catagorize_equipment(console, equipment, manifest, owned_weapons)
                
                # Add to the lists all of the weapons in the vault.
                console.print(f'Getting equipment in the vault ...')
                catagorize_equipment(console, profile.profile_inventories, manifest, owned_weapons)

    for weapon_catagory in WEAPON_CATAGORIES:
        console.print('')
        console.print(f'[bold]{weapon_catagory.type}[/bold]')
        console.print(f'[underline blue]{weapon_catagory.url}[/underline blue]')
        console.print('')

        response = requests.get(weapon_catagory.url, headers = HTTP_HEADERS)
        if response.status_code != 200:
            console.print(f'[red]Unsuccessful. status_code = {response.status_code}[/red]')
            console.print('')
            continue

        response_body = response.text.replace('\n', ' ').replace('\r', '')

        best_weapons = []
        for match in re.finditer(WEAPON_NAME_PATTERN, response_body):
            best_weapon_rank = int(match.group(2))
            best_weapon_name = html.unescape(match.group(3))
            best_weapons.append(Weapon(rank = best_weapon_rank, name = best_weapon_name))

        def sort_best_weapons_by_rank(best_weapon):
            return best_weapon.rank

        for best_weapon in sorted(best_weapons, key = sort_best_weapons_by_rank):
            best_weapon_name = best_weapon.name.strip()
            best_weapon_name_lowered = best_weapon_name.lower()

            owned_weapons_of_this_type_lowered = [weapon.lower() for weapon in owned_weapons[weapon_catagory.type]]

            if best_weapon_name_lowered in owned_weapons_of_this_type_lowered:
                best_weapon_name = f'[underline]{best_weapon_name}[/underline]'

            if best_weapon_name_lowered in RED_WAR_EXOTIC_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Red War Exotics)'
            if best_weapon_name_lowered in FORSAKEN_EXOTIC_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Forsaken Exotics)'
            if best_weapon_name_lowered in SHADOWKEEP_EXOTIC_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Shadowkeep Exotics)'
            if best_weapon_name_lowered in BEYOND_LIGHT_EXOTIC_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Beyond Light Exotics)'
            if best_weapon_name_lowered in THE_WITCH_QUEEN_EXOTIC_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - The Witch Queen Exotics)'
            if best_weapon_name_lowered in LIGHTFALL_EXOTIC_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Lightfall Exotics)'
            if best_weapon_name_lowered in THE_FINAL_SHAPE_EXOTIC_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - The Final Shape Exotics)'
            if best_weapon_name_lowered in LEGACY_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Legacy)'
            if best_weapon_name_lowered in LEGACY_CRUCIBLE_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Legacy Crucible)'
            if best_weapon_name_lowered in LEGACY_GAMBIT_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Legacy Gambit)'
            if best_weapon_name_lowered in LEGACY_VANGUARD_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Exotic Archive - Legacy Vanguard)'

            if best_weapon_name_lowered in GUNSMITH_FOCUSED_DECODING_SUROS_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Gunsmith - Focused Decoding - Suros)'
            if best_weapon_name_lowered in GUNSMITH_FOCUSED_DECODING_FIELD_FORGED_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Gunsmith - Focused Decoding - Field-Forged)'
            if best_weapon_name_lowered in GUNSMITH_FEATURED_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Gunsmith - Featured)'

            if best_weapon_name_lowered in VANGUARD_FOCUSED_DECODING_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Vanguard - Focused Decoding)'
            if best_weapon_name_lowered in VANGUARD_FOCUSED_DECODING_NIGHTFALL_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Vanguard - Focused Decoding - Nightfall)'
            if best_weapon_name_lowered in VANGUARD_FOCUSED_DECODING_LEGACY_VANGUARD_OPS_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Vanguard - Focused Decoding - Legacy Vanguard Ops)'
            if best_weapon_name_lowered in VANGUARD_FOCUSED_DECODING_LEGACY_NIGHTFALL_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Vanguard - Focused Decoding - Legacy Nightfall)'

            if best_weapon_name_lowered in DRIFTER_FOCUSED_DECODING_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Drifter - Focused Decoding)'
            if best_weapon_name_lowered in DRIFTER_FOCUSED_DECODING_LEGACY_WEAPONS:
                best_weapon_name = f'{best_weapon_name} (Drifter - Focused Decoding - Legacy)'

            console.print(f'{best_weapon.rank:02d} - {best_weapon_name}')

    console.print('')


if __name__ == '__main__':
    asyncio.run(main())
