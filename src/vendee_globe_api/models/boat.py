from pydantic import BaseModel, Field


class Boat(BaseModel):
    nat_voile: str = Field(description="Identifier of the boat")
    skipper: str = Field(description="Skipper name")
    name: str = Field(description="Boat name")
    color: str = Field(description="Boat color")
    skipper_first_name: str = Field(description="skipper first name")
    skipper_last_name: str = Field(description="skipper last name")
    length: float = Field(description="boat length")
    width: float = Field(description="boat width")
    mast_height: float = Field(description="boat mast height")
    upwind_sail_area: float = Field(description="boat upwind sail area")
    downwind_sail_area: float = Field(description="boat downwind sail area")
    gender: int = Field(description="skipper gender")
    nationality: str = Field(description="skipper nationality")
    age: int = Field(description="skipper age")
    n_participations: int = Field(description="number of participations of the skipper")
    foil: int = Field(description="whether the boat has a foil (1) or not (0)")
    year: int = Field(description="boat year of construction")
