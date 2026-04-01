from sqlalchemy import Column, String, Float
from src.db.database import Base

class ParkingSessionDB(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, index=True)
    plate = Column(String, index=True)
    entry_time = Column(Float)
    exit_time = Column(Float, nullable=True)
    payment_time = Column(Float, nullable=True)
    payment_status = Column(String)
    amount_due = Column(Float)
    status = Column(String, default="ACTIVE")