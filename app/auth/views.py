from flask import render_template, redirect, url_for, flash, request
from . import auth
from .forms import LoginForm, RegisterForm
from app.models import User
from app import db
from flask_login import login_required, current_user, logout_user, login_user
from app.emails import mail_sender


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Пользователь с указанным email не зарегистрирован.')
            return redirect(url_for('auth.login'))
        if not user.verify_password(form.password.data):
            flash('Неправильный email или пароль.')
            return redirect(url_for('auth.login'))
        else:
            login_user(user=user, remember=form.remember_me.data)
            flash('Вы успешно вошли в систему.')
            return redirect(request.args.get('next') or url_for('main.chanel', chanelname='all'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email = form.email.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Спасибо за регистрацию. Теперь вы можете зайти на сайт.')
        mail_sender(to=user.email, subject='Welcome', template='email/new_user', user=user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
