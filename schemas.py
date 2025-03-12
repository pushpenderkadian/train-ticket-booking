from pydantic import BaseModel,     Field, ValidationError, field_validator
from pydantic_core.core_schema import ValidationInfo
from typing import Optional



class ChildRequest(BaseModel):
    name: str
    age: int=Field(..., gt=0, lt=5)
    gender: str

class PassengerRequest(BaseModel):
    name: str
    age: int=Field(..., gt=5)
    gender: str
    with_infant: bool
    child: Optional[ChildRequest]=None

    @field_validator("child", mode="before")
    @classmethod
    def validate_child(cls, child, values:ValidationInfo):
        if values.data.get("with_infant") and child is None:
            raise ValueError("Child details must be provided when with_infant is True")
        return child