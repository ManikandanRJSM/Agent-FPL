from langchain.tools import tool
import requests
import json


@tool
def get_manager_details(manager_id : int) -> str:
    """get the manager details based on the manager id. this uses python package called requests to featch the manager details via api call and retrun the manager details as json or give the error repose as json"""
    r = requests.get(f'https://fantasy.premierleague.com/api/entry/{manager_id}')

    result = {}

    if r.status_code == 200:
        raw_data = r.json()
        result = {
            'manager_id' : raw_data['id'],
            'first_name' : raw_data['player_first_name'],
            'last_name' : raw_data['player_last_name'],
            'user_name' : raw_data['name'],
            'transfer_balance' : raw_data['last_deadline_bank'],
            'reagion_id' : raw_data['player_region_id'],
            'reagion_name' : raw_data['player_region_name'],
            'reagion_short_code' : raw_data['player_region_iso_code_short'],
            'reagion_long_code' : raw_data['player_region_iso_code_long'],
        }
    json_string = json.dumps(result)
    # print(json_string)
    return json_string

# get_manager_details.invoke({"manager_id": 5125930})


def get_player_suggestion(player_data : str, transfer_balance : int) -> str:
    pass