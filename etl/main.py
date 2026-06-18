import sys
import os

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add it to the front of sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


from utils.SparkUtils import SparkSessionFactory
from pyspark.sql.functions import explode, col
#from helpers.GetEnv import GetEnv
import requests
import json

import logging

etl_logger = logging.getLogger(__name__)

def extract() -> None:
    logging.basicConfig(filename='./logs/etl_logs/extract.log', level=logging.INFO)
    try:
        etl_logger.info('Extract Started')

        r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
        if r.status_code == 200:
            data = r.json()
            # print(data['elements'])
            transform(data['teams'], data['elements'])

            etl_logger.info('Extract Finished Passing to transform function')
    except Exception as e:
        etl_logger.error(e)


def transform(teams : list, players : list) -> None:

    print(f"Type of players: {type(players)}")
    print(f"Number of players in list: {len(players)}")
    spark_session = SparkSessionFactory.create_spark_session()
    players_rdd = spark_session.sparkContext.parallelize([json.dumps(p) for p in players])
    players_df = spark_session.read.json(players_rdd)
    print(players_df.printSchema())



def load():
    return None


if __name__ == "__main__":
    extract()
