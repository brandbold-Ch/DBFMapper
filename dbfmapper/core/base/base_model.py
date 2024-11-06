from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):

    @abstractmethod
    def get(self, **kwargs) -> Any:
        return

    @abstractmethod
    def get_all(self, easy_view: bool, **kwargs) -> list:
        return []
