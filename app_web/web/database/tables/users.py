import sqlalchemy

from ..db_session import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    first_name = sqlalchemy.Column(sqlalchemy.Text)
    second_name = sqlalchemy.Column(sqlalchemy.Text)
    email = sqlalchemy.Column(sqlalchemy.Text)
    password = sqlalchemy.Column(sqlalchemy.Text)
    phone_number = sqlalchemy.Column(sqlalchemy.Text)
    image_path = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean)
