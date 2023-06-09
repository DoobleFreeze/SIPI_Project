import sqlalchemy
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase


class Favorites(SqlAlchemyBase):
    __tablename__ = 'favorites'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    org_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("organization.id"))

    users = orm.relationship('Users', backref="favorites")
    organization = orm.relationship('Organization', backref="favorites")
