"""
Some simple examples of the public endpoints available for examining users, 
characters, and clans using the Destiny API.

You will need to put in your own api key to run it. To learn how go to:
    http://destinydevs.github.io/BungieNetPlatform/docs/API-Key
"""
import requests
import json


#dictionary to hold extra headers
# HEADERS = {'X-API-Key':'22f201d0d1864a4d8d5a7ccc79be8a33'}

#make request for Gjallarhorn
# r = requests.get("https://www.bungie.net/platform/Destiny/Manifest/InventoryItem/1274330687/", headers=HEADERS);

#convert the json object we received into a Python dictionary object
#and print the name of the item
# inventoryItem = r.json()
# print(inventoryItem['Response']['data']['inventoryItem']['itemName'])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# def user_id_from_name(user_name, user_platform, my_api_key):
#     """Wrapper for GetMembershipIdByDisplayName endpoint. 
#     Given username, returns ID number, or 0 if not found
#     For Destiny 2, will need to be extended to PC."""

#     url = 'https://bungie.net/Platform/User/GetMembershipIds/'
#     headers = {"X-API-Key": my_api_key}
#     response = requests.get(url, headers = headers).json()
#     print(f'response = {response}')
#     exit(0)

#     if response.status_code == 200:  
#         print(f'request = {response["Response"]}')
#     else:
#         print(f'user_id_from_name() unsuccessful. status_code = {response.status_code}')
#     exit(0)


#     membership_type = membership_type_from_platform(user_platform)
#     id_request_url = 'https://bungie.net/Platform/Destiny2/SearchDestinyPlayerByBungieName/' + membership_type + '/'
#     my_headers = {"X-API-Key": my_api_key}
#     post_body = {'displayName': user_name, 'displayNameCode': 0}
#     id_request = requests.post(id_request_url, headers = my_headers, json = post_body)
#     if id_request.status_code == 200:  
#         return id_request.json()['Response']
#     else:
#         print("user_id_from_name() unsuccessful for " + user_name)
#         return None

# def info_from_id(user_id, my_api_key):
#     """Wrapper for GetAccountSummary endpoint.
#     Given the user id, return list of their characters, and print basic information
#     about their characters. Also saves this information as a text file (member_data.txt)"""
#     membership_type = membership_type_from_platform(user_platform)
#     summary_request_url = 'https://bungie.net/Platform/Destiny/' + membership_type + '/Account/' + \
#                           user_id + '/Summary/'                 
#     my_headers = {"X-API-Key": my_api_key}        
#     summary_request = requests.get(summary_request_url, headers = my_headers)
#     if summary_request.status_code == 200:
#         member_data = summary_request.json()['Response']['data']
#         #Save to file with nice formatting (comment out if you dont' want to save)
#         with open('member_data.txt', 'w') as fileObject:
#             fileObject.write(json.dumps(member_data, indent = 3))
#             print("User's data saved to member_data.txt")
#         print_user_info(member_data)
#         return member_data
#     else:
#         print("info_from_id() unsuccessful for " + user_id)
#         return None

# def get_clan_info(user_id, user_platform, my_api_key):
#     """Wrapper for GetBungieAccount. Returns account information for user, 
#     such as username, clan identification, etc."""
#     membership_type = membership_type_from_platform(user_platform)
#     get_account_url = 'https://bungie.net/Platform/User/GetBungieAccount/' + user_id + \
#                         '/' + membership_type + '/'
#     my_headers = {"X-API-Key": my_api_key}   
#     account_request = requests.get(get_account_url, headers = my_headers)
#     if account_request.status_code == 200:
#         user_bungie_account = account_request.json()['Response']
#         if user_bungie_account['clans']:
#             clan_id = user_bungie_account['clans'][0]['groupId']
#             clan_name = user_bungie_account['relatedGroups'][clan_id]['name'] 
#         else:
#             clan_name = None
#             clan_id = None
#         return user_bungie_account, clan_name, clan_id


