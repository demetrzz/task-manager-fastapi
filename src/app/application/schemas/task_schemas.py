from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    author_id: int
    assignee_id: int


class TaskAdd(BaseModel):
    title: str
    assignee_id: int


class TaskCompletion(BaseModel):
    completed: bool
