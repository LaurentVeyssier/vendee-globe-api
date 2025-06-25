from datetime import datetime

from pydantic import BaseModel, Field


class Boat(BaseModel):
    nat_voile: str = Field(description="Identifier of the boat")
    name: str = Field(description="Boat name")
    color: str = Field(description="Boat color")
    skipper_first_name: str = Field(description="skipper first name")
    skipper_last_name: str = Field(description="skipper last name")
    length: float | None = Field(description="boat length")
    width: float | None = Field(description="boat width")
    mast_height: float | None = Field(description="boat mast height")
    upwind_sail_area: float | None = Field(description="boat upwind sail area")
    downwind_sail_area: float | None = Field(description="boat downwind sail area")
    gender: int = Field(description="skipper gender")
    age: int = Field(description="skipper age")
    n_participations: int = Field(description="number of participations of the skipper")
    foil: int = Field(description="whether the boat has a foil (1) or not (0)")
    year: int = Field(description="boat year of construction")


class RaceSample(BaseModel):
    id: int = Field(description="Race observation ID")
    rank: int = Field(description="Skipper rank")
    nat_voile: str = Field(description="Boat unique identifier")
    date_time: datetime = Field(
        description="exact date and time of the race observation"
    )
    latitude: float = Field(description="latitude of the observed boat")
    longitude: float = Field(description="longitude of the observed boat")
    heading_30min: float = Field(description="Heading over the last 30 minutes")
    speed_30min: float = Field(description="Speed over the last 30 minutes")
    vmg_30min: float = Field(description="VMG over the last 30 minutes")
    distance_30min: float = Field(
        description="Distance covered over the last 30 minutes"
    )
    heading_last: float = Field(description="Most recent heading")
    speed_last: float = Field(description="Most recent speed")
    VMG_last: float = Field(description="Most recent VMG")
    distance_last: float = Field(description="Most recent distance covered")
    heading_24h: float = Field(description="Heading over the last 24 hours")
    speed_24h: float = Field(description="Speed over the last 24 hours")
    vmg_24h: float = Field(description="VMG over the last 24 hours")
    distance_24h: float = Field(description="Distance covered over the last 24 hours")
    distance_to_finish: float = Field(description="Distance to the finish line")
    distance_to_leader: float = Field(description="Distance to the race leader")

    # TODO: define a field validator that validates field "date_time" with parameter `mode="before"`
    # This field validator, named `parse_str_to_datetime`, transforms the date_time field (initially str)
    # to a datetime field
    ...
