from nameko.rpc import rpc
from .common.encryption import Password, Token
from .business.authorization import Authorizer, Authenticator
from nameko.dependency_providers import DependencyProvider


class SessionDataDependency(DependencyProvider):

    def get_dependency(self, worker_ctx):
        try:
            session_data = worker_ctx.data["session_data"]
        except KeyError:
            session_data = None
        except AttributeError:
            session_data = None
        return session_data


class AuthRPC:
    """
    Authentication and Authorization service
    """

    name = "auth"
    session_data: dict = SessionDataDependency()

    @rpc
    def login(self, email: str, password: Password):
        password = Password(password)
        return Authorizer().login(email, password)

    @rpc
    def validate_token(self, access_token: str):
        access_token = Token(access_token)
        return Authorizer().validate(access_token)

    @rpc
    def refresh_token(self, refresh_token: str):
        refresh_token = Token(refresh_token)
        return Authorizer().refresh(refresh_token)

    @rpc
    def logout(self):
        return Authorizer().logout(self.session_data["user_id"])

    @rpc
    def register_user(
        self,
        role_id: int,
        credentials: dict,
        name: str,
    ):
        password = Password(credentials["password"])
        return Authenticator(self.session_data).register(
            role_id,
            credentials["email"],
            password,
            name,
        )
