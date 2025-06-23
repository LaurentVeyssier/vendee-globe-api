from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TripBase(Base):
    __tablename__ = "boats"

    nat_voile = Column(String, primary_key=True, nullable=False)
    skipper = Column(String, nullable=False)
    boat = Column(String, nullable=False)
    color = Column(String, nullable=False)
    skipper_first_name = Column(String, nullable=False)
    skipper_last_name = Column(String, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    mast_height = Column(Float, nullable=False)
    upwind_sail_area = Column(Float, nullable=False)
    downwind_sail_area = Column(Float, nullable=False)
    gender = Column(Integer, nullable=False)
    nationality = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    n_participations = Column(Integer, nullable=False)
    foil = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)


class HistoryBase(Base):
    __tablename__ = "race"

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer, nullable=False)
    nat_voile = Column(String, ForeignKey("boats.nat_voile"), nullable=False)
    date = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    cap_30min = Column(Float, nullable=False)
    vitesse_30min = Column(Float, nullable=False)
    vmg_30min = Column(Float, nullable=False)
    distance_30min = Column(Float, nullable=False)
    cap_last = Column(Float, nullable=False)
    vitesse_last = Column(Float, nullable=False)
    VMG_last = Column(Float, nullable=False)
    distance_last = Column(Float, nullable=False)
    cap_24h = Column(Float, nullable=False)
    vitesse_24h = Column(Float, nullable=False)
    vmg_24h = Column(Float, nullable=False)
    distance_24h = Column(Float, nullable=False)
    dtf = Column(Float, nullable=False)
    dtl = Column(Float, nullable=False)
