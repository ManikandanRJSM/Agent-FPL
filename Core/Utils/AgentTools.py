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

@tool
def get_player_suggestion(player_data : str, transfer_balance : int) -> str:
    """Suggest the best player to transfer based on the given player data JSON and the manager's transfer balance. you will get all the players data here as JSON compare the player data with players JSON and give the suggestion""" 
    from Utils.SparkUtils import SparkSessionFactory
    from Constants.DataConstants import players_columns, teams_columns
    import json

    player_data_dict = json.loads(player_data)
    spark_session = SparkSessionFactory.create_spark_session()

    all_players_df = spark_session.read.parquet("../../data/players")

    players_df = all_players_df \
        .filter( (all_players_df.player_id !=  player_data_dict['player_id']) & (all_players_df.player_element_type ==  player_data_dict['player_element_type'])) \
        .select(*players_columns, *teams_columns)

    data_to_llm = {
        'user_selected_player_data' : player_data,
        'all_player_data' : [json.loads(row) for row in players_df.toJSON().collect()]
    }
    json_string = json.dumps(data_to_llm)
    return json_string