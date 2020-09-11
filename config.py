from pydantic import BaseConfig

class settings(BaseConfig):
    DATABASE_URI = 'sqlite:///./database.db'