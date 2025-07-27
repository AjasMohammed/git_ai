from pydantic import BaseModel, Field


class SheetData(BaseModel):
    task: str = Field(description="Short description of the task.")
    notes: str = Field(description="Detailed notes or context on the task.")
