from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditUserForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

import logging

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered.  Please log in')
        return redirect(url_for('login'))

    return render_template('register.html', title='register', form=form)


@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')

            return redirect(next_page)

        flash('Invalid username and password combination')

    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['get', 'post'])
def edit_profile():
    form = EditUserForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User {} cannot be found'.format(username))
        return redirect(url_for('index'))

    if user == current_user:
        flash('Sorry, you cannot follow yourself')
        return redirect(url_for('index'))

    current_user.follow(user)
    db.session.commit()
    flash('You are now following {}'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User {} cannot be found'.format(username))
        return redirect(url_for('index'))

    if user == current_user:
        flash('Sorry, you cannot unfollow yourself')
        return redirect(url_for('index'))

    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}'.format(username))
    return redirect(url_for('user', username=username))
