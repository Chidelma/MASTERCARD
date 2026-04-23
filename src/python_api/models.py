import datetime

from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    home_address: constr(min_length=1)


class UserResponse(BaseModel):
    class Config:
        from_attributes = True

    id: int
    first_name: str
    last_name: str
    home_address: str


class CreateTask(BaseModel):
    name: constr(min_length=1)
    description: constr(min_length=1)

    due_date: datetime.datetime | None = None

class TaskResponse(BaseModel):
    class Config:
        from_attributes = True

    id: int
    name: str
    description: str
    due_date: datetime.datetime | None = None
    deleted: bool


class TaskRec(TaskResponse):
    user_id: int