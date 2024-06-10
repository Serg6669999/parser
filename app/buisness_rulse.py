from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Iterator


@dataclass
class DataStructure:
    pass


class FileParser(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def get_file_data(self) -> Iterator[DataStructure]:
        pass
