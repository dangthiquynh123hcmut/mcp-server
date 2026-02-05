from enum import Enum
from pydantic import BaseModel

class ItemFieldType(str, Enum):
    TEXTAREA = "textarea"
    NUMBER = "number"
    DATE = "date"
    TIME = "time"
    DATETIME = "dateTime"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    SINGLE_SELECT = "single-select"
    MULTIPLE_SELECT = "multiple-select"
    TEXT = "text"
    FILE = "file"

class GeneratedOption(BaseModel):
    label: str 
    value: str 


class LaboratoryTestItem(BaseModel):
    label: str 
    code: str 
    type: ItemFieldType 
    unit: str 
    options: list[GeneratedOption] 

class LaboratoryTestRequest(BaseModel):
    user_prompt: list[str] = None
    items: list[LaboratoryTestItem]

class LaboratoryTestResultsForm(BaseModel):
    """Response form for laboratory test results"""
    data: dict
    status: str = "success"
