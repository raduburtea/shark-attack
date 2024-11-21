import uuid
from typing import Optional

from dotenv import dotenv_values
from pydantic import BaseModel, Field, validator

config = dotenv_values(".env")


class SharkAttack(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="id")
    Month: str
    Country: str
    Activity: str
    Injuries: str
    Type: str

    @validator("Country")
    def country_must_be_in_countries(cls, country):
        if country not in config["countries"]:
            raise ValueError(f'Genre must be in {config["countries"]}')
        return country

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "Month": "Sep",
                "Country": "SOUTH AFRICA",
                "Activity": "Swimming",
                "Injuries": "Lasceration",
                "Type": "Unprovoked",
            }
        }


class UpdateSharkAttack(BaseModel):
    Month: Optional[str]
    Country: Optional[str]
    Activity: Optional[str]
    Injuries: Optional[str]
    Type: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "Month": "Sep",
                "Country": "SOUTH AFRICA",
                "Activity": "Swimming",
                "Injuries": "Lasceration",
                "Type": "Unprovoked",
            }
        }
