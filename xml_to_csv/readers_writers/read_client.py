from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ReadClient(ABC):
    @abstractmethod
    def read_data(self) -> List[Dict[str, Any]]:
        pass