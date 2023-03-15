# create virtual environment
virtualenv venv
# activate virtual environment
source venv/bin/activate
# install requirements
pip install -r requirements.txt
# create database tables
python -c "from database import db; db.create_all()"