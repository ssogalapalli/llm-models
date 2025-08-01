import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
#load env file
load_dotenv()
# Read keys from .env file
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("OLLAMA_OPENAI_API_KEY")
def connect_ollama():
    ollama_via_openai = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    return ollama_via_openai

