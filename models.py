from sqlalchemy import Column, Integer, String, Date, Enum as SQLAlchemyEnum
from database import Base
from schemas import CategoryEnum

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    activity_name = Column(String, index=True)
    duration_minutes = Column(Integer)
    date = Column(Date)
    category = Column(SQLAlchemyEnum(CategoryEnum))
    notes = Column(String, nullable=True)
