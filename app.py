

from flask import Flask, jsonify
from flask_smorest import Api

from db import db
from blocklist import BLOCKLIST

from resources.item import blp as ItemBlueprint
from resources.brand import blp as BrandBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

import secrets
from flask_jwt_extended import JWTManager

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

    # integrating jwt (authentication) with app
    app.config["JWT_SECRET_KEY"] = "106561910718341680690669917170099921986"
    jwt = JWTManager(app)

    # Addition code to put a limitation on authorization
    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 7:
    #         return {"is_admin" : True}
    #     return {"is_admin" : False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoke_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked",
                 "error": "token revoked"
                 }), 401
        )


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message" : "The token has expired",
                "error" : "token_expired"
            }), 401
        )


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify(
            {
                "message" : "Signature verification failed.",
                "error" : "invalid_token"
            }), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {
                    "description" : "Request does not contain an access token",
                    "error" : "authorization_required"
                }
            ), 401
        )

    # creating all the table in db if not already created
    with app.app_context():
        db.create_all()


    # registering the Item and brand blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(BrandBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


# Calling app for debug
# app = create_app()
# app.run(debug=True, port=5432)