import datetime
import sqlalchemy
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase


class Appointment(SqlAlchemyBase):
    __tablename__ = 'appointment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_comment = sqlalchemy.Column(sqlalchemy.Text)
    org_data = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    org_time = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    org_comment = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    data_create = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    status = sqlalchemy.Column(sqlalchemy.Text)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    org_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("organization.id"))
    org_user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)

    users = orm.relationship('Users', backref="appointment")
    organization = orm.relationship('Organization', backref="appointment")
