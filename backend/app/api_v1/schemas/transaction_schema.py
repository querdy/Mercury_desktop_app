from pydantic import Field, validator

from app.api_v1.schemas.base import CamelModel


class TrafficSchema(CamelModel):
    traffic: int

    class Config:
        orm_mode = True


class TransactionSchema(CamelModel):
    transaction_pk: int
    traffics: list[TrafficSchema] | None = None

    class Config:
        orm_mode = True

    @validator('transaction_pk')
    def _transaction_pk(cls, value):
        if 0 < value < 9223372036854775807:
            return value
        raise ValueError('Номер транзакции должен соответствовать Int64')


class TrafficMsgSchema(CamelModel):
    traffic: int
    product_name: str
    status: str


class TransactionMsgSchema(CamelModel):
    transaction_pk: int
    traffics: list[TrafficMsgSchema]


class PushResearchSchema(CamelModel):
    enterprise_uuid: int
    transaction_pk: int
    traffic: TrafficMsgSchema

