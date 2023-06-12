import os

# openai
openai_key = os.environ.get('OPENAI_KEY')

# mongo
mongo_uri = os.environ.get('MONGO_URI')

# voce_chat
voce_secret = os.environ.get('VOCE_SECRET')
voce_url = os.environ.get('VOCE_URL')
voce_bot_id = os.environ.get('VOCE_BOT_ID')
voce_dbname = os.environ.get('VOCE_DBNAME')

# api
api_token_url = os.environ.get('API_TOKEN_URL')
user_info_secret_key = os.environ.get('USER_INFO_SECRET_KEY')
access_token_expire_minutes = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

# 微信
wechat_oa_token = os.environ.get('WECHAT_OA_TOKEN')

# chatgpt
chatgpt_username = ""
chatgpt_password = ""
chatgpt_token_url = ""

chatgpt_expire_minutes = os.environ.get('CHATGPT_EXPIRE_MINUTES')

voce_bot_dict = {}


class Settings:
    Api = {
        "HOST": "0.0.0.0",
        "APP_NAME": "sin_api",
        "PORT": 20001,
        "RELOAD": True,
        "token_url": api_token_url,
        "secret_key": user_info_secret_key,
        "access_token_expire_minutes": access_token_expire_minutes,
        "algorithm": "HS256",
    }
    TokenData = {
        "chatgpt_expire_minutes": chatgpt_expire_minutes
    }
    WechatOA = {
        "token": wechat_oa_token
    }
    Openai = {
        "secret": openai_key,
        "model": "gpt-3.5-turbo",
    }
    VoceChat = {
        "secret": voce_secret,
        "url": voce_url,
        "sent_to": "send_to_user",
        "bot_id": str(voce_bot_id),
        "dbname": voce_dbname,
        "bot": voce_bot_dict
    }
    Mongo = {
        "uri": mongo_uri
    }