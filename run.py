import json
import zipfile
import sys

from app.data_base.db import MySQLDB
from app.data_base.models import Base, User
from app.data_base.orm import ORM
from app.parser import UserFileParser

if __name__ == "__main__":
    print("start")
    mysql_db = MySQLDB(Base)
    orm = ORM(db=mysql_db)


    argv = sys.argv
    arg = 0
    if len(argv):
        arg = argv[0]
    if arg:
        try:
            file_name = argv[1]
        except IndexError:
            raise("python run.py save <file_name>")

        print("save")
        user_file_parser = UserFileParser(file_path=file_name)
        users_data = user_file_parser.get_file_data()
        mysql_db.create_table()
        parser_file_name = sys.argv[1]
        orm.bulk_save(users_data=users_data)
        print("successfully")

    if arg == "get":
        print("get")
        total_record = orm.get_total_record()
        non_unique_phone_number = orm.get_non_unique_record_by_field(User.phone_number)
        count_people_by_birth_date = orm.get_count_people_by_birth_date()
        count_namesakes = orm.count_namesakes()

        data = {"total_record": total_record,
                "non_unique_phone_number": non_unique_phone_number,
                "count_people_by_birth_date": count_people_by_birth_date,
                "count_namesakes": count_namesakes
                }
        json_data = json.dumps(data).encode()
        result_file_name = "result2"

        with zipfile.ZipFile(f"{result_file_name}.zip", 'w') as zip_file:
            zip_file.writestr('dictionary.json', str(data))
        print("successfully")