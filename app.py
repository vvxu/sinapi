from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Response, Depends, status
import hashlib
from starlette.responses import HTMLResponse
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 引用mod中的方法
from mod.voce_bot import *
from mod.wechat_model import *
from mod.connect_openai import *
from mod.generate_data import *


def get_user_info(user):
    user_information = PymongoCRUD("userinformation", "user")
    print (user)
    filter = {f'user.{user}.username': f'{user}'}
    search_user = user_information.find_one(filter)
    return search_user["user"]


# 密码生成函数
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = Settings.Api["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.Api["access_token_expire_minutes"]
user_info = get_user_info('admin')


# 构建app
app = FastAPI(title=Settings.Api["APP_NAME"])
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    user = get_user(user_info, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="未激活用户")
    return current_user


# @app.get("/")
# async def index():
#     return "dd"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 路由
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(user_info, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


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
    handler = MessageHandler(data)
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
    insert = GenerateCode("chatgpt", 6)
    code = insert.insert_code()
    wechat_handler = WeChatOAHandler(await request.body(), code)
    return wechat_handler.handle()


@app.post("/validate_code")
async def validate_code(verification_code: VerificationCode):
    validate = GenerateCode("chatgpt", 6, verification_code.code)
    return validate.validate_code()


# chatgpt-api
@app.post("/chatgpt")
async def chatgpt(item: dict):
    validate = GenerateCode("chatgpt", 6, item["messages"]["code"])
    if validate.validate_code() == "true":
        ans = send_msg_to_openai(item["messages"]["content"])
        logging.info(f"{item['messages']['code']}提问：{item['messages']['content'][-1]['content']}")
        return {"content": ans}
    return "false"
