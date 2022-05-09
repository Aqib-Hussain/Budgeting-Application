from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder="../static")

# Setting up the database connection to run locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financeDatabase.db'
database = SQLAlchemy(app)
