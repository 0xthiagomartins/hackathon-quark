from datetime import date
from werkzeug.exceptions import Unauthorized, Forbidden, NotFound
import string, random, math
from . import state
from src.common.encryption import Password, Token
from ..db.controllers import ctrl_user, ctrl_user_role


class Authenticator:
    def __init__(self, session_data: dict = {}):
        self.session_data = session_data

    def __get_user(self, by, value, joins=[], must_be_verified=False):
        user = ctrl_user.get(by=by, value=value, joins=joins)
        if not user:
            raise NotFound("User Not Found")
        if user["archived"] or not user["verified"] == must_be_verified:
            print(user)
            raise Forbidden("Invalid User")
        return user

    def generate_verification_code(self, data: dict):
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        verification_code = state.VerificationCode(code)
        while verification_code.exists():
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            verification_code = state.VerificationCode(code)
        verification_code.set_value(data)
        return code

    def _send_code_by_email(self, user, data={}):
        code = self.generate_verification_code(
            {"user_id": user["id"], "roles": user["roles"], **data}
        )
        """
        TODO:
        Your logic to send email

        MOCKED
        """
        return code

    def register(
        self,
        role_id: int,
        email: str,
        password: Password,
        name: str,
    ) -> int:
        user = ctrl_user.get(by="email", value=email)
        """
        assert that self.session_data.get("user_id") has admin permission
        """
        if user:
            raise Exception(f"User with email {email} already exists.")
        user_id = ctrl_user.upsert(
            by=["email"],
            value=[email],
            data={
                "email": email,
                "name": name,
                "password": password.hashed,
                "verified": True,
            },
        )
        ctrl_user_role.create(
            data={
                "user_id": user_id,
                "role_id": role_id,
            }
        )
        return user_id

    def validate(
        self,
        by,
        value,
        password: Password = None,
        must_be_verified: bool = True,
    ):
        user = self.__get_user(
            by=by,
            value=value,
            joins=["roles"],
            must_be_verified=must_be_verified,
        )
        if password:
            if not (password == user["password"]):
                raise Unauthorized("Invalid User")
        return user

    def recover_password(self, email: str):
        user = self.validate(by="email", value=email)
        code = self._send_code_by_email(user)
        return code

    def change_password(
        self,
        email: str,
        new_password: Password,
        code: str,
        expected_data: str,
    ):
        user = self.validate(by="email", value=email)
        verification_code = state.VerificationCode(code)
        if not verification_code.exists():
            raise Forbidden("Invalid Code")
        code_values = verification_code.get_value()
        if code_values["expected_data"] != expected_data:
            raise Forbidden("Invalid Expected Data")
        verification_code.delete()
        ctrl_user.update(
            by="id",
            value=user["id"],
            data={
                "password": new_password,
            },
        )

    def symmetric_encrypt_value(self, value: int):
        return Token(value).symmetric_encrypt()
