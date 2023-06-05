import sqlalchemy

from ..db_session import SqlAlchemyBase


class TypeAppointment(SqlAlchemyBase):
    __tablename__ = 'type_appointment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text)
