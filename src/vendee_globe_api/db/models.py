from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BoatBase(Base):
    __tablename__ = "boats"

    nat_voile = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skipper_first_name = Column(String, nullable=False)
    skipper_last_name = Column(String, nullable=False)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    mast_height = Column(Float, nullable=True)
    upwind_sail_area = Column(Float, nullable=True)
    downwind_sail_area = Column(Float, nullable=True)
    gender = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    n_participations = Column(Integer, nullable=False)
    foil = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


class RaceBase(Base):
    __tablename__ = "race"

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer, nullable=False)
    nat_voile = Column(String, ForeignKey("boats.nat_voile"), nullable=False)
    date_time = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    heading_30min = Column(Float, nullable=False)
    speed_30min = Column(Float, nullable=False)
    vmg_30min = Column(Float, nullable=False)
    distance_30min = Column(Float, nullable=False)
    heading_last = Column(Float, nullable=False)
    speed_last = Column(Float, nullable=False)
    VMG_last = Column(Float, nullable=False)
    distance_last = Column(Float, nullable=False)
    heading_24h = Column(Float, nullable=False)
    speed_24h = Column(Float, nullable=False)
    vmg_24h = Column(Float, nullable=False)
    distance_24h = Column(Float, nullable=False)
    distance_to_finish = Column(Float, nullable=False)
    distance_to_leader = Column(Float, nullable=False)
