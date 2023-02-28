import re
from datetime import datetime
from typing import Optional

from pydantic import validator, ValidationError

from app.api_v1.schemas.base import CamelModel


class ResearchSchema(CamelModel):
    uuid: Optional[int]
    laboratory: str
    disease: str
    date_of_research: str
    method: str = ""
    expertise_id: str
    result: str
    conclusion: str
    product: str = 'main'

    class Config:
        orm_mode = True

    @validator('laboratory')
    def _laboratory(cls, value):
        value = value.strip()
        if len(value) <= 255:
            return value
        raise ValueError('Длина строки не должна превышать 255 символов')

    @validator('disease')
    def _disease(cls, value):
        value = value.strip()
        if len(value) <= 255:
            return value
        raise ValueError('Длина строки не должна превышать 255 символов')

    @validator('date_of_research')
    def _date_of_research(cls, value):
        value = value.strip()
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return value
        except ValueError:
            raise ValueError('Формат даты должен соответствовать %d.%m.%Y')

    @validator('method')
    def _method(cls, value):
        value = value.strip()
        if len(value) <= 255:
            return value
        raise ValueError('Длина строки не должна превышать 255 символов')

    @validator('expertise_id')
    def _expertise_id(cls, value):
        value = value.strip()
        if len(value) <= 255:
            return value
        raise ValueError('Длина строки не должна превышать 255 символов')

    @validator('result')
    def _result(cls, value):
        value = value.strip()
        if value in ['1', '2', '3']:
            return value
        raise ValueError('result должно быть 1, 2 или 3')

    @validator('conclusion')
    def _conclusion(cls, value):
        value = value.strip()
        if len(value) <= 255:
            return value
        raise ValueError('Длина строки не должна превышать 255 символов')


class EnterpriseSchema(CamelModel):
    uuid: Optional[int]
    name: str
    researches: list[ResearchSchema]

    class Config:
        orm_mode = True


class EnterpriseDeleteSchema(CamelModel):
    uuid: int


