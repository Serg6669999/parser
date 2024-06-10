from typing import List

from sqlalchemy import distinct, func

from app.data_base.db import MySQLDB
from app.data_base.models import PhoneNumber, User
from app.parser import UserData


class ORM:
    def __init__(self, db: MySQLDB):
        self.db = db

    def get_total_record(self) -> int:
        session = self.db.create_session()
        return session.query(User.id).count()

    def get_unique_record_list(self, model_field) -> List[str]:
        session = self.db.create_session()
        return session.query(distinct(model_field)).all()

    def get_non_unique_record_by_field(self, model_field):
        session = self.db.create_session()
        subquery = session.query(PhoneNumber.number.label('cnt')) \
            .group_by(PhoneNumber.number) \
            .having(func.count(PhoneNumber.number) > 1) \
            .subquery()

        return session.query(func.count(subquery.c.cnt)).scalar()

    def get_count_people_by_birth_date(self):
        session = self.db.create_session()
        year = func.year(User.birth_date)
        result = session.query(year, func.count(User.id)).group_by(year).all()

        return [{"year": year, "people_count": peaple_count} for year, peaple_count in result]

    def count_namesakes(self):
        session = self.db.create_session()
        return session.query(User.last_name).group_by(User.last_name).\
            having(func.count(User.last_name) > 1).count()

    def drop_rows(self, model):
        session = self.db.create_session()
        session.query(model).delete()

    def bulk_save(self, users_data: List[UserData], batch_size: int = 100):
        """
        :param batch_size: The batch_size parameter controls how many objects
                           are created in a single query
        """
        user_data_list = []
        for i, user_data in enumerate(users_data):
            if i % batch_size != 0:
                user_data_list.append(user_data)
            else:
                self.__bulk_save(user_data_list)
                user_data_list.clear()

    def __bulk_save(self, users_data: List[UserData]):

        users_list = []
        phone_number_list = []
        for user_data in users_data:
            user = User(first_name=user_data.first_name,
                        last_name=user_data.last_name,
                        patronymic_name=user_data.patronymic_name,
                        birth_date=user_data.birth_date,
                        other_data=user_data.other_data
                        )
            phone_number = PhoneNumber(number=user_data.phone_number,
                                       user=user
                                      )
            users_list.append(user)
            phone_number_list.append(phone_number)
        session = self.db.create_session()
        session.add_all(users_list)
        session.add_all(phone_number_list)
        session.commit()
