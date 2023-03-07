from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import *
from commands import db_cmd

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(db_cmd)

    from routes import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
