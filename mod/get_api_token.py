import requests
import json
from config import *
import logging
from mod.mongo_model import *


# 日志
logging.basicConfig(format='%(asctime)s %(message)s', filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.INFO)


def get_this_api_token():
    try:
        username = Settings.Chatgpt["username"]
        password = Settings.Chatgpt["password"]
        url = Settings.Chatgpt["token_url"]
        data = {"username": username, "password": password}
        res = requests.post(url, data=data)
        logging.info("get_this_api_token res")
        return res.json()["access_token"]
    except:
        return "获取验证码失败..."
