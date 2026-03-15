from typing import Literal

from pydantic import BaseModel


class SeedsByCategory(BaseModel):
    fruits: list[str]
    veggies: list[str]
    herbs: list[str]
    flowers: list[str]


class Container(BaseModel):
    type: str
    size: str
    depth: str


class PlantInGroup(BaseModel):
    name: str
    category: Literal["fruits", "veggies", "herbs", "flowers"]
    water_needs: str = ""


class PlantGroup(BaseModel):
    name: str
    plants: list[PlantInGroup]
    container: Container
    reason: str
    placement: str


class BloomSchedule(BaseModel):
    spring: list[str]
    summer: list[str]
    fall: list[str]


class GardenPlanResponse(BaseModel):
    plant_groups: list[PlantGroup]
    aesthetic_tips: list[str]
    bloom_schedule: BloomSchedule
