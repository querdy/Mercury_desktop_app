from sqlalchemy.orm import Session

from app.api_v1 import models
from app.api_v1.schemas.user_schema import UserSchema


def save_user(db: Session, user: UserSchema):
    if get_user_by_login(db=db, login=user.login):
        set_active_user(db=db, login=user.login)
        return None
    db.query(models.User).update({'is_active': False})
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    return created_user


def get_active_user(db: Session):
    query = db.query(models.User).filter_by(is_active=True).first()
    return query


def get_users(db: Session):
    query = db.query(models.User).all()
    return query


def get_user_by_login(db: Session, login: str):
    query = db.query(models.User).filter_by(login=login).first()
    return query


def save_cookies(db: Session, login: str, cookies: str):
    user_in_db = get_user_by_login(db=db, login=login)
    user_in_db.cookies = cookies
    db.commit()


def read_cookies(db: Session, login: str):
    user_in_db = get_user_by_login(db=db, login=login)
    return user_in_db and user_in_db.cookies


def set_active_user(db: Session, login: str):
    db.query(models.User).update({'is_active': False})
    db.query(models.User).filter_by(login=login).update({'is_active': True})
    db.commit()


def delete_user(db: Session, login: str):
    query = db.query(models.User).filter_by(login=login).delete()
    db.commit()
    return bool(query)
