"""There are settings for flask app server"""

from flask import Flask

from static.data import SECRET_KEY


def setup_app() -> Flask:
    """sets up a Flask up with sqlite db

    :return: Flask app
    """

    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app
