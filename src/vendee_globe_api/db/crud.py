from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from vendee_globe_api.db.models import BoatBase, RaceBase


def get_min_datetime(db: Session) -> datetime:
    return db.query(func.min(RaceBase.date_time)).scalar()


def get_max_datetime(db: Session) -> datetime:
    # TODO: based on the implementation of `get_min_datetime`, implement `get_max_datetime`
    pass


def get_partial_race(db: Session, actual_time: datetime) -> List[RaceBase]:
    # TODO: fill the blanks!
    return (
        db.query(RaceBase)
        .filter(...)
        .order_by(RaceBase.date_time)
        .all()
    )


def get_boats(db: Session) -> List[BoatBase]:
    return db.query(BoatBase).all()
