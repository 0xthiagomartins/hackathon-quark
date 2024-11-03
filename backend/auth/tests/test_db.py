import pytest
from src.db.controllers import (
    ctrl_user,
    ctrl_role,
    ctrl_permission,
    ctrl_role_permission,
)
from src.db import engine, SQLModel
from src.common.encryption import Password


@pytest.fixture(scope="session")
def engine_fixture():
    yield
    engine.dispose()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def create_role():
    def _create_role(name, description=""):
        role = {"name": name, "description": description}
        created_role = ctrl_role.create(data=role, returns_object=True)
        return created_role

    return _create_role


@pytest.fixture
def create_permission():
    def _create_permission(name, description=""):
        permission = {"name": name, "description": description}
        created_permission = ctrl_permission.create(
            data=permission, returns_object=True
        )
        return created_permission

    return _create_permission


@pytest.fixture
def create_user():
    def _create_user(email, password, verified=False):
        hashed_password = Password(password).hashed
        user = {"email": email, "password": hashed_password, "verified": verified}
        created_user = ctrl_user.create(data=user, returns_object=True)
        return created_user

    return _create_user


def test_create_user(create_user):
    user = create_user(email="testuser@example.com", password="TestPass123")
    assert user["id"] is not None
    assert user["email"] == "testuser@example.com"


def test_read_user(create_user):
    user = create_user(email="readuser@example.com", password="ReadPass123")
    fetched_user = ctrl_user.get(by="id", value=user["id"])
    assert fetched_user is not None
    assert fetched_user["email"] == "readuser@example.com"


def test_update_user(create_user):
    user = create_user(email="updateuser@example.com", password="UpdatePass123")
    updated_email = "updateduser@example.com"
    ctrl_user.update(
        by="id", value=user["id"], data={"email": updated_email}, returns_object=True
    )
    updated_user = ctrl_user.get(by="id", value=user["id"])
    assert updated_user["email"] == updated_email


def test_delete_user(create_user):
    user = create_user(email="deleteuser@example.com", password="DeletePass123")
    ctrl_user.delete(by="id", value=user["id"])
    deleted_user = ctrl_user.get(by="id", value=user["id"])
    assert not deleted_user


def test_create_role(create_role):
    role = create_role(name="TEST_ROLE", description="A role for testing.")
    assert role["id"] is not None
    assert role["name"] == "TEST_ROLE"


def test_create_permission(create_permission):
    permission = create_permission(
        name="TEST_PERMISSION", description="A permission for testing."
    )
    assert permission["id"] is not None
    assert permission["name"] == "TEST_PERMISSION"


def test_assign_permission_to_role(create_role, create_permission):
    role = create_role(name="ASSIGN_ROLE", description="Role to assign permissions.")
    permission = create_permission(
        name="ASSIGN_PERMISSION", description="Permission to assign."
    )
    role_permission = {"role_id": role["id"], "permission_id": permission["id"]}
    created_role_permission = ctrl_role_permission.create(
        data=role_permission, returns_object=True
    )
    assert created_role_permission["id"] is not None
    assert created_role_permission["role_id"] == role["id"]
    assert created_role_permission["permission_id"] == permission["id"]


def test_delete_permission_from_role(create_role, create_permission):
    role = create_role(name="REMOVE_ROLE", description="Role to remove permissions.")
    permission = create_permission(
        name="REMOVE_PERMISSION", description="Permission to remove."
    )
    role_permission = {"role_id": role["id"], "permission_id": permission["id"]}
    created_role_permission = ctrl_role_permission.create(
        data=role_permission, returns_object=True
    )
    assert created_role_permission["id"] is not None

    # Delete the role_permission
    ctrl_role_permission.delete(by="id", value=created_role_permission["id"])
    deleted_role_permission = ctrl_role_permission.get(
        by="id", value=created_role_permission["id"]
    )
    assert deleted_role_permission == {}
