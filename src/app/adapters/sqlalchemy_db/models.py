from sqlalchemy import Integer, String, Column, MetaData, Table, Boolean, true
from sqlalchemy.orm import registry

from app.application.schemas import User

metadata_obj = MetaData()
mapper_registry = registry()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String()),
    Column("email", String()),
    Column('hashed_password', String()),
    Column("is_active", Boolean(), default=True),
)

mapper_registry.map_imperatively(User, user)
