from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY

from app.db.database import Base


class Enterprise(Base):
    __tablename__ = "enterprise"

    uuid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    researches = relationship("Research", back_populates="enterprise")


class Research(Base):
    __tablename__ = "research"

    uuid = Column(Integer, primary_key=True, index=True)
    laboratory = Column(String)
    disease = Column(String)
    date_of_research = Column(String)
    method = Column(String, default=None)
    expertise_id = Column(String)
    result = Column(String)
    conclusion = Column(String)
    product = Column(String)
    enterprise_name = Column(ForeignKey("enterprise.name", ondelete="CASCADE"))
    enterprise = relationship("Enterprise", back_populates="researches", uselist=False)


def validate_research(research: Research) -> bool:
    return all([
        research.product,
        research.laboratory,
        research.disease,
        research.date_of_research,
        research.expertise_id,
        research.result,
        research.conclusion,
    ])

