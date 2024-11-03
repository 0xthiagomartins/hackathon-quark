from src.common.in_memory import State
from datetime import datetime, timezone
from src.common.serialization import to_bytes, from_bytes

UTC = timezone.utc


class VerificationCode(State):
    __slots__ = (
        "business_id",
        "code",
    )

    def __init__(self, code: str):
        super().__init__()
        self.ttl = 5 * 60
        self.subject = "VERIFICATION_CODE"
        self.code = code
        self.business_id = "business_id"

    def set_value(self, data: dict):
        self.reset_value()
        pipe = self.connection.pipeline()
        data.update({"timestamp": datetime.now(UTC).timestamp()})
        pipe.set(str(self), to_bytes(data))
        if self.ttl:
            pipe.expire(str(self), self.ttl)
        pipe.execute()

    def get_value(self):
        value = self.connection.get(str(self))
        if value is not None:
            value = from_bytes(value)
        return value


class TokenData(State):
    __slots__ = (
        "business_id",
        "user_id",
    )

    def __init__(self, user_id: int):
        super().__init__()
        self.ttl = 60 * 60 * 24
        self.user_id = user_id
        self.business_id = "business_id"
        self.subject = "TOKEN"

    def set_value(self, data: dict):
        data.update({"timestamp": datetime.now(UTC).timestamp()})
        super().set_value(data)

    def get_value(self):
        value = super().get_value()
        return value
