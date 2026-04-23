from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    home_address = Column(String, nullable=False)

    active = Column(Boolean, nullable=False, default=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    due_date = Column(DateTime, nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)
