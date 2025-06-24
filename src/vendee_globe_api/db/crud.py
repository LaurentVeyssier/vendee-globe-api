from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from vendee_globe_api.db.models import BoatBase, RaceBase


def get_min_datetime(race_db: Session) -> datetime:
    return race_db.query(func.min(RaceBase.date_time)).scalar()


def get_partial_race(race_db: Session, actual_time: datetime) -> List[RaceBase]:
    return (
        race_db.query(RaceBase)
        .filter(RaceBase.date_time <= actual_time)
        .order_by(RaceBase.date_time)
        .all()
    )


def get_boats(boat_db: Session) -> List[BoatBase]:
    return boat_db.query(BoatBase).all()
