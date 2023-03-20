from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY

from app.db.database import Base


class EnterpriseForResearch(Base):
    __tablename__ = "enterprise_for_research"

    uuid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    researches = relationship("Research", back_populates="enterprise_for_research")


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
    enterprise_name = Column(ForeignKey("enterprise_for_research.name", ondelete="CASCADE"))
    enterprise_for_research = relationship("EnterpriseForResearch", back_populates="researches", uselist=False)


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

