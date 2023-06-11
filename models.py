from typing import Optional, Union, Set, List
from pydantic import BaseModel
from datetime import datetime, timedelta


# user
# user model
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


# git
class GithubUserModel(BaseModel):
    name: Optional[str]
    blog: str
    bio: Optional[str]
    public_repos: int
    followers: int
    avatar_url: str


# voce
class VoceProperties(BaseModel):
    content_type: Union[str, None] = None
    height: Union[int, None] = None
    width: Union[int, None] = None
    name: Union[str, None] = None
    size: Union[int, None] = None


class VoceDetail(BaseModel):
    content: Union[str, None] = None
    content_type: Union[str, None] = None
    expires_in: Union[str, None] = None
    properties: Union[VoceProperties, None] = None
    type: Union[str, None] = None


class VoceTarget(BaseModel):
    gid: Union[int, None] = None


class VoceMsg(BaseModel):
    created_at: Union[str, None] = None
    detail: Union[VoceDetail, None] = None
    from_uid: Union[int, None] = None
    mid: Union[int, None] = None
    target: Union[VoceTarget, None] = None
    

class VerificationCode(BaseModel):
    code: str
    expire_time: datetime
