import random
import string
from datetime import datetime, timedelta
from models import *


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def generate_code(code):
    expire_time = int(datetime.now().timestamp() + timedelta(hours=1).total_seconds())
    verification_code = VerificationCode(code=code, expire_time=expire_time)
    codes.append(verification_code)
    return code
