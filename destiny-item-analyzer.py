#!/usr/bin/env python3

import asyncio
import aiobungie
from configparser import ConfigParser
import json
import os
from attr import dataclass
import requests
from bs4 import BeautifulSoup, Tag
from collections.abc import Sequence
from datetime import datetime
from rich.console import Console


@dataclass
class WeaponCategory:
    name: str
    url: str

WEAPON_CATEGORIES = [
    WeaponCategory('Auto Rifle',                'https://www.blueberries.gg/weapons/best-destiny-2-auto-rifles/'),
    WeaponCategory('Combat Bow',                'https://www.blueberries.gg/weapons/destiny-2-best-bows/'),
    WeaponCategory('Fusion Rifle',              'https://www.blueberries.gg/weapons/destiny-2-fusion-rifles/'),
    WeaponCategory('Glaive',                    'https://www.blueberries.gg/weapons/best-glaives-destiny-2/'),
    WeaponCategory('Breech Grenade Launcher',   'https://www.blueberries.gg/weapons/breech-grenade-launchers/'),
    WeaponCategory('Grenade Launcher',          'https://www.blueberries.gg/weapons/destiny-2-grenade-launchers/'),
    WeaponCategory('Hand Cannon',               'https://www.blueberries.gg/weapons/destiny-2-hand-cannons/'),
    WeaponCategory('Linear Fusion Rifle',       'https://www.blueberries.gg/weapons/linear-fusion-rifles/'),
    WeaponCategory('Machine Gun',               'https://www.blueberries.gg/weapons/destiny-2-machine-guns/'),
    WeaponCategory('Pulse Rifle',               'https://www.blueberries.gg/weapons/destiny-best-2-pulse-rifles/'),
    WeaponCategory('Rocket Launcher',           'https://www.blueberries.gg/weapons/destiny-2-rocket-launchers/'),
    WeaponCategory('Scout Rifle',               'https://www.blueberries.gg/weapons/destiny-2-scout-rifles/'),
    WeaponCategory('Shotgun',                   'https://www.blueberries.gg/weapons/destiny-2-best-shotguns/'),
    WeaponCategory('Sidearm',                   'https://www.blueberries.gg/weapons/destiny-2-best-sidearms/'),
    WeaponCategory('Sniper Rifle',              'https://www.blueberries.gg/weapons/destiny-2-snipers/'),
    WeaponCategory('Submachine Gun',            'https://www.blueberries.gg/weapons/destiny-2-smg/'),
    WeaponCategory('Sword',                     'https://www.blueberries.gg/weapons/best-destiny-2-swords/'),
    WeaponCategory('Trace Rifle',               'https://www.blueberries.gg/weapons/best-trace-rifles/'),
]
WEAPON_TYPES = [weapon_category.name for weapon_category in WEAPON_CATEGORIES]

HTTP_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        + 'Chrome/125.0.0.0 '
        + 'Safari/537.36',
}

async def get_manifest(
    console: Console,
    client: aiobungie.Client,
    downloaded_manifest_version: str
) -> list[dict]:
    online_manifest_version: str = await client.rest.fetch_manifest_version()

    filename: str = 'destiny-item-analyzer'
    manifest_is_downloaded: bool = os.path.isfile(f'{filename}.json')

    if not (manifest_is_downloaded and online_manifest_version == downloaded_manifest_version):
        if manifest_is_downloaded:
            console.print('Deleting outdated manifest file ...')
            os.remove(f'{filename}.json')

        console.print('Downloading new manifest file ...')
        await client.rest.download_json_manifest(file_name = filename)

        config: ConfigParser = ConfigParser()
        config.read('destiny-item-analyzer.ini')
        config['MANIFEST']['downloaded_version'] = online_manifest_version
        config.write(open('destiny-item-analyzer.ini', 'w'))

    with open(f'{filename}.json', "r") as file:
        manifest: dict = json.loads(file.read())
        return list(manifest["DestinyInventoryItemDefinition"].values())


async def get_profile(
        client: aiobungie.Client,
        membership: aiobungie.MembershipType
) -> aiobungie.crates.Component:
    return await client.fetch_profile(
        membership.id,
        membership.type,
        components=[
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.PROFILE_INVENTORIES,
        ],
    )


async def get_inventory(
    console: Console,
    client: aiobungie.Client,
    membership: aiobungie.MembershipType,
    character_id: int
) -> Sequence[aiobungie.crates.ProfileItemImpl]:
    character: aiobungie.crates.CharacterComponent = await client.fetch_character(
        membership.id,
        membership.type,
        character_id,
        components=[
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.CHARACTER_INVENTORY,
        ],
    )
    character_class: str = str(character.character.class_type)
    console.print(f'Getting inventory for {character_class.title()} ...')
    return character.inventory


