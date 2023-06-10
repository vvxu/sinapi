# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Response, Depends, status
from models import *
import hashlib
from mod.voce_bot import *
from mod.wechat_model import *
from mod.get_api_token import *
from mod.connect_openai import *
import time
from starlette.responses import HTMLResponse
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt


# 密码生成函数
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = Settings.Api["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.Api["access_token_expire_minutes"]


# 构建app
app = FastAPI(title=Settings.Api["APP_NAME"])


def get_user_info(user):
    user_information = PymongoCRUD("userinformation", "user")
    filter = {f'user.{user}.username': f'{user}'}
    search_user = user_information.find_one(filter)
    return search_user["user"]


# 密码部分
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(user_db, username: str, password: str):
    user = get_user(user_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.Api["secret_key"], algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Settings.Api["secret_key"], algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(get_user_info('admin'), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="未激活用户")
    return current_user


# 路由
@app.get("/")
async def index():
    return "你好"


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(get_user_info('admin'), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/verify")
async def verify(item: dict, current_user: User = Depends(get_current_active_user)):
    return "true"


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# chatgpt-api
@app.post("/chatgpt")
async def chatgpt(item: dict, current_user: User = Depends(get_current_active_user)):
    logging.info("提问：%s" % item['messages'][-1]['content'])
    ans = send_msg_to_openai(item["messages"])
    return {"content": ans}


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
