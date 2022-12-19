from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'Your account has been created {email}')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You are logged in')
                return redirect(url_for('site.profile'))
            else:
                flash('You have been denied access.')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please check your credentials')
    return render_template('sign_in.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))