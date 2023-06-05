import datetime
import sqlalchemy
from sqlalchemy import orm

from ..db_session import SqlAlchemyBase


class Review(SqlAlchemyBase):
    __tablename__ = 'review'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    user_comment = sqlalchemy.Column(sqlalchemy.Text)
    stars = sqlalchemy.Column(sqlalchemy.Integer)
    data_create = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    org_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("organization.id"))

    users = orm.relationship('Users', backref="review")
    organization = orm.relationship('Organization', backref="review")
