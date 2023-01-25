from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        zip_code = request.form.get('zipCode')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        interest_1 = request.form.get('interest_1')
        interest_2 = request.form.get('interest_2')
        interest_3 = request.form.get('interest_3')
        interest_4 = request.form.get('interest_4')
        interest_5 = request.form.get('interest_5')
        points = 0

        user = User.query.filter_by(email=email).first()
        check = User.query.filter_by(username=username).first()
        if user:
            flash('Email already exists.', category='error')
        elif check:
            flash('Username alredy taken.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, zip_code=zip_code, interest_1=interest_1, interest_2=interest_2,
                            interest_3=interest_3, interest_4=interest_4, interest_5=interest_5, points=points, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        interest_1 = request.form.get('interest_1')
        interest_2 = request.form.get('interest_2')
        interest_3 = request.form.get('interest_3')
        interest_4 = request.form.get('interest_4')
        interest_5 = request.form.get('interest_5')

        check = User.query.filter_by(email=email).first()
        user = User.query.filter_by(id=current_user.id).first()
        if check:
            flash('Email already exists.', category='error')
        elif len(email) > 0 and len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) > 0 and len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) > 0 and len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            if email != '':
                user.email = email
            if first_name != '':
                user.first_name = first_name
            if password1 != '':
                user.password = generate_password_hash(password1, method='sha256')
            if interest_1 != '':
                user.interest_1 = interest_1
            if interest_2 != '':
                user.interest_2 = interest_2
            if interest_3 != '':
                user.interest_3 = interest_3
            if interest_4 != '':
                user.interest_4 = interest_4
            if interest_5 != '':
                user.interest_5 = interest_5
            db.session.commit()
            return redirect(url_for('views.profile'))

    return render_template("edit.html", user=current_user)
