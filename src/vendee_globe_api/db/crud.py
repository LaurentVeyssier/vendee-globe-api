from typing import List

from sqlalchemy.orm import Session

from vendee_globe_api.db.models import BoatBase, RaceBase


def get_full_race(race_db: Session) -> List[RaceBase]:
    return race_db.query(RaceBase).all()


def get_boats(boat_db: Session) -> List[BoatBase]:
    return boat_db.query(BoatBase).all()
