from fastapi import FastAPI, HTTPException
from datetime import datetime 
from schema import *
import crud
from lifespan import lifespan
from models import Session
from dependancy import SessionDependancy, TokenDependancy
import models
from sqlalchemy import select
from constant import *
import auth
from sqlalchemy.orm import selectinload


app = FastAPI(
    title="BUY/SELL Advertisments API",
    description="API for BUY/SELL Advertisments",
    version="1.0.0",
    lifespan=lifespan
)   


@app.post(
    "/advertisments/",
    tags=["create advertisments"],
    response_model=CreateAdvResponse
)
async def create_Advertisment(request:createAdvRequest, session: SessionDependancy, token: TokenDependancy):
    Adv_dict = request.model_dump(exclude_unset=True)
    Adv_orm_obj = models.Advertisment(user_id=token.user_id, **Adv_dict)
    await crud.add_item(session, Adv_orm_obj)
    return Adv_orm_obj.id_dict


@app.get(
    "/advertisments/{Adv_id}",
    tags=["get advertisments"],
    response_model=GetAdvResponse
)
async def get_Advertisment(Adv_id:int, session: SessionDependancy):
    Adv_orm_obj = await crud.get_item_by_id(session, models.Advertisment, Adv_id)
    return Adv_orm_obj.dict


@app.get(
    "/advertisments/",
    tags=["search advertisments"],
    response_model=SearchAdvResponse
)
async def search_Advertisment(session: SessionDependancy, Title: str):
    query = (
        select(models.Advertisment)
        .where(models.Advertisment.Title.ilike(f"%{Title}%"))
        .limit(10000)
        .options(selectinload(models.Advertisment.user))
    )
    Advs = (await session.scalars(query)).unique().all()
    return {"results": [Adv.dict for Adv in Advs]}


@app.patch(
    "/advertisments/{response_model.id}",
    tags=["update advertisments"],
    response_model=UpdateAdvResponse
)
async def update_Advertisment(Adv_id:int, Adv_data: UpdateAdvRequest, session: SessionDependancy, token: TokenDependancy):
    Adv_dict = Adv_data.model_dump(exclude_unset=True)
    Adv_orm_obj = await crud.get_item_by_id(session, models.Advertisment, Adv_id)
    if Adv_orm_obj.user_id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")
    for field, value in Adv_dict.items():
        setattr(Adv_orm_obj, field, value)
    await crud.add_item(session, Adv_orm_obj)
    return SUCCCESS_RESPONSE    


@app.delete(
    "/advertisments/{Adv_id}",
    tags=["delete advertisments"],
    response_model=DeleteAdvResponse
)
async def delete_Advertisment(Adv_id:int, session: SessionDependancy, token: TokenDependancy):
    Adv_orm_obj = await crud.get_item_by_id(session, models.Advertisment, Adv_id)
    if Adv_orm_obj.user_id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")
    await crud.delete_item(session, Adv_orm_obj)
    return SUCCCESS_RESPONSE


@app.post(
    "/login",
    response_model=LoginResponse,
    tags=["login"],
)
async def login(login_data: LoginRequest, session: SessionDependancy):
    query = select(models.User).where(models.User.name == login_data.name)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not auth.check_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict


@app.post(
    "/user",
    response_model=CreateUserResponse,
    tags=["create user"],
)
async def create_user(user_data: CreateUserRequest, session: SessionDependancy):
    user_data_dict = user_data.model_dump()
    user_data_dict["password"] = auth.hash_password(user_data_dict["password"])
    user = models.User(**user_data_dict)
    await crud.add_item(session, user)
    return user.id_dict


@app.get(
    "/user/{User_id}",
    tags=["get user"],
    response_model=GetUserResponse,
)
async def get_User(User_id:int, session: SessionDependancy):
    User_orm_obj = await crud.get_item_by_id(session, models.User, User_id)
    return User_orm_obj.dict

@app.patch(
    "/user/{User_id}",
    tags=["update user"],
    response_model=UpdateUserResponse
)
async def update_User(
    User_id:int,
    User_data: UpdateUserRequest,
    session: SessionDependancy,
    token: TokenDependancy
    ):
    User_orm_obj = await crud.get_item_by_id(session, models.User, User_id)
    if User_orm_obj.id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")
    User_dict = User_data.model_dump(exclude_unset=True)
    User_dict["password"] = auth.hash_password(User_dict["password"])
    for field, value in User_dict.items():
        setattr(User_orm_obj, field, value)
    await crud.add_item(session, User_orm_obj)
    return SUCCCESS_RESPONSE


@app.delete(
    "/user/{User_id}",
    tags=["delete user"],
    response_model=DeleteUserResponse
)
async def delete_User(User_id:int, session: SessionDependancy, token: TokenDependancy):
    User_orm_obj = await crud.get_item_by_id(session, models.User, User_id)
    if User_orm_obj.id != token.user_id and token.user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough rights")
    await crud.delete_item(session, User_orm_obj)
    return SUCCCESS_RESPONSE