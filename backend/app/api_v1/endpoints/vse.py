from itertools import groupby
from typing import Any

from fastapi import Body, Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.api_v1.crud.vse_crud import save_vse_param, save_vse_targets, get_active_vse_param, get_active_product_target, \
    get_all_enterprise, update_enterprise_list, get_products, get_active_vse_params, get_vse_param, \
    update_active_vse_params, get_vse_targets, update_products
from app.api_v1.schemas.transaction_schema import TrafficMsgSchema, PushVseSchema
from app.api_v1.schemas.vse_schema import ProductSchema, EnterpriseForVseSchema, CreateEnterprisesSchema, \
    ReturnProductsSchema, ReturnActiveVseParamSchema, ReturnVseParamSchema, CreateActiveVseParamSchema, \
    ReturnTargetVseSchema, UpdateProductsSchema
from app.api_v1.tasks.vse.vse import parse_vse_parameters, add_base_vse, get_vse_guid, push_vse, parse_target_list, \
    save_vse, get_vse_products, choose_enterprise
from app.db.database import get_db


router = APIRouter(prefix="/vse", tags=["vse"])


@router.get("/enterprise", status_code=status.HTTP_200_OK, response_model=list[EnterpriseForVseSchema])
async def get_enterprises_route(db: Session = Depends(get_db)) -> Any:
    enterprises = get_all_enterprise(db=db)
    return enterprises


@router.post("/enterprise", status_code=status.HTTP_201_CREATED)
async def create_enterprises(enterprises: CreateEnterprisesSchema, db: Session = Depends(get_db)) -> Any:
    update_enterprise_list(db=db, enterprises=enterprises)


@router.get("/product", status_code=status.HTTP_200_OK, response_model=ReturnProductsSchema)
async def get_products_route(db: Session = Depends(get_db)):
    products = get_products(db=db)
    return ReturnProductsSchema(products=products)


@router.get("/active_vse_param", status_code=status.HTTP_200_OK)
async def get_active_vse_param_route(db: Session = Depends(get_db)):
    active_vse_params = get_active_vse_params(db=db)
    return ReturnActiveVseParamSchema(active_vse_params=active_vse_params)


@router.post("/active_vse_param", status_code=status.HTTP_201_CREATED)
async def create_active_vse_param_route(active_vse_params: CreateActiveVseParamSchema, db: Session = Depends(get_db)):
    update_active_vse_params(active_vse_params=active_vse_params, db=db)


@router.get("/vse_param/{transaction_pk}/{enterprise_pk}", status_code=status.HTTP_200_OK)
async def get_vse_params(transaction_pk: str, enterprise_pk: str, db: Session = Depends(get_db)):
    products = get_vse_products(transaction_pk=transaction_pk, db=db)
    save_vse_targets(db=db, vse_targets=parse_target_list())
    for product in products:
        try:
            vse_pk = add_base_vse(traffic_pk=products.get(product), enterprise_pk=enterprise_pk)
            vse_params = parse_vse_parameters(vse_pk=vse_pk)
            save_vse_param(db=db, product=ProductSchema(product_name=product, vse_params=vse_params))
        except ValueError:
            continue


@router.get("/vse_param", status_code=status.HTTP_200_OK)
async def get_vse_param_route(db: Session = Depends(get_db)):
    vse_params = get_vse_param(db=db)
    return ReturnVseParamSchema(vse_params=vse_params)


@router.get("/vse_target", status_code=status.HTTP_200_OK)
async def get_vse_targets_route(db: Session = Depends(get_db)):
    vse_targets = get_vse_targets(db=db)
    return ReturnTargetVseSchema(targets=vse_targets)


@router.put("/vse_target", status_code=status.HTTP_200_OK)
async def update_vse_targets_route(products: UpdateProductsSchema, db: Session = Depends(get_db)):
    update_products(db=db, products=products)


@router.post("/push_vse", status_code=status.HTTP_200_OK)
async def push_vse_route(transaction: PushVseSchema = Body(), db: Session = Depends(get_db)):
    # products = get_vse_products(transaction_pk='6061471893', db=db)
    products = get_vse_products(transaction_pk=transaction.transaction_pk, db=db)
    # choose_enterprise(enterprise_pk='1176144')
    choose_enterprise(enterprise_pk=transaction.enterprise_pk)
    for product in products:
        target = get_active_product_target(db=db, product_name=product)
        vses = get_active_vse_param(db=db, product_name=product)
        if not vses or not target:
            continue
        try:
            vse_pk = add_base_vse(traffic_pk=products.get(product), enterprise_pk=transaction.enterprise_pk)
        except ValueError:
            continue
        vse_guid = get_vse_guid(vse_pk=vse_pk)
        for vse in vses:
            push_vse(vse_index=vse.value,
                     fact_value=vse.fact_value,
                     conclusion=vse.conclusion,
                     vse_pk=vse_pk,
                     vse_guid=vse_guid
                     )
        save_vse(target_pk=target, vse_pk=vse_pk)
        # save_vse(target_pk='481', vse_pk=vse_pk)
        # save_vse(target_pk=product.vse_target, vse_pk=vse_pk)
    # save_vse_targets(db=db, vse_targets=parse_target_list())