async def get_equipment(
    console: Console,
    client: aiobungie.Client,
    membership: aiobungie.MembershipType,
    character_id: int
) -> Sequence[aiobungie.crates.ProfileItemImpl]:
    character: aiobungie.crates.CharacterComponent = await client.fetch_character(
        membership.id,
        membership.type,
        character_id,
        components=[
            aiobungie.ComponentType.CHARACTERS,
            aiobungie.ComponentType.CHARACTER_EQUIPMENT,
        ],
    )
    character_class: str = str(character.character.class_type)
    console.print(f'Getting equipment for {character_class.title()} ...')
    return character.equipment


def catagorize_equipment(
    console: Console,
    equipment: Sequence[aiobungie.crates.ProfileItemImpl],
    manifest: list[dict],
    owned_weapons: list[str]
) -> None:
    for item in equipment:
        manifest_items: list[dict] = [
            manifest_item
            for manifest_item in manifest
            if manifest_item['hash'] == item.hash
        ]
        if len(manifest_items) == 0:
            console.print(f'[yellow]Item not found in manifest: {item.hash}[/yellow]')
            continue

        manifest_item: dict = manifest_items[0]

        item_name: str = manifest_item['displayProperties']['name']
        if 'itemTypeDisplayName' not in manifest_item:
            continue
        item_type: str = manifest_item['itemTypeDisplayName']
        if item_type in WEAPON_TYPES:
            owned_weapons.append(item_name)


async def main():
    console: Console = Console(highlight=False)

    console.print('')
    console.print('[bold]Best weapons in Destiny 2 - Blueberries.gg[/bold]')
    console.print('')

    config: ConfigParser = ConfigParser()
    config.read('destiny-item-analyzer.ini')

    api_key: str = config['DEFAULT']['api_key']
    username: str = config['DEFAULT']['username']
    downloaded_manifest_version: str = config['MANIFEST']['downloaded_version']

    owned_weapons: list[str] = []

    client: aiobungie.Client = aiobungie.Client(api_key)
    async with client.rest:
        manifest: list[dict] = await get_manifest(console, client, downloaded_manifest_version)

        console.print(f'Getting profile for {username} ...')
        for user in await client.search_users(username):
            for membership in user.memberships:
                profile: aiobungie.crates.Component = await get_profile(client, membership)

                # Build lists of all of the weapons that the characters have equipped.
                for character_id in profile.characters:
                    inventory: Sequence[aiobungie.crates.ProfileItemImpl] = await get_inventory(
                        console,
                        client,
                        membership,
                        character_id
                    )
                    catagorize_equipment(console, inventory, manifest, owned_weapons)
                    equipment: Sequence[aiobungie.crates.ProfileItemImpl] = await get_equipment(
                        console,
                        client,
                        membership,
                        character_id
                    )
                    catagorize_equipment(console, equipment, manifest, owned_weapons)

                # Add to the lists all of the weapons in the vault.
                console.print('Getting equipment in the vault ...')
                catagorize_equipment(console, profile.profile_inventories, manifest, owned_weapons)

    for weapon_category in WEAPON_CATEGORIES:
        console.print('')
        console.print(f'[bold]{weapon_category.name}[/bold]')
        console.print(f'[underline blue]{weapon_category.url}[/underline blue]')
        console.print('')

        response: requests.Response = requests.get(weapon_category.url, headers = HTTP_HEADERS)
        if response.status_code != 200:
            console.print(f'[red]Unsuccessful. status_code = {response.status_code}[/red]')
            console.print('')
            continue

        soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')

        tier_table: Tag = soup.find('div', attrs={'class': 'tier-table'})
        weapon_cells: list[Tag] = tier_table.find_all('td', class_ = 'column-2')

        best_weapons: list[str] = []
        for weapon_cell in weapon_cells:
            anchor: Tag = weapon_cell.find('a')
            if anchor:
                anchor_text = anchor.get_text(strip=True)
                if anchor_text:
                    best_weapons.append(anchor_text)
                    continue

            cell_texts: list[str] = [
                weapon_cell_text.strip()
                for weapon_cell_text in weapon_cell.find_all(string=True, recursive=False)
                if weapon_cell_text.strip()
            ]
            if cell_texts:
                best_weapons.append(cell_texts[0])
            else:
                best_weapons.append('Unknown weapon')

        for best_weapon in best_weapons:
            if best_weapon == 'Unknown weapon':
                console.print(f'  [yellow]{best_weapon}[/yellow]')
                continue

            best_weapon_lowered: str = best_weapon.lower()
            owned_weapons_lowered: list[str] = [weapon.lower() for weapon in owned_weapons]
            if best_weapon_lowered in owned_weapons_lowered:
                console.print(f'[cyan]\u2022 {best_weapon}[/cyan]')
                continue

            console.print(f'  {best_weapon}')

    console.print('')


if __name__ == '__main__':
    asyncio.run(main())
