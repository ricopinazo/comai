from dataclasses import dataclass
from abc import ABC

@dataclass
class Interaction(ABC):
    content: str

@dataclass
class Command(Interaction):
    pass
    # content: str

@dataclass
class Query(Interaction):
    pass
    # content: str
