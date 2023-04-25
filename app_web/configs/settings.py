"""
Настройки сервера:
HOST_SERVER - Хост сервера (Его домен). По умолчанию стоит 0.0.0.0 для того,
    чтобы к нему можно было обращаться из разных контейнеров.
PORT_SERVER - Порт сервера.

Настройки логирования:
FLASK_LOG - Включить/выключить логирование от библиотеки Flask
LOGGING_CFG_PATH - Путь до файла конфигурации.

Настройки Базы Данных:
DB_HOST - Хост БД
DB_PORT - Порт подключения к БД
DB_LOGIN - Логин пользователя
DB_PASSWORD - Пароль пользователя
"""
from dotenv import load_dotenv
import os

HOST_SERVER = '0.0.0.0'
PORT_SERVER = 6589

FLASK_LOG = False
LOGGING_CFG_PATH = "./configs/logging.cfg.yml"

load_dotenv(dotenv_path="./configs/.db.env")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_LOGIN = os.getenv("DB_LOGIN")
DB_PASSWORD = os.getenv("DB_PASSWORD")
