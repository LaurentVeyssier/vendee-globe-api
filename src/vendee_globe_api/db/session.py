from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import vendee_globe_api.constants as c

engine = create_engine(c.DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, class_=Session, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    trips_db = SessionLocal()
    try:
        yield trips_db
    finally:
        trips_db.close()
