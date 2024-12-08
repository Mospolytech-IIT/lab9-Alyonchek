from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    user_id: int


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
