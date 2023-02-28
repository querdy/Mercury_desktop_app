from typing import Optional

from app.api_v1.schemas.base import CamelModel


class UserSchema(CamelModel):
    uuid: Optional[int]
    is_active: Optional[bool]
    login: str
    password: str
    cookies: Optional[str]

    class Config:
        orm_mode = True


class UserDeleteSchema(CamelModel):
    login: str
