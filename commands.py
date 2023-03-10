from flask import Blueprint
from database import db

db_cmd = Blueprint('db_cmd', __name__)

@db_cmd.cli.command('create')
def create_db():
    db.create_all()
    print('Database created!')

@db_cmd.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Database dropped!')