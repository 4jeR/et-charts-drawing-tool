from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_caching import Cache
import os 

CHARTS_FOLDER = os.path.join('static', 'plots')

app = Flask(__name__, static_folder='static')

app.config['UPLOAD_FOLDER'] = CHARTS_FOLDER
app.config['SECRET_KEY'] = 'c8ba4ab3f643089aed4ff7a6205e4815'
# app.config['CACHE_TYPE'] = 'simple'
# app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///et_charts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# cache = Cache(app)
from web import routes 
from web import help_utils