import sqlalchemy
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase


class Organization(SqlAlchemyBase):
    __tablename__ = 'organization'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text)
    about = sqlalchemy.Column(sqlalchemy.Text)
    email = sqlalchemy.Column(sqlalchemy.Text)
    phone_number = sqlalchemy.Column(sqlalchemy.Text)
    address = sqlalchemy.Column(sqlalchemy.Text)
    image_path = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    type_app_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("type_appointment.id"))

    users = orm.relationship('Users', backref="organization")
    type_appointment = orm.relationship('type_appointment', backref="organization")
