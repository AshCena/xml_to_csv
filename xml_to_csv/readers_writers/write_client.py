from abc import ABC, abstractmethod
from typing import List, Any


class WriteClient(ABC):
    @abstractmethod
    def write(self, data: List[Any]) -> None:
        pass