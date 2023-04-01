

from flask import Flask
from flask_smorest import Api

from db import db

import models

from resources.item import blp as ItemBlueprint
from resources.brand import blp as BrandBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    # Adding configurations to application
    app.config["API_TITLE"] = "BigBazaar SuperMarket REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"

    # Adding swagger-ui config for manually testing APIs
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Adding db related config
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # integrating db with app
    db.init_app(app)
    api = Api(app)

    # creating all the table in db if not already created
    with app.app_context():
        db.create_all()


    # registering the Item and brand blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(BrandBlueprint)

    return app
