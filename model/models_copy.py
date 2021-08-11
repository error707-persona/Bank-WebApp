from model import db
from datetime import datetime
# class transaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(), nullable=False, unique=True)
#     amount_send = db.Column(db.Integer(), nullable=False)
#     transfer_to = db.Column(db.Integer(), length = 12, nullable=False)


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    fromm = db.Column(db.String(), nullable=False)
    to = db.Column(db.String(), nullable=False)
    date= db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False, default=1000)

    def __repr__(self):
        return f'Transaction{self.id}'


class User_this(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    account_no = db.Column(db.Integer, nullable=False)
    branch = db.Column(db.String(), nullable=False)
    bankname = db.Column(db.String(), nullable=False)
    pin = db.Column(db.Integer, nullable=False, unique=True)
    current_balance = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'Item {self.name}'