import os 
from dotenv import load_dotenv
import requests
load_dotenv()

BASE_URL= 'http://quotes.stormconsultancy.co.uk/random.json'
def get_quotes():
    response = requests.get(BASE_URL).json()
    return response