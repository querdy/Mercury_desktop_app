from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.api_v1 import models
from app.api_v1.schemas.vse_schema import ProductSchema, TargetVseSchema, EnterpriseForVseSchema, \
    CreateEnterprisesSchema, CreateActiveVseParamSchema, UpdateProductsSchema
from app.db.database import Base


def get_products(db: Session):
    query = db.query(models.Product).all()
    return query


def get_vse_targets(db: Session):
    query = db.query(models.TargetVse).all()
    return query


def update_products(db: Session, products: UpdateProductsSchema):
    for product in products.products:
        product_in_db = db.query(models.Product).get(product.uuid)
        if product_in_db is None:
            raise HTTPException(
                status_code=422,
                detail="Не верные данные. Не существующий uuid."
            )
        product_dict = product.dict()
        product_uuid = product_dict.pop('uuid', None)
        product_dict.pop('vse_params', None)
        product_dict.pop('active_vse_params', None)
        db.query(models.Product).filter_by(uuid=product_uuid).update(product_dict)
    db.commit()


def save_vse_param(db: Session, product: ProductSchema):
    products_in_db = set([product.product_name for product in get_products(db=db)])
    if product.product_name in products_in_db:
        raise ValueError('Продукт уже есть в БД')
    product_dict = product.dict()
    vse_params = product_dict.pop("vse_params", [])
    product_dict.pop("active_vse_params")
    product_dict.pop("vse_target")
    created_product = models.Product(**product_dict)

    for param in vse_params:
        created_vse_param = models.VseParam(**param)
        created_product.vse_params.append(created_vse_param)

    db.add(created_product)
    db.commit()
    return created_product


def delete_all_products(db: Session):
    db.query(models.EnterpriseForVse).delete()
    db.commit()


def save_vse_targets(db: Session, vse_targets: list[TargetVseSchema]):
    db.query(models.TargetVse).delete()
    for target in vse_targets:
        created_target = models.TargetVse(**target.dict())
        db.add(created_target)
    db.commit()


def get_active_vse_param(db: Session, product_name: str):
    query = db.query(models.ActiveVseParam).filter_by(product_name=product_name).all()
    return query


def get_active_product_target(db: Session, product_name: str):
    query = db.query(models.Product).filter_by(product_name=product_name).first()
    return query.vse_target


def get_vse_param(db: Session):
    query = db.query(models.VseParam).all()
    return query


def get_active_vse_params(db: Session):
    query = db.query(models.ActiveVseParam).all()
    return query


def get_all_enterprise(db: Session):
    query = db.query(models.EnterpriseForVse).all()
    return query


def create_enterprise(db: Session, enterprise: EnterpriseForVseSchema):
    db.add(models.EnterpriseForVse(**enterprise.dict()))
    db.commit()


def update_enterprise_list(db: Session, enterprises: CreateEnterprisesSchema):
    db.query(models.EnterpriseForVse).delete()
    for enterprise in enterprises.enterprises:
        enterprise.uuid = None
        db.add(models.EnterpriseForVse(**enterprise.dict()))
    db.commit()


def update_active_vse_params(db: Session, active_vse_params: CreateActiveVseParamSchema):
    db.query(models.ActiveVseParam).delete()
    for param in active_vse_params.active_vse_params:
        created_active_param = models.ActiveVseParam(**param.dict())
        db.add(created_active_param)
    db.commit()
