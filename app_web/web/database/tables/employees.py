import sqlalchemy
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase


class Employees(SqlAlchemyBase):
    __tablename__ = 'employees'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    org_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("organization.id"))

    users = orm.relationship('Users', backref="employees")
    organization = orm.relationship('Organization', backref="employees")
