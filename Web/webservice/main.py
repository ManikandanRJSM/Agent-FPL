import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI, Header
from Core.CoreController import Agents

app = FastAPI()


@app.get("/get_manager_details/{manager_id}")
def getManagerDetails(manager_id: int):

    manager_details_agent = Agents()
    data = manager_details_agent.featchManagerAgent(manager_id)

    return {"status_code" : 200, "status" : "SUCCESS", "data": data}


@app.get("/get_manger_players/{manager_id}")
def getManagerPlayers(manager_id : int, authorization: str | None = Header(None)):
    import requests
    from Utils.SparkUtils import SparkSessionFactory
    from Constants.DataConstants import players_columns, teams_columns
    from pyspark.sql.functions import broadcast

    spark_session = SparkSessionFactory.create_spark_session()

    headers = {
        "Authorization": f"Bearer {authorization}",
        "Accept": "application/json"
    }
    r = requests.get(f"https://fantasy.premierleague.com/api/my-team/{manager_id}/", headers=headers)
    manger_reqt = requests.get(f'https://fantasy.premierleague.com/api/entry/{manager_id}')
    data = {}

    if r.status_code == 200 and manger_reqt.status_code == 200:
        
        player_data = r.json()['picks']
        manger_data = manger_reqt.json()
        player_df = spark_session.createDataFrame(player_data);

        all_players_df = spark_session.read.parquet("../../data/players").alias("players")
        all_teams_df = spark_session.read.parquet("../../data/teams").alias("teams")
        joined_df = (
            player_df
            .join(broadcast(all_players_df), player_df["element"] == all_players_df["id"], how="inner")
            .join(broadcast(all_teams_df), all_players_df["team"] == all_teams_df["id"], how="inner")
            .select(*players_columns, *teams_columns)
        )
        
        data = {
            'status_code' : r.status_code,
            'status' : 'SUCCESS',
            'data' : {
                'player_data' : [json.loads(row) for row in joined_df.toJSON().collect()],
                'manager_data' : {
                    'user_name' : manger_data['name'],
                    'transfer_balance' : manger_data['last_deadline_bank'],
                }
            }
        }
    else:
        data = {
            'status_code' : r.status_code,
            'status' : 'FAILED',
            'data' : {
                'player_data' : r.json(),
                'manager_data' : manger_reqt.json()
            }
        }
    
    return data