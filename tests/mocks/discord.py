from dataclasses import dataclass
from typing import Optional


@dataclass
class MockGuild:
    id: int


@dataclass
class MockMessage:
    id: int
    guild: Optional[MockGuild] = None
