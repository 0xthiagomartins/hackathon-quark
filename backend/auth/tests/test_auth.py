import pytest
from src.business.authorization import Authorizer, Authenticator
from src.common.encryption import Password, Token
from src.db.controllers import ctrl_user, ctrl_role, ctrl_user_role
from src.db import engine, SQLModel


@pytest.fixture(scope="session")
def engine_fixture():
    yield
    engine.dispose()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def admin_role():
    admin_role = ctrl_role.get(by="name", value="ADMIN")
    return admin_role


@pytest.fixture()
def authenticator() -> Authenticator:
    return Authenticator()


@pytest.fixture()
def authorizer() -> Authorizer:
    return Authorizer()


def test_register(admin_role, authenticator):
    email = "testregister@example.com"
    password = "TestPass123"
    name = "Test User"
    role_id = admin_role["id"]
    user_id = authenticator.register(
        role_id=role_id,
        email=email,
        password=Password(password),
        name=name,
    )
    assert user_id is not None

    user = ctrl_user.get(by="id", value=user_id)
    assert user is not None
    assert user["email"] == email
    assert user["verified"] is True


def test_login(authorizer):
    tokens = authorizer.login(
        email="testregister@example.com",
        password=Password("TestPass123"),
    )

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "Bearer"


@pytest.fixture(name="user_id")
def test_validate_token(authorizer, tokens):
    token = Token(tokens["access_token"])
    tokens, user_id, roles = authorizer.validate(token)
    return user_id


@pytest.fixture(name="tokens")
def tokens(authorizer):
    """Test successful login."""

    tokens = authorizer.login(
        email="testregister@example.com",
        password=Password("TestPass123"),
    )

    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "Bearer"
    return tokens


"""
def test_logout(authorizer, user_id):
    authorizer.logout(user_id)
    assert True
"""
