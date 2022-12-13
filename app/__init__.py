from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ns = api.namespace('filmes/v1', description='Filmes que eu já vi')

from app.models import table
from app.controllers import default