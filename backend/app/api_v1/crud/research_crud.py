from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api_v1 import models
from app.api_v1.models import Enterprise
from app.api_v1.schemas.research_schema import EnterpriseSchema, ResearchSchema
from app.db.database import Base


def get_enterprise(db: Session, enterprise_uuid: int):
    query = db.query(models.Enterprise).get(enterprise_uuid)
    return query


def get_enterprise_by_name(db: Session, enterprise_name: str):
    query = db.query(models.Enterprise).filter_by(enterprise_name=enterprise_name).first()
    return query


def get_all_enterprise(db: Session):
    query = db.query(models.Enterprise).all()
    return query


def create_enterprise(db: Session, enterprise: EnterpriseSchema) -> Enterprise:
    enterprise_dict = enterprise.dict()
    researches = enterprise_dict.pop("researches", [])
    created_enterprise = models.Enterprise(**enterprise_dict)

    for research in researches:
        created_research = models.Research(**research)
        created_enterprise.researches.append(created_research)

    db.add(created_enterprise)
    db.commit()
    return created_enterprise


def create_research(db: Session, research: ResearchSchema):
    research_dict = research.dict()
    created_research = models.Research(**research_dict)
    db.add(created_research)
    db.commit()
    return created_research


def update_enterprise(db: Session, enterprise: EnterpriseSchema):
    enterprise_in_db = get_enterprise(db=db, enterprise_uuid=enterprise.uuid)
    enterprise_dict = enterprise.dict()
    enterprise_dict.pop('uuid', None)

    researches = enterprise_dict.pop("researches", [])
    diff_research = get_uuids_difference(enterprise_in_db.researches, researches)
    if diff_research:
        db.query(models.Research).filter(models.Research.uuid.in_(diff_research)).delete()

    for research in researches:
        research_uuid = research.pop('uuid', None)
        if research_uuid is not None:
            research_in_db = db.query(models.Research).get(research_uuid)
            if research_in_db is None:
                raise HTTPException(
                    status_code=422,
                    detail="Не верные данные. Не существующий uuid."
                )
            db.query(models.Research).filter_by(uuid=research_uuid).update(research)
        else:
            created_research = models.Research(**research)
            enterprise_in_db.researches.append(created_research)
    db.query(models.Enterprise).filter_by(uuid=enterprise.uuid).update(enterprise_dict)
    db.commit()
    return enterprise_in_db


def delete_enterprise(db: Session, enterprise_uuid: int):
    query = db.query(models.Enterprise).filter_by(uuid=enterprise_uuid).delete()
    db.commit()
    return bool(query)


def get_uuids_difference(array_in_db: list[Base], new_array: list[dict]) -> set:
    uuids_db = set([each.uuid for each in array_in_db])
    uuids_upd = set([each.get("uuid") for each in new_array if each.get("uuid")])
    return uuids_db - uuids_upd
