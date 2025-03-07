from abc import ABC, abstractmethod
from typing import Dict, Any


class Transformer(ABC):

    @abstractmethod
    def transform(self, data: Dict[str, Any]) -> Any:
        pass