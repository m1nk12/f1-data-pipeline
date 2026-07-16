import pandas as pd
from pydantic import BaseModel, field_validator, model_validator
from datetime import timedelta
import datetime

class Driver(BaseModel):
    driver_id: str
    given_name: str
    family_name: str
    code: str | None = None
    nationality: str | None = None
    dob: datetime.date | None = None

    @field_validator("code")
    @classmethod
    def uppercase_code(cls, value):
        if value is None:
            return value
        return value.upper()
    
class Constructor(BaseModel):
    constructorId: str
    name: str
    nationality: str
    @field_validator("name")
    @classmethod
    def snake_case(cls, value):
        string = value.split()
        res = ""
        for idx in range(0, len(string)):
            res += string[idx]
            if(idx != len(string) - 1):
                res += '_'
        return res
    
class Race(BaseModel):
    season: int
    round: int
    name: str
    date: datetime.date
    time: datetime.time
    @field_validator("name")
    @classmethod
    def snake_case(cls, value):
        string = value.split()
        res = ""

        for idx in range(0, len(string) - 1):
            res += string[idx]
            if(idx != len(string) - 1):
                res += "_"
        return res
    @model_validator(mode = "after")
    def vietnam_time(self):
        utc = datetime.datetime.combine(self.date, self.time)

        vietnam_tz = utc + timedelta(hours = 7)

        self.date = vietnam_tz.date()
        self.time = vietnam_tz.time()

        return self