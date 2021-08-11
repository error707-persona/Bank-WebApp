
import sqlalchemy
from model import app
from flask import render_template, redirect, url_for, flash, request, session
from model.models import Item
from model.forms import RegisterForm, LoginForm, transfer, login_pass
from model.models import Users
from model.models import db
from model.models_copy import User_this, Transaction
from flask_login import login_user, logout_user, login_required

global user
@app.route('/')
@app.route('/home')
def home_page():
    return render_template("index.html")

@app.route('/about/<username>')
def about_page(username):
     return f'<h1>About Page {username}</h1>'

@app.route('/customer', methods=['GET', 'POST'])
# @login_required
def customers():
    transferForm = transfer()
    if transferForm.validate_on_submit():
        if session.get('logged_in') == True:
            if int(transferForm.amount.data) < 100:
                flash('Invalid transaction: Amount is less then 100', category='danger')
            else:
                update = User_this.query.filter_by(account_no=transferForm.account.data).first()
                cut = User_this.query.filter_by(account_no=int(session['account_no'])).first()
                if update == cut:
                    flash('Invalid Transaction: Cannot Send money to Your own account', category='danger')
                else:
                    if session['current_balance'] < int(transferForm.amount.data):
                        flash('Invalid Transaction: Not enough balance in your account', category='danger')
                    else:
                        update.current_balance = update.current_balance + int(transferForm.amount.data)
                        cut.current_balance = cut.current_balance - int(transferForm.amount.data)
                        session['current_balance'] = cut.current_balance
                        record = Transaction(fromm='current user', to=transferForm.account.data, amount=transferForm.amount.data)
                        db.session.add(record)
                        db.session.commit()
                        flash('Congratulations the transaction was a success!', category='success')
        else:
            flash('Please login first to carry out transactions', category='info')
    items = User_this.query.all()
    return render_template('customer.html',  items=items, transferForm=transferForm)

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    log = login_pass()
    if log.validate_on_submit():
        if session.get('logged_in') == True:
            flash(f'You are already logged Please logout', category='info')
        else:
            user = User_this.query.filter_by(account_no=int(log.account.data)).first()
            session['name']=user.name
            session['email']=user.email
            session['account_no']=user.account_no
            session['branch']=user.branch
            session['bankname']=user.bankname
            session['pin']=user.pin
            session['current_balance']=user.current_balance
            session['logged_in'] = True
            # login_user(user)
            flash(f'Account Created Successfully! You are now logged in as: {user.name}', category='success')
        return redirect(url_for('customers'))
    items = User_this.query.all()
    return render_template('login_cus.html', items=items, log=log)

@app.route('/logout_page')
def logout_page():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('account_no', None)
    session.pop('branch', None)
    session.pop('bankname', None)
    session.pop('current_balance', None)
    session.pop('pin', None)
    session.pop('logged_in', None)
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user_to_create = Users(username=form.username.data, email=form.email.data, password_h=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(f'Account Created Successfully! You are now logged in as: {attempted_user.username}', category='success')
        except sqlalchemy.exc.SQLAlchemyError as e: print(e)

        return redirect(url_for('customers'))
    if form.errors != {}: #if there are no errors from validations
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password1.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('customers'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))