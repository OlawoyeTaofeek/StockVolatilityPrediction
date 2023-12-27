"""This module extracts information from your `.env` file so that
you can use your AlphaVantage API key in other parts of the application.
"""

import os
from pydantic_settings import BaseSettings 

def return_full_path(filename: str = ".env") -> str:
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    full_path = os.path.join(directory_name, filename)
    return full_path

class Settings(BaseSettings):
    alpha_vantage_api_key: str
    db_name: str
    model_directory: str

    class Config:
        env_file = return_full_path(".env")

# Create an instance of the `Settings` class
settings = Settings()




