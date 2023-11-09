from enum import Enum

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Env(str, Enum):
    Local = "local"
    Development = "development"
    Release = "release"
    Production = "production"


class Environment(BaseSettings):
    host: str
    port: int
    env: str
    secret_key: str
    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str
    debug: bool


env_data = Environment()
