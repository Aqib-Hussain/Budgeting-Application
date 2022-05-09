from DB import database


class UserAccount(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    email = database.Column(database.String(100), nullable=False, unique=True)
    hashedPassword = database.Column(database.String(200), nullable=False)
    goals = database.relationship("Goal", backref='userAccount', lazy='dynamic')
    # goalValue = database.Column(database.Long(120), nullable=True)
    # incomeValue = database.Column(database.Long(120), nullable=True)
    # expenseValue = database.Column(database.Long(120), nullable=True)
    # assetValue = database.Column(database.Long(120), nullable=True)


class Goal(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    userAccountId = database.Column(database.Integer, database.ForeignKey(UserAccount.id))
    goalText = database.Column(database.String(255), nullable=False)
    goalNumber = database.Column(database.Float(200), nullable=False)
    currentNumber = database.Column(database.Float(200), nullable=False)
    percentageProjection = database.Column(database.Float(200), nullable=False)
    yearProjection = database.Column(database.Integer, nullable=False)


# Creating the tables for the database
database.create_all()
