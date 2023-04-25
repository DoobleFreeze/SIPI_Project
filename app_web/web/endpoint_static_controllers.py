from flask import Blueprint, render_template, send_from_directory
import traceback
import time

from . import logger, operator
from .handlers.global_values import *
from .database import db_session
from .database import __all_models as al

module = Blueprint('statics_page', __name__, url_prefix='/static')


@module.route('/', methods=['GET'])
def index():
    try:
        pass
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC='static method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    try:
        pass
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/profile/{user_id} method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/login', methods=['GET'])
def profile():
    try:
        pass
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/login method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))


@module.route('/register', methods=['GET'])
def profile():
    try:
        pass
    except Exception as e:
        logger.error(LOG_ERROR.format(FUNC=f'static/register method handler', ERROR=str(e)))
        logger.debug(LOG_ERROR_DETAILS.format(ERROR=traceback.format_exc()))

