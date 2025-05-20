from pydantic import BaseModel
import datetime
from typing import Literal
from constant import SUCCCESS_RESPONSE
import uuid


class IdResponse(BaseModel):
    id: int


class SuccessResponse(BaseModel):
    status: Literal["success"]


class createAdvRequest(BaseModel):
    Title: str
    Price: int | None = None
    Description: str | None = None


class CreateAdvResponse(IdResponse):
    pass


class UpdateAdvResponse(SuccessResponse):
    pass


class UpdateAdvRequest(BaseModel):
    Title: str | None = None
    Price: int | None = None
    Description: str | None = None


class GetAdvResponse(BaseModel):
    id: int
    Title: str
    Price: int
    Description: str 
    name: str
    user_id: int
    Create_time: datetime.datetime


class DeleteAdvResponse(SuccessResponse):
    pass


class SearchAdvResponse(BaseModel):
    results: list[GetAdvResponse]


class BasicUserRequest(BaseModel):
    name: str
    password: str

class LoginRequest(BasicUserRequest):
    pass


class LoginResponse(BaseModel):
    token: uuid.UUID


class CreateUserRequest(BasicUserRequest):
    pass


class CreateUserResponse(IdResponse):
    pass


class GetUserResponse(BaseModel):
    id: int
    name: str


class UpdateUserRequest(BasicUserRequest):
    pass


class UpdateUserResponse(SuccessResponse):
    pass


class DeleteUserResponse(SuccessResponse):
    pass