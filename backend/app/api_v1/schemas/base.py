from pydantic import BaseModel

from humps.camel import case


class CamelModel(BaseModel):
    class Config:
        alias_generator = case
        allow_population_by_field_name = True
