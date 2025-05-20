import asyncpg
import config
import atexit
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime, func, ForeignKey, UUID
from sqlalchemy.orm import mapped_column, Mapped
from custum_types import ROLE
import uuid


engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    
    
    @property
    def id_dict(self):
        return {"id": self.id}


class Token(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, server_default=func.gen_random_uuid()
    )
    creation_token: Mapped[datetime.datetime] = mapped_column(
         DateTime, server_default=func.now()    
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates="tokens", )


    @property
    def dict(self):
        return {"token": self.token}


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    tokens: Mapped[list[Token]] = relationship(Token, lazy="joined", back_populates="user", cascade="all, delete-orphan")
    Advertisments: Mapped[list["Advertisment"]] = relationship("Advertisment", lazy="joined", back_populates="user", cascade="all, delete-orphan")
    role: Mapped[ROLE] = mapped_column(String, default="user")


    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "Advertisments": self.Advertisments,
        }


class Advertisment(Base):
    __tablename__ = "advertisments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Title: Mapped[str] = mapped_column(String, nullable=False)
    Price: Mapped[int] = mapped_column(Integer, nullable=False)
    Description: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates="Advertisments")
    Create_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    

    @property
    def dict(self):
        return {
            "id": self.id,
            "Title": self.Title,
            "Price": self.Price,
            "Description": self.Description,
            "name": self.user.name,
            "Create_time": self.Create_time.isoformat(),
            "user_id": self.user_id
        }


ORM_OBJ = Advertisment | User | Token
ORM_CLS = type[Advertisment] | type[User] | type[Token]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()


