import typing as t
from datetime import datetime

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from vendee_globe_api.db import crud, session
from vendee_globe_api.models import Boat, RaceSample

app = FastAPI()


@app.get("/boats", response_model=t.List[Boat])
def get_boats(db: t.Annotated[Session, Depends(session.get_db)]):
    return crud.get_boats(db=db)


@app.get("/start_datetime", response_model=datetime)
def get_min_datetime(db: t.Annotated[Session, Depends(session.get_db)]):
    return crud.get_min_datetime(db=db)


@app.get("/race", response_model=t.List[RaceSample])
def get_race(db: t.Annotated[Session, Depends(session.get_db)]):
    return crud.get_partial_race(db=db, actual_time=datetime.now())
