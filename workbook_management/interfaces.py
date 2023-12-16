from abc import ABC, abstractmethod


class IWorkbookLoader(ABC):
    @abstractmethod
    def load(self, path: str):
        pass




