from pydantic import BaseModel


class TaskBase(BaseModel):
    id: int
    title: str
    completed: bool
    author_id: int
    assignee_id: int

    class Config:
        from_attributes = True


class TaskAdd(BaseModel):
    title: str
    assignee_id: int


class TaskCompletion(BaseModel):
    completed: bool
