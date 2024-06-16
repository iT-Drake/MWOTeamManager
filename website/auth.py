from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=remember)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        in_game_name = request.form.get('inGameName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_settings_changed = False
        user = User.query.filter_by(name=name).first()
        if in_game_name != user.in_game_name:
            if not in_game_name:
                flash('In-game name can\'t be empty', category='error')
            else:
                user.in_game_name = in_game_name
                user_settings_changed = True
        
        if password1:
            if password1 != password2:
                flash('Passwords don\'t match', category='error')
                user_settings_changed=False
            else:
                user.password = generate_password_hash(password1)
                user_settings_changed = True

        if user_settings_changed:
            db.session.add(user)
            db.session.commit()
            # login_user(user, remember=True)
            flash('User settings updated', category='success')
    
    return render_template('profile.html', user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        in_game_name = request.form.get('inGameName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(name=name).first()
        if user:
            flash('User already exists.', category='error')
        elif len(name) < 3:
            flash('Name must be greater than 2 characters', category='error')
        elif len(in_game_name) < 1:
            flash('In-game name must be filled in', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 5 characters', category='error')
        else:
            new_user = User(name=name, in_game_name=in_game_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            
            return redirect(url_for('views.home'))

    return render_template("register.html")
