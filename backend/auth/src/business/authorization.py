from datetime import datetime, timedelta
from werkzeug.exceptions import Unauthorized
from src.common.encryption import Token
from . import state
from .authentication import Authenticator

TOKEN_TTL = 60 * 60 * 24
TOKEN_TYPE = "Bearer"
REFRESH_DURATION = TOKEN_TTL * 30


class Authorizer:
    def __generate_tokens(self, credential: dict) -> dict:
        now = datetime.now()
        expiration_date = now + timedelta(seconds=TOKEN_TTL)
        token = Token(
            {
                "credentials": credential,
                "iat": int(now.timestamp()),
                "exp": int(expiration_date.timestamp()),
            }
        )
        access_token = token.jwt_encode(type="access")
        refresh_token = token.jwt_encode(type="refresh")
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": TOKEN_TTL,
            "token_type": TOKEN_TYPE,
        }
        return tokens

    def login(self, email: str, password: str) -> dict:
        user = Authenticator().validate(
            by="email",
            value=email,
            password=password,
        )
        tokens = self.__generate_tokens(
            credential={
                "user_id": user["id"],
                "roles": user["roles"],
            }
        )
        state.TokenData(user["id"]).set_value(tokens)
        return tokens

    def logout(self, user_id: int):
        user = Authenticator().validate(
            by="id",
            value=user_id,
        )
        state.TokenData(user_id).delete()

    def refresh(self, token: Token) -> dict:
        refresh_data = token.get_refresh()
        user_id = refresh_data["credentials"]["user_id"]
        user = Authenticator().validate(
            by="id",
            value=user_id,
        )
        tokens = self.__generate_tokens(
            credential={
                "user_id": user["id"],
                "role": user["roles"],
            }
        )
        state.TokenData(user["id"]).set_value(tokens)
        return tokens

    def validate(self, token: Token) -> dict:
        access_data = token.get_access()
        user_id = access_data["credentials"]["user_id"]
        roles = access_data["credentials"]["roles"]
        tokens = state.TokenData(user_id).get_value()
        if not tokens:
            raise Unauthorized("Invalid Access Token")
        return tokens, user_id, roles
