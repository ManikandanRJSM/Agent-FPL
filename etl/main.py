import sys
import os

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add it to the front of sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from Utils.SparkUtils import SparkSessionFactory
from pyspark.sql.functions import explode, col
#from helpers.GetEnv import GetEnv
import requests
import json

import logging

etl_logger = logging.getLogger(__name__)
logging.basicConfig(filename='./logs/etl_logs/etl.log', level=logging.INFO)

def extract() -> None:
    try:
        etl_logger.info('Extract Started')

        r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
        if r.status_code == 200:
            data = r.json()
            transform(data['teams'], data['elements'], data['element_types'])

            etl_logger.info('Extract Finished Passing to transform function')
    except Exception as e:
        etl_logger.error(e)


def transform(teams : list, players : list, postion : list) -> None:

    etl_logger.info('Transform Started')

    etl_logger.info(f"Type of players: {type(players)}")
    etl_logger.info(f"Number of players in list: {len(players)}")
    
    etl_logger.info(f"Type of teams: {type(teams)}")
    etl_logger.info(f"Number of teams in list: {len(teams)}")

    spark_session = SparkSessionFactory.create_spark_session()

    players_rdd = spark_session.sparkContext.parallelize([json.dumps(p) for p in players])
    players_df = spark_session.read.json(players_rdd)

    teams_rdd = spark_session.sparkContext.parallelize([json.dumps(t) for t in teams])
    teams_df = spark_session.read.json(teams_rdd)

    postion_rdd = spark_session.sparkContext.parallelize([json.dumps(et) for et in postion])
    postion_df = spark_session.read.json(postion_rdd)
    # players_df.select('element_type').show()
    # exit()
    # print(teams_df.printSchema())

    etl_logger.info('Finished Passing to load function')

    load(teams_df = teams_df, players_df = players_df, element_types_df = postion_df)



def load(**data : dict) -> None:

    etl_logger.info('Load Started')
    data['teams_df'].write.mode("overwrite").parquet(f"./data/teams")
    data['players_df'].write.mode("overwrite").parquet(f"./data/players")
    data['element_types_df'].write.mode("overwrite").parquet(f"./data/positions")

    etl_logger.info('Load finished')


if __name__ == "__main__":
    extract()
