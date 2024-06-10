import argparse
import zipfile

from app.data_base.db import MySQLDB
from app.data_base.models import Base, User
from app.data_base.orm import ORM
from app.parser import UserFileParser


class Terminal:
    def __init__(self):
        self.mysql_db = MySQLDB(Base)
        self.orm = ORM(db=self.mysql_db)
        self.__args = self.__create_arg_parse()

    def __create_arg_parse(self):
        parser = argparse.ArgumentParser(
            description='document parser')
        subparsers = parser.add_subparsers(dest='command')
        save_parser = subparsers.add_parser('save', help='save file')
        save_parser.add_argument('file_name', type=str, help='file_name.csv')

        get_parser = subparsers.add_parser('get', help='get data')
        get_parser.add_argument('file_name', type=str, help='file_name for result')
        args = parser.parse_args()
        return args

    def __get(self, file_name: str):
        print("get")
        total_record = self.orm.get_total_record()
        non_unique_phone_number = self.orm.get_non_unique_record_by_field(
            User.phone_number)
        count_people_by_birth_date = self.orm.get_count_people_by_birth_date()
        count_namesakes = self.orm.count_namesakes()

        data = {"total_record": total_record,
                "non_unique_phone_number": non_unique_phone_number,
                "count_people_by_birth_date": count_people_by_birth_date,
                "count_namesakes": count_namesakes
                }

        with zipfile.ZipFile(f"{file_name}.zip", 'w') as zip_file:
            zip_file.writestr('dictionary.json', str(data))
        print("successfully")

    def __save(self, file_name):
        print("save")
        user_file_parser = UserFileParser(file_path=file_name)
        users_data = user_file_parser.get_file_data()
        self.mysql_db.create_table()
        self.orm.bulk_save(users_data=users_data)
        print("successfully")

    def run(self):
        if self.__args.command == 'save':
            self.__save(self.__args.file_name)
        elif self.__args.command == 'get':
            self.__get(self.__args.file_name)
