from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

@app.route('/')
def hello():
	from app.models import User
	user = User.get_by_id(3)
	return str(user)

from . import slack_handlers
app.register_blueprint(slack_handlers.bp)