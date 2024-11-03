from sqlmodel import Field, Relationship
from sqlmodel_controller import BaseID
from datetime import date


class UserRole(BaseID, table=True):
    __tablename__ = "user_roles"

    user_id: int = Field(default=None, foreign_key="users.id")
    role_id: int = Field(default=None, foreign_key="roles.id")


class User(BaseID, table=True):
    __tablename__ = "users"

    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=True)
    password: str = Field(nullable=False)
    verified: bool = Field(default=False)
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRole)


class RolePermission(BaseID, table=True):
    __tablename__ = "role_permissions"

    role_id: int = Field(default=None, foreign_key="roles.id")
    permission_id: int = Field(default=None, foreign_key="permissions.id")


class Role(BaseID, table=True):
    __tablename__ = "roles"

    name: str = Field(
        unique=True, nullable=False
    )  # e.g., 'ADMIN', 'TRAINEE', 'ASSESSOR'
    description: str = Field(default="", nullable=True)
    permissions: list["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRole)


class Permission(BaseID, table=True):
    __tablename__ = "permissions"

    name: str = Field(
        unique=True, nullable=False
    )  # e.g., 'read', 'edit', 'delete', 'approve'
    description: str = Field(default="", nullable=True)
    roles: list["Role"] = Relationship(
        back_populates="permissions", link_model=RolePermission
    )


class Client(BaseID, table=True):
    __tablename__ = "clients"

    assessor_id: int = Field(default=None, foreign_key="users.id")
    name: str = Field(nullable=False)
    account: str = Field(nullable=False)

    approved: bool = Field(default=False)


class Operation(BaseID, table=True):
    __tablename__ = "operations"

    liq_date: date
    quote_id: str = Field(nullable=False)
    client_id: int = Field(foreign_key="clients.id")
    structure: str = Field(nullable=False)
    asset: str = Field(nullable=False)
    entry_price: float = Field(nullable=False)
    amount: int = Field(default=0)
    strike_percent: float = Field(nullable=False)
    barrier_percent: float = Field(nullable=False)
    status: str = Field(nullable=False)

    approved: bool = Field(default=False, nullable=False)
