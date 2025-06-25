from datetime import datetime

from fastapi import FastAPI

from vendee_globe_api.db import crud, session

app = FastAPI()
start_time = datetime.now()
with next(session.get_db()) as db:
    min_datetime = crud.get_min_datetime(db=db)
    max_datetime = crud.get_max_datetime(db=db)
total_duration = (max_datetime - min_datetime).total_seconds() / 60


# TODO: define a /boats route that returns all boats static information
...

# TODO: define a /race route that return race data, up to the equivalent race elapsed time.
# You should make a time conversion between our timer (defined from settings.timer, in minutes) and
# the race time (defined with total_duration, in minutes), min_datetime and max_datetime
# Display only the relevant data
...
