import uuid
from typing import Optional
from pydantic import BaseModel, Field


class GameRecord(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    teamName: str = Field(...)
    dateOfGame: str = Field(...)
    escapeTime: int = Field(...)
    hintsUsed: int = Field(...)
    score: int = Field(...)
    timeGameComplete: str = Field(...)
    timeInRoom: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "dateOfGame": "05/05/2024",
                "escapeTime": 2710,
                "hintsUsed": 3,
                "score": 271000,
                "timeStamp": "00:10:34",
                "timeInRoom": "3:15"
            }
        }


class GameRecordUpdate(BaseModel):
    teamName: Optional[str] = None
    dateOfGame: Optional[str] = None
    escapeTime: Optional[int] = None
    hintsUsed: Optional[int] = None
    score: Optional[int] = None
    timeGameComplete: Optional[str] = None
    timeInRoom: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "dateOfGame": "05/05/2024",
                "escapeTime": 2710,
                "hintsUsed": 3,
                "score": 271000,
                "timeStamp": "00:10:34",
                "timeInRoom": "3:15"
            }
        }
