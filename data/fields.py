import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Fields(SqlAlchemyBase):
    __tablename__ = 'fields'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    player1_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("user.id"))
    player1_field = sqlalchemy.Column(sqlalchemy.String)
    player1_field_isfilled = sqlalchemy.Column(sqlalchemy.Boolean)
    player2_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("user.id"))
    player2_field = sqlalchemy.Column(sqlalchemy.String)
    player2_field_isfilled = sqlalchemy.Column(sqlalchemy.Boolean)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean)
    player1 = orm.relationship('User', foreign_keys=[player1_id])
    player2 = orm.relationship('User', foreign_keys=[player2_id])
