from abc import ABC, abstractmethod


class IConfigLoader(ABC):
    @abstractmethod
    def load(self, path: str):
        pass
