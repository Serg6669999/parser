from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import (MYSQL_DATABASE, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT)


class MySQLDB:
    def __init__(self, base: declarative_base):
        self.base = base

    def __create_engine(self):
        url = f"mysql+mysqldb://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        return create_engine(url, echo=False)

    def create_session(self):
        engine = self.__create_engine()
        Session = sessionmaker(bind=engine)
        return Session()

    def create_table(self):
        engine = self.__create_engine()
        self.base.metadata.create_all(engine)
