from itertools import groupby
from typing import Optional

from app.api_v1.schemas.base import CamelModel


class EnterpriseForVseSchema(CamelModel):
    uuid: Optional[int]
    name: str
    mercury_id: str

    class Config:
        orm_mode = True


class CreateEnterprisesSchema(CamelModel):
    enterprises: list[EnterpriseForVseSchema | None]


class TargetVseSchema(CamelModel):
    uuid: Optional[int]
    value: str
    view: str

    class Config:
        orm_mode = True


class VseParamSchema(CamelModel):
    uuid: Optional[int]
    value: str
    view: str
    product_name: Optional[str]

    class Config:
        orm_mode = True


class ActiveVseParamSchema(CamelModel):
    uuid: Optional[int]
    value: str
    view: str
    fact_value: str
    conclusion: str
    product_name: Optional[str]

    class Config:
        orm_mode = True


class ProductSchema(CamelModel):
    uuid: Optional[int]
    product_name: str
    vse_params: list[VseParamSchema] | None = None
    active_vse_params: list[ActiveVseParamSchema] | None = None
    vse_target: str | None = None

    class Config:
        orm_mode = True


class ReturnTargetVseSchema(CamelModel):
    targets: list[TargetVseSchema | None]


class ReturnProductsSchema(CamelModel):
    products: list[ProductSchema | None]


class UpdateProductsSchema(CamelModel):
    products: list[ProductSchema | None]


class ReturnActiveVseParamSchema(CamelModel):
    active_vse_params: list[ActiveVseParamSchema | None]


class ReturnVseParamSchema(CamelModel):
    vse_params: list[VseParamSchema | None]

    def dict(self, *args, **kwargs):
        repr = super().dict(*args, **kwargs)
        vse_params = sorted(repr['vseParams'], key=lambda x: x['productName'])
        products = {key: list(value) for key, value in groupby(vse_params, key=lambda x: x['productName'])}
        repr['vseParams'] = products
        return repr


class CreateActiveVseParamSchema(CamelModel):
    active_vse_params: list[ActiveVseParamSchema | None]
