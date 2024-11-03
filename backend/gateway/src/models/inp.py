from pydantic import BaseModel, EmailStr


class Credentials(BaseModel):
    email: EmailStr
    password: str


class UserForm(BaseModel):
    credentials: Credentials
    name: str
