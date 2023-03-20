from typing import Any

from fastapi import APIRouter, status, Depends, HTTPException, Body

from sqlalchemy.orm import Session

from app.api_v1.crud.research_crud import create_enterprise, get_enterprise, get_all_enterprise, \
    update_enterprise, delete_enterprise
from app.api_v1.schemas.transaction_schema import TransactionSchema, PushResearchSchema, TrafficMsgSchema
from app.api_v1.schemas.research_schema import EnterpriseForResearchSchema, EnterpriseDeleteSchema
from app.api_v1.tasks.research.research import get_traffics, push_research
from app.db.database import get_db

router = APIRouter(prefix="/research", tags=["research"])


@router.post("/enterprise", status_code=status.HTTP_201_CREATED, response_model=EnterpriseForResearchSchema)
async def create_enterprise_route(enterprise: EnterpriseForResearchSchema, db: Session = Depends(get_db)) -> Any:
    try:
        created_enterprise = create_enterprise(db=db, enterprise=enterprise)
        return created_enterprise
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.delete("/enterprise", status_code=status.HTTP_200_OK)
async def delete_enterprise_route(enterprise: EnterpriseDeleteSchema, db: Session = Depends(get_db)):
    if not delete_enterprise(enterprise_uuid=enterprise.uuid, db=db):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get("/enterprise/{uuid}", status_code=status.HTTP_200_OK, response_model=EnterpriseForResearchSchema)
async def get_enterprise_route(uuid: int, db: Session = Depends(get_db)):
    try:
        enterprise = get_enterprise(db=db, enterprise_uuid=uuid)
        return enterprise
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@router.get("/{transaction_pk}/{enterprise_uuid}", status_code=status.HTTP_200_OK)
async def add_research_route(transaction_pk: int, enterprise_uuid: int, db: Session = Depends(get_db)) -> Any:
    TransactionSchema(transaction_pk=transaction_pk)
    return get_traffics(transaction_pk=transaction_pk, enterprise_uuid=enterprise_uuid, db=db)


@router.post("/push_research", status_code=status.HTTP_200_OK, response_model=TrafficMsgSchema)
async def push_research_route(traffic: PushResearchSchema = Body(), db: Session = Depends(get_db)):
    return push_research(enterprise_uuid=traffic.enterprise_uuid,
                         transaction_pk=traffic.transaction_pk,
                         traffic=traffic.traffic.traffic,
                         product=traffic.traffic.product_name,
                         db=db
                         )


@router.get("/enterprises", status_code=status.HTTP_200_OK, response_model=list[EnterpriseForResearchSchema])
async def get_enterprises_route(db: Session = Depends(get_db)) -> Any:
    enterprises = get_all_enterprise(db=db)
    return enterprises


@router.put("/enterprise", status_code=status.HTTP_200_OK, response_model=EnterpriseForResearchSchema)
async def update_enterprise_route(enterprise: EnterpriseForResearchSchema = Body(), db: Session = Depends(get_db)):
    try:
        updated_enterprise = update_enterprise(db=db, enterprise=enterprise)
        return updated_enterprise
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
