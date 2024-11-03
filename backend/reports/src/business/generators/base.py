from dataclasses import dataclass
from typing import Any


@dataclass
class BaseConfig:
    business_name: str
    session_data: str
    data_set: Any
