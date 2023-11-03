import os
from enum import Enum

from dotenv import load_dotenv


class Env(str, Enum):
    Local = "local"
    Development = "development"
    Release = "release"
    Production = "production"


class Environment:
    def __init__(self) -> None:
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = int(os.getenv("DB_PORT", "1521"))
        self.ENV: Env = os.getenv("ENV", Env.Local)

    def get_json(self):
        return self.__dict__.__repr__()


def load_env():
    load_dotenv()


env_data = Environment()
