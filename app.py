# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Response
from models import *
import hashlib
from mod.voce_bot import *
from mod.wechat_model import *
# from mod.mongo_model import *
import time
from starlette.responses import HTMLResponse
# from lxml import etree


app = FastAPI()


@app.get("/")
async def index():
    return "你好"


# 验证连接
@app.get("/voce_api")
async def get_voce_api():
    return {"status": "OK"}


# 连接
@app.post("/voce_api")
async def post_voce_api(data: VoceMsg, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_handler, data)
    return {"status": "OK"}


#     
async def run_handler(data):
    print(f"执行到31 {time.time()}")
    handler = MessageHandler(data)
    print(f"执行到32 {time.time()}")
    handler.handle()


# 微信公众号接口
@app.get("/wechatOA")
async def wechat(signature: str, echostr: str, timestamp: str, nonce: str):
    if not all([signature, timestamp, nonce, echostr]):
        return "参数校验失败"
    sign = hashlib.sha1("".join(sorted([Settings.WechatOA["token"], timestamp, nonce])).encode('UTF-8')).hexdigest()
    return HTMLResponse(content=echostr if sign == signature else "error")


@app.post("/wechatOA")
async def wechat(request: Request):
    wechat_handler = WeChatOAHandler(await request.body())
    return wechat_handler.handle()
