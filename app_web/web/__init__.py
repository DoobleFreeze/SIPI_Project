from flask import Flask, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .database import db_session
from .database import __all_models as al

logger = None
operator = None


def create_api(flask_log,
               logging_cgf_path,
               db_host,
               db_port,
               db_login,
               db_password) -> Flask:
    global logger, operator

    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Инициализация логирования
    from .initialization_logger import get_logger
    logger = get_logger(
        logging_cfg_path=logging_cgf_path,
        flask_log=flask_log,
        flask_app=app,
    )

    # Инициализация очередей
    from .handlers.operator import Operator
    operator = Operator(
        logger=logger
    )

    # Инициализация Базы данных
    db_session.global_init(
        logger=logger,
        db_host=db_host,
        db_port=db_port,
        db_login=db_login,
        db_password=db_password,
    )

    from . import endpoint_static_controllers as static_control
    from .handlers.global_values import JSON_ERROR_NOT_FOUND

    app.register_blueprint(static_control.module)
    app.config['SECRET_KEY'] = 'rtu_mirea_ona_key'

    @login_manager.user_loader
    def load_user(user_id):  # Возвращает информацию о пользователе по его ID
        s = db_session.create_session()
        return s.query(al.users.Users).get(user_id)

    @app.errorhandler(404)
    def not_found(_error):
        return make_response(jsonify(JSON_ERROR_NOT_FOUND), JSON_ERROR_NOT_FOUND['response_code'])

    return app
