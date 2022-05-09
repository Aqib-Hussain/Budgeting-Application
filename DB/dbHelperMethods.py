from functools import wraps

from DB import database
from . import models
from .models import UserAccount, Goal


def insertIntoDatabase(func):
    def wrapper(*args, **kwargs):
        database.session.add(func(*args, **kwargs))
        database.session.commit()
        return func(*args, **kwargs)

    return wrapper


@insertIntoDatabase
def createUser(email, hashedPassword):
    return UserAccount(email=email, hashedPassword=hashedPassword)


@insertIntoDatabase
def createGoal(user, goalText, currentNumber, goalNumber):
    return Goal(userAccountId=user.id, goalText=goalText, currentNumber=currentNumber, goalNumber=goalNumber,
                percentageProjection=0.00, yearProjection=0)


def searchForUserByEmail(email):
    user = UserAccount.query.filter_by(email=email).first()
    return user


def searchForUsersGoals(user):
    goals = database.session.execute(database.select(Goal).where(Goal.userAccountId == user.id))
    return goals.scalars().all()


def searchForIndividualGoal(goalId):
    goal = database.session.execute(database.select(Goal).where(Goal.id == goalId))
    return goal.fetchone()[0]


def updateUserGoal(goalId, goalText, currentNumber, goalNumber):
    goal = Goal.query.filter_by(id=goalId).first()
    goal.goalText = goalText
    goal.goalNumber = goalNumber
    goal.currentNumber = currentNumber
    database.session.commit()


def updateGoalProjection(goalId, percentageProjection, yearProjection):
    goal = Goal.query.filter_by(id=goalId).first()
    goal.percentageProjection = percentageProjection
    goal.yearProjection = yearProjection
    database.session.commit()


def deleteUserGoal(goalId):
    database.session.delete(Goal.query.filter_by(id=goalId).one())
    database.session.commit()
