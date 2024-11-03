from typing import Any
import pickle


def to_bytes(data: Any) -> bytes:
    return pickle.dumps(data)


def from_bytes(data_bytes: bytes) -> Any:
    return pickle.loads(data_bytes)
