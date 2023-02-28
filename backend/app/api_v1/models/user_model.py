from sqlalchemy import Integer, Column, String, Boolean

from app.db.database import Base


class User(Base):
    __tablename__ = 'user'

    uuid = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    login = Column(String, unique=True)
    password = Column(String)
    cookies = Column(String)
