from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class ExecutedTransaction(Base):
    __tablename__ = "executed_transaction"

    uuid = Column(Integer, primary_key=True, index=True)
    transaction = Column(String, unique=True)
    execution_traffic = relationship("ExecutionTraffic", back_populates="executed_transaction")


class ExecutionTraffic(Base):
    __tablename__ = "execution_traffic"

    uuid = Column(Integer, primary_key=True, index=True)
    traffic = Column(String)
    transaction = Column(ForeignKey("executed_transaction.transaction"))
    executed_transaction = relationship("ExecutedTransaction", back_populates="execution_traffic")