# def get_clan_member_data(clan_id, my_api_key):
#     """Wrapper for MembersV3. Given clan id (the group ID number), 
#     returns all members of the clan. This is very much not finished.
#     There are lots of options that I have not finished that would need
#     to be worked on to get this in final working order. For instance, this
#     is only returning the first page of results"""
#     get_clan_url = 'https://bungie.net/Platform/Group/' + clan_id + '/MembersV3/?currentPage=1'
#     my_headers = {"X-API-Key": my_api_key}   
#     clan_request = requests.get(get_clan_url, headers = my_headers)
#     if clan_request.status_code == 200:    
#         clan_data = clan_request.json()['Response']
#         return clan_data

# def membership_type_from_platform(platform):
#     """Most api calls require information about platform.
#     Convention is ps4->2, and xbox one ->1. When D2 comes
#     out will need to put in pc case!"""
#     if platform == 'pc':
#         return '3'
#     elif platform == 'ps4':
#         return '2'
#     elif platform == 'xbone':
#         return '1'
#     else: 
#         return None

# def print_user_info(member_data):
#     """Prints minimal basic informationa bout the user. 
#     Obviously just scratching the surface. This is just an example."""
#     total_hours_played = extract_hours_played(member_data)
#     print("\nSome basic information about the user:")
#     print("This user's grimoire score is " + str(member_data['grimoireScore']) + '.')
#     print("They have " + str(len(member_data['characters'])) + " characters.")
#     print("They have played a total of " + str(total_hours_played) + " hours of Destiny.") 

# def extract_hours_played(member_data):
#     """Extracts total hours played from member data. Note if they have 
#     multiple characters, you have to extract the data from each character."""
#     total_minutes = 0
#     for character in member_data['characters']:
#         total_minutes += int(character['characterBase']['minutesPlayedTotal'])
    # return round(total_minutes/60)

if __name__ == '__main__':   
    api_key = '22f201d0d1864a4d8d5a7ccc79be8a33'
    membership_id = '4611686018527363836'
    membership_type = 3  # Steam
    character_id = '2305843010228834011'  # Paraselene?

    COMPONENTS_CHARACTERS = '200'
    COMPONENTS_CHARACTER_EQUIPMENT = '205'
    COMPONENTS_CHARACTER_INVENTORIES = '201'

    components = ','.join([COMPONENTS_CHARACTERS, COMPONENTS_CHARACTER_EQUIPMENT, COMPONENTS_CHARACTER_INVENTORIES])

    url = f'https://bungie.net/Platform//Destiny2/{membership_type}/Profile/{membership_id}/?components={components}'
    headers = {"X-API-Key": api_key}
    response = requests.get(url, headers = headers)
    if response.status_code != 200:  
        print(f'Unsuccessful. status_code = {response.status_code}')
        exit(0)

    for item in response.json()['Response']['characterEquipment']['data'][character_id]['items']:
        item_hash = item['itemHash']
        item_instance_id = item['itemInstanceId']
        print(f'itemHash = {item_hash}, itemInstanceId = {item_instance_id}')

    exit(0)


    #############################
    #Test the different functions
    #############################
    #Get user ID from name
    user_id = user_id_from_name(user_name, user_platform, my_api_key)
    if user_id == '0':
        print(user_name + " was not found.")
    else:
        print(user_name + " has id number " + user_id + '.')

    exit(0)

    #Get their member summary and pull some basic information 
    character_data = info_from_id(user_id, my_api_key)
    
    #Find their bungie account information, clan id, clan name
    user_bungie_account, user_clan_name, user_clan_id = get_clan_info(user_id, user_platform, my_api_key)
    if user_clan_name:
        print(user_name + " is in the clan named '" + user_clan_name + "'")
    else:
        print(user_name + " is not in a clan.")
        
    #Get data about every clan member
    if user_clan_id:
        clan_data = get_clan_member_data(user_clan_id, my_api_key)
        
    #clan_data has *lots* of data about the clan
    if user_clan_id:
        print(clan_data.keys())
        
    #Let's find out how many members there are in the clan, and print their names
    if user_clan_id:
        clan_member_list = clan_data['results']
        num_members = len(clan_member_list)
        print("\nThere are " + str(num_members) + " members of the " + user_clan_name + " clan.")
        print("Let's list them all!")

        print("\n----------------------\n" + user_clan_name + " Member List\n----------------------")
        clan_member_names = []
        for member_num in range(num_members):
            temp_member_name = clan_member_list[member_num]['user']['displayName']
            clan_member_names.append(temp_member_name)
            print(str(member_num+1) + ": " + temp_member_name)
