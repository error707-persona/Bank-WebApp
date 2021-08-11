from model import db, bcrypt, login_manager
from flask_login import UserMixin

# class transaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(), nullable=False, unique=True)
#     amount_send = db.Column(db.Integer(), nullable=False)
#     transfer_to = db.Column(db.Integer(), length = 12, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    budget = db.Column(db.Integer, nullable=False, default=1000)
    items = db.relationship('Item', backref='transaction', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
            return f'₹{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'₹{self.budget}'

    @property
    def password_h(self):
        return self.password_h

    @password_h.setter
    def password_h(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    account_no = db.Column(db.Integer, nullable=False, unique=True)
    pin = db.Column(db.Integer, nullable=False, unique=True)
    current_balance = db.Column(db.Integer, nullable=False)
    tran = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return f'Item{self.name}'