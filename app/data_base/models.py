from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Text, Date, BigInteger
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


Base = declarative_base()


class PhoneNumber(Base):
    __tablename__ = "phone_number"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    number: Mapped[int] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="phone_number")

    def __repr__(self):
        return f"id: {id}, user_id: {self.user_id}, number: {self.number}"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    first_name: Mapped[str] = mapped_column(String(30).with_variant(VARCHAR(30, charset="utf8"), 'mysql'), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30).with_variant(VARCHAR(30, charset="utf8"), 'mysql'), nullable=False)
    patronymic_name: Mapped[str] = mapped_column(String(30).with_variant(VARCHAR(30, charset="utf8"), 'mysql'), nullable=False)
    birth_date:  Mapped[Date] = mapped_column(Date)
    other_data: Mapped[Text] = mapped_column(Text)

    phone_number = relationship("PhoneNumber", uselist=False, back_populates="user", cascade='save-update, merge, delete')

    def __repr__(self):
        return f"id: {self.id}, name: {self.last_name} {self.first_name} {self.patronymic_name}"