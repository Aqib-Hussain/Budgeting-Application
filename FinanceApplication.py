from flask import render_template, request, redirect, make_response, jsonify
from DB.dbHelperMethods import createUser, searchForUserByEmail, createGoal, searchForUsersGoals, deleteUserGoal, \
    searchForIndividualGoal, updateUserGoal, updateGoalProjection, createValuation, searchForUserValuations, \
    updateValuation
from werkzeug.security import generate_password_hash, check_password_hash
from DB import app
from API.PolygonDataGetter import makeGraphForStock
from Visualisations.BuildGraphs import startBuildingValuationsCharts
import jwt as jwt
from datetime import datetime, timedelta
import functools

app.config['MY_JWT_KEY'] = "YouCanEnterJABA"


def jwtValidate(func):
    @functools.wraps(func)
    def checkJwt(*args, **kwargs):
        try:
            if request.cookies.get('jwtToken') is not None:
                jwtPayload = jwt.decode(request.cookies.get('jwtToken'), app.config['MY_JWT_KEY'], algorithms='HS256')

                user = searchForUserByEmail(jwtPayload.get('username'))

                if user is None:
                    return render_template('Login.html', error="Please login first")

                return func(*args, **kwargs)
            else:
                return render_template('Login.html', error="Please login first")
        except jwt.exceptions.ExpiredSignatureError:
            return render_template('Login.html', error="Please login again")

    return checkJwt


@app.route("/")
def homepage():
    return render_template('Index.html')


@app.route("/signup", methods=['POST'])
def signUpUser():
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']
    if password == confirmPassword:
        hashed_password = generate_password_hash(password)
    else:
        return render_template('Index.html', error="Your passwords do not match")
    userFound = searchForUserByEmail(email)
    if userFound is None:
        createUser(email, hashed_password)
        newUser = searchForUserByEmail(email)
        createValuation(newUser.id)
    else:
        return render_template('Index.html', error="This email is being used")
    return redirect('/login')


@app.route("/login", methods=['GET', 'POST'])
def loginUser():
    if request.method == 'GET':
        return render_template('Login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = searchForUserByEmail(email)
        if user is not None:
            if check_password_hash(user.hashedPassword, password):
                jwtToken = jwt.encode(
                    {'username': user.email, 'exp': datetime.utcnow() + timedelta(minutes=20)},
                    app.config['MY_JWT_KEY'])
                response = make_response(redirect('/goals'))
                response.set_cookie('userLoggedIn', user.email)
                response.set_cookie('jwtToken', jwtToken)
                return response
            else:
                return render_template('Login.html', error="The password is incorrect")
        else:
            return render_template('Login.html', error="This account does not exist")


@app.route("/goals", methods=['GET', 'POST'])
@jwtValidate
def displayAndAddGoals():
    username = request.cookies.get('userLoggedIn')
    user = searchForUserByEmail(username)
    goals = searchForUsersGoals(user)
    if request.method == 'GET':
        return render_template('Goals.html', goals=goals, username=username)
    else:
        goalText = request.form['goalText']
        goalNumber = request.form['goalNumber']
        currentNumber = request.form['currentNumber']
        createGoal(user, goalText, currentNumber, goalNumber)
        return redirect('/goals')


@app.route("/deleteOrEditGoal", methods=['POST'])
@jwtValidate
def deleteOrEditGoal():
    username = request.cookies.get('userLoggedIn')
    user = searchForUserByEmail(username)
    goals = searchForUsersGoals(user)
    if 'deleteButton' in request.form:
        deleteUserGoal(request.form['deleteButton'])
        return redirect('/goals')
    elif 'editButton' in request.form:
        specificGoal = searchForIndividualGoal(request.form['editButton'])
        return render_template('Goals.html', goals=goals, username=username, editButtonPressed=True,
                               specificGoal=specificGoal)
    elif 'submitEditButton' in request.form:
        goalId = request.form['submitEditButton']
        goalText = request.form['newGoalText']
        currentNumber = request.form['newCurrentValue']
        goalNumber = request.form['newGoalValue']
        updateUserGoal(goalId, goalText, currentNumber, goalNumber)
        return redirect("/goals")
    elif 'closeEditButton' in request.form:
        return redirect("/goals")


@app.route("/updateProjections", methods=['POST'])
@jwtValidate
def updateProjections():
    goalId = request.form['updateGoalProjection']
    yearProjection = request.form['yearProjection']
    percentageProjection = request.form['percentageProjection']
    updateGoalProjection(goalId, percentageProjection, yearProjection)
    return redirect('/goals')


@app.route("/markets", methods=['GET', 'POST'])
@jwtValidate
def viewMarkets():
    if request.method == 'GET':
        return render_template('Markets.html')
    else:
        stockName = request.form['stockName']
        dateFrom = request.form['dateFrom']
        dateTo = request.form['dateTo']
        makeGraphForStock(stockName.upper(), dateFrom, dateTo)
        return render_template('Markets.html', generateGraph=True, stockName=stockName, dateFrom=dateFrom,
                               dateTo=dateTo)


@app.route("/valuations", methods=['GET', 'POST'])
@jwtValidate
def viewValuations():
    username = request.cookies.get('userLoggedIn')
    user = searchForUserByEmail(username)
    valuations = searchForUserValuations(user.id)
    if request.method == 'GET':
        return render_template('Valuations.html', username=username, valuations=valuations)
    else:
        updateValuation(user.id, request.form['propertyValuesAsset'],
                        request.form['savingsAccountsAsset'],
                        request.form['pensionsAccountsAsset'], request.form['carsAsset'],
                        request.form['otherAsset'],
                        request.form['mortgagesLiability'],
                        request.form['studentLoanLiability'], request.form['personalLoanLiability'],
                        request.form['carLoansLiability'],
                        request.form['otherDebtLiability'])
        startBuildingValuationsCharts(user.id)
        return render_template('Valuations.html', username=username, valuations=valuations, showGraphs=True)


if __name__ == '__main__':
    app.run()
