from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class EnterpriseForVse(Base):
    __tablename__ = "enterprise_for_vse"

    uuid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    mercury_id = Column(String, unique=True)


class TargetVse(Base):
    __tablename__ = "vse_target"

    uuid = Column(Integer, primary_key=True, index=True)
    value = Column(String)
    view = Column(String)


class Product(Base):
    __tablename__ = "product"

    uuid = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, unique=True)
    vse_params = relationship("VseParam", back_populates="product")
    active_vse_params = relationship("ActiveVseParam", back_populates="product")
    vse_target = Column(String, default='481')


class VseParam(Base):
    __tablename__ = "vse_param"

    uuid = Column(Integer, primary_key=True, index=True)
    value = Column(String)
    view = Column(String)
    product_name = Column(ForeignKey("product.product_name", ondelete="CASCADE"))
    product = relationship("Product", back_populates="vse_params")


class ActiveVseParam(Base):
    __tablename__ = "active_vse_param"

    uuid = Column(Integer, primary_key=True, index=True)
    value = Column(String)
    view = Column(String)
    fact_value = Column(String)
    conclusion = Column(String)
    product_name = Column(ForeignKey("product.product_name"))
    product = relationship("Product", back_populates="active_vse_params")


