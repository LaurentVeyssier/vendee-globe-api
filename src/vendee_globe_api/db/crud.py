from typing import List

from sqlalchemy.orm import Session

from vendee_globe_api.db.models import BoatBase, RaceBase


# Read (single trip by id)
def get_full_race(trips_db: Session) -> List[RaceBase]:
    return trips_db.query(RaceBase).all()


def get_boats(history_db: Session) -> List[BoatBase]:
    return history_db.query(BoatBase).all()
