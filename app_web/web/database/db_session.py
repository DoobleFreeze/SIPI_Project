import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
import logging
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(logger: logging.Logger, db_host, db_port, db_login, db_password):
    """
    Создание подключения к БД

    Создает подключение к базе данных.
    Для подключения к БД в переменных среды должны быть `host` - хост базы
    данных, `port` - порт подключения, `login` - никнейм (юзернейм)
    пользователя, от имени которого будет вестись взаимодействие с базой данных,
    `password` - пароль от аккаунта пользователя.

    Arguments:
        db_password:
        db_login:
        db_port:
        db_host:
        logger (logging.Logger): Оператор логирования.
    """
    global __factory

    if __factory:
        return

    conn_str = f'postgresql://{db_login}:{db_password}@{db_host}:{db_port}/sipi_db'
    logger.info(f"Connecting to the database")

    engine = sa.create_engine(conn_str)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """
    Создание сессии для работы с БД

    Return:
        Session: сессия для работы с БД
    """
    global __factory
    return __factory()
