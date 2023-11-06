from pydantic import BaseModel


class TaskBase(BaseModel):
    id: int
    title: str
    completed: bool
    author_id: int
    assignee_id: int

    class Config:
        from_attributes = True


class TaskSchemaAdd(BaseModel):
    title: str
    author_id: int
    assignee_id: int
