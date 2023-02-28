from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.api_v1 import models
from app.api_v1.schemas.transaction_schema import TransactionSchema, TrafficSchema
from app.api_v1.models import ExecutedTransaction, ExecutionTraffic


def get_all_saved_transactions(db: Session) -> list[Type[ExecutedTransaction]]:
    return db.query(models.ExecutedTransaction).all()


def get_transaction_by_number(db: Session, transaction: int) -> Type[ExecutedTransaction] | None:
    query = db.query(models.ExecutedTransaction).filter_by(transaction=transaction).first()
    return query


def get_all_traffic_by_transaction(db: Session, transaction: int) -> list[Type[ExecutionTraffic]]:
    query = db.query(models.ExecutionTraffic).filter_by(transaction=transaction).all()
    return query


def get_traffic_in_transaction_by_number(db: Session, traffic: int, transaction: int):
    query = db.query(models.ExecutionTraffic).filter_by(traffic=traffic,
                                                        transaction=transaction).first()
    return query


def save_transaction(db: Session, transaction: TransactionSchema | int) -> ExecutedTransaction | None:
    if isinstance(transaction, TransactionSchema):
        saved_transaction = models.ExecutedTransaction(**transaction.dict())
    else:
        saved_transaction = models.ExecutedTransaction(transaction=transaction)
    if get_transaction_by_number(db=db, transaction=transaction):
        raise HTTPException(status_code=400, detail="transaction is in db")
    db.add(saved_transaction)
    db.commit()
    return saved_transaction


def save_traffic(db: Session, transaction: int, traffic: TrafficSchema | int):
    transaction_in_db = get_transaction_by_number(db=db, transaction=transaction)
    saved_traffic = models.ExecutionTraffic(traffic=traffic)
    if get_traffic_in_transaction_by_number(db=db,
                                            traffic=(traffic.traffic if isinstance(traffic, TrafficSchema) else traffic),
                                            transaction=transaction):
        raise HTTPException(status_code=400, detail="traffic is in db")
    if isinstance(traffic, TrafficSchema):
        transaction_in_db.execution_traffic.append(**traffic.dict())
    else:
        transaction_in_db.execution_traffic.append(saved_traffic)
    db.commit()
    return saved_traffic

