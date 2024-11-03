import re, bcrypt, uuid
from werkzeug.exceptions import Forbidden
from cryptography.fernet import Fernet
from jose import jwt, ExpiredSignatureError
from src.settings import SIGNING_KEY, PASSWORD_SALT, SYSTEM_ENCRYPT_KEY
from werkzeug.exceptions import Unauthorized, Forbidden

symmetric_cypher = Fernet(SYSTEM_ENCRYPT_KEY)
ALGORITHM = "HS256"


class Password(str):
    def __init__(self, password: str):
        self.unhashed = password
        self.hashed = self.hash()

    def hash(self):
        hashed_pass = bcrypt.hashpw(self.unhashed.encode(), PASSWORD_SALT.encode())
        return hashed_pass.decode()

    def __eq__(self, hashed_password):
        if isinstance(hashed_password, str):
            return self.hashed == hashed_password
        elif isinstance(hashed_password, Password):
            return self.hashed == hashed_password.hashed
        return NotImplemented

    def __str__(self):
        return self.hashed

    def __repr__(self):
        return self.hashed


class Token:
    def __init__(self, value):
        self.value = value

    def symmetric_decrypt(self):
        value = eval(symmetric_cypher.decrypt(self.value.encode()).decode())
        if not isinstance(value, list):
            raise Unauthorized("Invalid token for symmetric decryption")
        return value[0]

    def symmetric_encrypt(self):
        return symmetric_cypher.encrypt(str(self.value).encode()).decode()

    def jwt_encode(self, type):
        data = {
            "type": type,
            "uuid": str(uuid.uuid4()),
            **self.value,
        }
        token = jwt.encode(data, SIGNING_KEY, algorithm=ALGORITHM)
        return token

    def jwt_decode(self, type):
        try:
            payload = jwt.decode(self.value, SIGNING_KEY, algorithms=[ALGORITHM])
            if payload["type"] != type:
                raise Forbidden("Incompatible token type")
            return payload
        except ExpiredSignatureError:
            raise Unauthorized(f"{type} expired")
        except Exception:
            raise Unauthorized("Generic error in token parser")

    def get_refresh(self):
        return self.jwt_decode("refresh")

    def get_access(self):
        return self.jwt_decode("access")
