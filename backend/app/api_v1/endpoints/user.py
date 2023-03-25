import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.api_v1.crud.user_crud import save_user, read_cookies, get_users, set_active_user, delete_user, get_active_user
from app.api_v1.schemas.user_schema import UserSchema, UserDeleteSchema, ActiveUserSchema
from app.api_v1.services.mercury import manager
from app.db.database import get_db

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/check", status_code=status.HTTP_200_OK)
async def check_login_and_password_route(user: UserSchema, db: Session = Depends(get_db)):
    cookies = read_cookies(db=db, login=user.login)
    manager.login(
        login=user.login,
        password=user.password,
        cookies=cookies,
    )
    if manager.is_auth:
        user_for_save = UserSchema(login=user.login,
                                   password=user.password,
                                   cookies=json.dumps(manager.client.session.sess.cookies.get_dict()))
        save_user(db=db, user=user_for_save)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[UserSchema])
async def get_users_route(db: Session = Depends(get_db)):
    users = get_users(db=db)
    return users


@router.get("/set/{login}", status_code=status.HTTP_200_OK)
async def set_active_user_route(login: str, db: Session = Depends(get_db)):
    try:
        set_active_user(db=db, login=login)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/active", status_code=status.HTTP_200_OK, response_model=ActiveUserSchema)
async def get_active_user_route(db: Session = Depends(get_db)):
    user = get_active_user(db=db)
    if user is None:
        return ActiveUserSchema(login='Нет активного пользователя')
    return user


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_user_route(user: UserDeleteSchema, db: Session = Depends(get_db)):
    if not delete_user(login=user.login, db=db):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
