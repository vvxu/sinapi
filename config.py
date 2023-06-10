import os

openai_key = os.environ.get('OPENAI_KEY')
mongo_uri = os.environ.get('MONGO_URI')
voce_secret = os.environ.get('VOCE_SECRET')
voce_url = os.environ.get('VOCE_URL')
voce_bot_id = os.environ.get('VOCE_BOT_ID')
api_username = os.environ.get('API_USERNAME')
api_passwd = os.environ.get('API_PASSWD')
api_token_url = os.environ.get('API_TOKEN_URL')


class Settings:
    Api = {
        "HOST": "0.0.0.0",
        "APP_NAME": "sin_api",
        "PORT": 20001,
        "RELOAD": True,
        "username": api_username,
        "password": api_passwd,
        "token_url": api_token_url
    }
    Openai = {
        "secret": openai_key,
        "model": "gpt-3.5-turbo",
        "voce_secret": voce_secret,
    }
    VoceChat = {
        "secret": voce_secret,
        "url": voce_url,
        "sent_to": "send_to_user",
        "bot_id": str(voce_bot_id)
    }
    Mongo = {
        "uri": mongo_uri
    }