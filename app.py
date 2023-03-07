from flask import Flask, jsonify, request
from config import *
from commands import db_cmd
from database import db, ma

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
