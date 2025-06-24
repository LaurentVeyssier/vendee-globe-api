import typing as t
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from vendee_globe_api.config import settings
from vendee_globe_api.db import crud, session
from vendee_globe_api.models import Boat, RaceSample

app = FastAPI()
start_time = datetime.now()
with next(session.get_db()) as db:
    min_datetime = crud.get_min_datetime(db=db)
    max_datetime = crud.get_max_datetime(db=db)
total_duration = (max_datetime - min_datetime).total_seconds() / 60


@app.get("/boats", response_model=t.List[Boat])
def get_boats(db: t.Annotated[Session, Depends(session.get_db)]):
    return crud.get_boats(db=db)


@app.get("/race", response_model=t.List[RaceSample])
def get_race(db: t.Annotated[Session, Depends(session.get_db)]):
    elapsed_time_ratio = (
        (datetime.now() - start_time).total_seconds() / 60
    ) / settings.timer
    equivalent_time = min_datetime + timedelta(
        minutes=total_duration * elapsed_time_ratio
    )
    return crud.get_partial_race(db=db, actual_time=equivalent_time)
