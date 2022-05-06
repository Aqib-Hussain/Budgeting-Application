from flask_sqlalchemy import SQLAlchemy
from app import app


# Setting up the database connection to run locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financeDatabase.db'
database = SQLAlchemy(app)