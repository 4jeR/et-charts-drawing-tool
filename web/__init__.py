from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 

CHARTS_FOLDER = os.path.join('static', 'plots')

app = Flask(__name__, static_folder='static')

app.config['UPLOAD_FOLDER'] = CHARTS_FOLDER
app.config['SECRET_KEY'] = 'c8ba4ab3f643089aed4ff7a6205e4815'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///et_charts'

db = SQLAlchemy(app)

from web import routes 
from web import tool_utils