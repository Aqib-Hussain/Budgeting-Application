from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


@app.route("/")
def homepage():
    return render_template('Index.html')


@app.route("/signup", methods=['POST'])
def signUpUser():
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']
    password_hash = generate_password_hash(password)
    if password == confirmPassword:
       hashed_password = generate_password_hash(password)
    else:
        return render_template('index.html', error="Your passwords do not match")

    # check database to see if user already exists

    #SAVE TO DB
    return redirect('/login')

