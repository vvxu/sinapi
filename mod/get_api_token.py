import requests
import json
from config import *


def get_this_api_token():
    url = Settings.Api["token_url"]
    data = {"username": Settings.Api["username"], "password": Settings.Api["password"]}
    res = requests.post(url, data=data) 
    return res.json()["access_token"]
