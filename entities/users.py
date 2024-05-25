from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlalchemy import String
from sqlmodel import Field

from configs import EntityBase


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"


class UserEntity(EntityBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    openid: str = Field(default=None, index=True)
    tenantid: str = Field(default=None, nullable=True, index=True)
    username: str = Field(max_length=25, sa_type=String(50))
    email: str | None = Field(default=None, unique=True)
    password: str = Field(nullable=False)
    role: Role = Field(default=Role.USER)

    pkg_name: str = Field(default=None, index=True)
    platform: str = Field(default='weapp', index=True)

    avatar: str = None
    user_desc: str = None
    is_enabled: bool = True
    login_time: int = None
    session_key: str = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)