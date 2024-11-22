import json
import pickle
import uuid
from typing import Literal, Optional, Union

from bson import ObjectId
from dotenv import dotenv_values
from pydantic import BaseModel, Field, validator

config = dotenv_values(".env")


class SharkAttackPred(BaseModel):
    """
    Model for data used for prediction only
    """

    month: str
    country: str
    activity: str
    injuries: str
    type: str

    @validator("country")
    def country_must_be_in_countries(cls, country):
        if country.upper() not in json.loads(config["country"]):
            raise ValueError(f'Country must be in {config["country"]}')
        return country

    @validator("month")
    def month_must_be_in_months(cls, month):
        if month.lower() not in [col.lower() for col in json.loads(config["month"])]:
            print([col.lower() for col in config["month"]])
            raise ValueError(f'Month must be in {config["month"]}')
        return month

    @validator("type")
    def type_must_be_in_types(cls, type):
        if type.lower() not in [col.lower() for col in json.loads(config["type"])]:
            raise ValueError(f'Typpe must be in {config["type"]}')
        return type

    @validator("injuries")
    def injury_must_be_in_injurys(cls, injuries):
        if injuries.lower() not in [
            col.lower() for col in json.loads(config["injuries"])
        ]:
            raise ValueError(f'Injury must be in {config["injuries"]}')
        return injuries

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


class SharkAttacks(SharkAttackPred):
    """
    Model used for adding and retrieving data from the database
    """

    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    month: str
    country: str
    activity: str
    injuries: str
    type: str
    year: int
    occurence_per_month: float

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "month": "Sep",
                "country": "SOUTH AFRICA",
                "activity": "Swimming",
                "injuries": "Lasceration",
                "type": "Unprovoked",
                "year": 1998,
                "occurence_per_month": 0.5,
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
                "year": 1998,
                "occurence_per_month": 0.5,
            }
        }


class AttributePred(BaseModel):
    """
    Model just for aggregating data
    """

    attribute: Union[Literal["Country", "Activity", "Type", "Year"]]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "attribute": "Country",
            }
        }
