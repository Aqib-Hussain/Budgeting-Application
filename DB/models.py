from __main__ import database


class UserAccount(database.Model):
    id = database.Column(database.Long, primary_key=True)
    email = database.Column(database.String(100), nullable=False, unique=True)
    hashedPassword = database.Column(database.String(200), nullable=False)
    # goalValue = database.Column(database.Long(120), nullable=True)
    # incomeValue = database.Column(database.Long(120), nullable=True)
    # expenseValue = database.Column(database.Long(120), nullable=True)
    # assetValue = database.Column(database.Long(120), nullable=True)


