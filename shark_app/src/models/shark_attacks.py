import uuid
from typing import Optional

from dotenv import dotenv_values
from pydantic import BaseModel, Field, validator

config = dotenv_values(".env")


class SharkAttacks(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    month: str
    country: str
    activity: str
    injuries: str
    type: str

    @validator("country")
    def country_must_be_in_countries(cls, country):
        if country.upper() not in config["countries"]:
            raise ValueError(f'Genre must be in {config["countries"]}')
        return country

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "month": "Sep",
                "country": "SOUTH AFRICA",
                "activity": "Swimming",
                "injuries": "Lasceration",
                "type": "Unprovoked",
            }
        }


class UpdateSharkAttacks(BaseModel):
    month: Optional[str]
    country: Optional[str]
    activity: Optional[str]
    injuries: Optional[str]
    type: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "month": "Sep",
                "country": "SOUTH AFRICA",
                "activity": "Swimming",
                "injuries": "Lasceration",
                "type": "Unprovoked",
            }
        }
