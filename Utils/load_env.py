from dotenv import load_dotenv, dotenv_values
import os


@staticmethod
def get_env_variables():
    # Absolute path to project root (one level up from Utils/)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    env_path = os.path.join(BASE_DIR, ".env")

    return dotenv_values(env_path)