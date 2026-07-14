import pandas as pd
from pydantic import BaseModel, field_validator
from datetime import date

class Driver(BaseModel):
    driver_id: str
    given_name: str
    family_name: str
    code: str | None = None
    nationality: str | None = None
    dob: date | None = None

    @field_validator("code")
    @classmethod
    def uppercase_code(cls, value):
        if value is None:
            return value
        return value.upper()