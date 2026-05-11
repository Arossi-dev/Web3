from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Balance(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String(42), nullable=False, index=True)
    token_symbol = Column(String(10), nullable=False)
    balance = Column(Numeric(36, 18), nullable=False)
    collected_at = Column(DateTime, default=lambda: datetime.now(timezoneutc))
