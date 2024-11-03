from pydantic import BaseModel
from datetime import date, datetime
from typing import Generic, Literal, Optional, TypeVar


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    data_set: list[T]
    per_page: int
    total_pages: int
    total_data: int
    previous: int | None
    current: int
    next: int | None


class User(BaseModel):
    email: str
    name: str


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    timestamp: float
