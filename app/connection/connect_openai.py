import os
from openai import OpenAI
from dotenv import load_dotenv
#load env file
load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')
model = os.getenv("MODEL")

def connect_openai():
    return OpenAI()