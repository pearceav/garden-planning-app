from pydantic import BaseModel


class GardenPreferences(BaseModel):
    yard_width: int = 20
    yard_depth: int = 26
    sun_exposure: str = "full sun"
    bed_types: list[str] = ["Wood Raised Bed", "Metal Raised Bed"]


class GardenPlanRequest(BaseModel):
    selected_seeds: list[str]
    preferences: GardenPreferences = GardenPreferences()
