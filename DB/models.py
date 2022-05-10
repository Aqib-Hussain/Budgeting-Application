from DB import database


class UserAccount(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String(100), nullable=False, unique=True)
    hashedPassword = database.Column(database.String(200), nullable=False)
    goals = database.relationship("Goal", backref='userAccount', lazy='dynamic')
    valuations = database.relationship("Valuation", backref='userAccount', lazy='dynamic')


class Goal(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    userAccountId = database.Column(database.Integer, database.ForeignKey(UserAccount.id))
    goalText = database.Column(database.String(255), nullable=False)
    goalNumber = database.Column(database.Float(200), nullable=False)
    currentNumber = database.Column(database.Float(200), nullable=False)
    percentageProjection = database.Column(database.Float(200), nullable=False)
    yearProjection = database.Column(database.Integer, nullable=False)


class Valuation(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    userAccountId = database.Column(database.Integer, database.ForeignKey(UserAccount.id))
    propertyValuesAsset = database.Column(database.Float(200), nullable=False)
    savingsAccountsAsset = database.Column(database.Float(200), nullable=False)
    pensionsAccountsAsset = database.Column(database.Float(200), nullable=False)
    carsAsset = database.Column(database.Float(200), nullable=False)
    otherAsset = database.Column(database.Float(200), nullable=False)
    mortgagesLiability = database.Column(database.Float(200), nullable=False)
    studentLoanLiability = database.Column(database.Float(200), nullable=False)
    personalLoanLiability = database.Column(database.Float(200), nullable=False)
    carLoansLiability = database.Column(database.Float(200), nullable=False)
    otherDebtLiability = database.Column(database.Float(200), nullable=False)


# Creating the tables for the database
database.create_all()
