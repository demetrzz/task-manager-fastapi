from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata_obj = Base.metadata


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
