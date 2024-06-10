import csv
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Union

from app.buisness_rulse import DataStructure, FileParser


@dataclass
class UserData(DataStructure):
    phone_number: int
    first_name: str
    last_name: str
    patronymic_name: str
    birth_date: datetime.strptime
    other_data: str


class UserFileParser(FileParser, ABC):
    def __init__(self, file_path: str):
        self.__file_data = self.get_file_data()
        super().__init__(file_path)

    def __check_valid_phone_number(self, phone_number: str) -> Union[int, None]:
        for char in phone_number:
            if char.isdigit() is False:
                print("Invalid phone number", phone_number)
                return None
        return int(phone_number)

    def get_file_data(self) -> Iterator[UserData]:
        with open(self.file_path, "r", encoding="windows-1251",
                  newline='') as file:
            rows = csv.reader(file, delimiter=';')
            for row in rows:
                yield UserData(
                    phone_number=self.__check_valid_phone_number(row[0]),
                    first_name=row[4].split(" ")[1],
                    last_name=row[4].split(" ")[0],
                    patronymic_name=row[4].split(" ")[2],
                    birth_date=datetime.strptime(row[8], "%d.%m.%Y"),
                    other_data="; ".join([data for i, data in enumerate(row) if
                                          not i in [0, 4, 8]])
                )
