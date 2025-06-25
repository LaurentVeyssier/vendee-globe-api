from datetime import datetime
from typing import List

from vendee_globe_api.db.models import BoatBase, RaceBase


def get_min_datetime() -> datetime:
    # TODO: get min_datetime in the race db
    pass


def get_max_datetime() -> datetime:
    # TODO: get max_datetime in the race db
    pass


def get_partial_race() -> List[RaceBase]:
    # TODO: return race data up to a `actual_time` datetime which is passed as parameter
    pass


def get_boats() -> List[BoatBase]:
    # TODO: return all boats static information
    pass
