from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from vendee_globe_api.db.models import BoatBase, RaceBase


def get_min_datetime(db: Session) -> datetime:
    # TODO: query the db to return the minimum datetime
    pass


def get_max_datetime(db: Session) -> datetime:
    r# TODO: query the db to return the maximum datetime
    pass


def get_partial_race(db: Session, actual_time: datetime) -> List[RaceBase]:
    # TODO: query the RaceBase db and do the following operations:
    # 1. filter date_time < actual_time
    # 2. order by date_time
    pass


def get_boats(db: Session) -> List[BoatBase]:
    # TODO: query the db to return all boats information
    pass
