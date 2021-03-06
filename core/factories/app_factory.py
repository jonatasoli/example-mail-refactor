import locale
import logging
import os
from logging import Formatter
from logging.handlers import RotatingFileHandler

from flask import Flask

import config as default_config
from core.factories import blueprints_factory
from ext import migrate
from ext.db import db
from ext.marshmallow import ma
from ext.restplus import api


def create_app(config=None) -> Flask:
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")  # set locale
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    if config is None:
        config = default_config

    app.config.from_object(config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Blueprints and Namespaces
    app = blueprints_factory.register_blueprints(app)
    api.init_app(app)

    """
    loghandler = RotatingFileHandler(os.path.join(app.config.get("BASEDIR"), "logs", "partyou.log"))
    loghandler.setFormatter(Formatter(
        "%(asctime)s %(levelname)s: %(message)s "
        "[in %(pathname)s:%(lineno)d]"
    ))
    

    app.logger.addHandler(loghandler)
    app.logger.setLevel(logging.INFO)

    app = logger_factory.create_logger(app)
    """
    return app
