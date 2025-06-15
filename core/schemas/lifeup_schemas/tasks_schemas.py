from pydantic import BaseModel
import os
from typing import List, Dict, Optional


class SuccessGetRequests(BaseModel):
    data: List[Dict]

    class Config:
        json_schema_extra = {
            "example": {
                "data":
                [
                    {
                    "id": 2,
                    "iteration": 1,
                    "sprint_goal": "testing",
                    "created_at": "2024-06-24T14:00:28.310078+00:00",
                    "finished": False,
                    "finished_at": None,
                    "description": "testing2"
                    }
                ]
            }
        }


class PostRequests(BaseModel):
    sprint_name : str = "Finish backend Project"
    sprint_desc : Optional[str] = "Finish all the endpoints and tests"  


class SuccessPostRequests(BaseModel):
    response: str = "A new goal has been set. New challenge awaits!"
    data: List

    class Config:
        json_schema_extra = {
            "example": {
                "response": "A new goal has been set. New challenge awaits!",
                "data":
                [
                    {
                    "id": 2,
                    "iteration": 1,
                    "sprint_goal": "testing",
                    "created_at": "2024-06-24T14:00:28.310078+00:00",
                    "finished": False,
                    "finished_at": None,
                    "description": "testing2"
                    }
                ]
            }
        }


class PostTasksRequests(BaseModel):
    sprint_name : str = "Finish backend Project"
    sprint_desc : Optional[str] = "Finish all the endpoints and tests"
    difficulty : int = 10
    importance : int = 10


class SuccessTasksPostRequests(BaseModel):
    response: str = "A new goal has been set. New challenge awaits!"
    data: List

    class Config:
        json_schema_extra = {
            "example": {
                "response": "A new goal has been set. New challenge awaits!",
                "data":
                [
                    {
                    "id": 2,
                    "iteration": 1,
                    "sprint_goal": "testing",
                    "created_at": "2024-06-24T14:00:28.310078+00:00",
                    "finished": False,
                    "finished_at": None,
                    "description": "testing2"
                    }
                ]
            }
        }