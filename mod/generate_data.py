import random
import string
from mod.mongo_model import *
from models import *
from config import *


class GenerateCode:
    def __init__(self, dbname, length=int, code=None):
        self.code = code
        self.length = length
        self.current_db = PymongoCRUD("token", dbname)
        # 验证码时间
        self.token_expire = int(Settings.TokenData["chatgpt_expire_minutes"])
        self.expire_time = int(datetime.now().timestamp() + timedelta(minutes=self.token_expire).total_seconds())
        # 当前时间
        self.current_time = int(datetime.now().timestamp())

    # 生成大写字符串
    def generate_random_string_letters(self):
        # 大小写
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(self.length))
    
    # 生成小写字符串
    def generate_random_string_lowercase(self):
        # 小写
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(self.length))
    
    # 组合写入数据的方法
    def set_current_code(self, code):
        # 当前聊天模式，如果不存在就插入;
        if not self.current_db.find_one({"code": code}):
            self.insert_current_code(code)   
        else:
            self.update_current_code(code)

    def insert_current_code(self, code):
        insert_data = {
            "code": code,
            "expire_time": self.expire_time
        }
        self.current_db.insert_one(insert_data)

    def update_current_code(self, code):
        # 当前聊天模式，如果不存在就插入;
        filter_data = {"code": code}
        update_data = {"code": code, "expire_time": self.expire_time}
        self.current_db.update_one(filter_data, update_data)

    # 插入一条
    def insert_code(self):
        code = self.generate_random_string_lowercase()
        self.set_current_code(code)
        return code

    # 验证
    def validate_code(self):
        find_data = {"code": self.code}
        this_find_data = self.current_db.find_one(find_data)
        if this_find_data["code"] == self.code and this_find_data["expire_time"] > self.current_time:
            return "true"
        return "false"
