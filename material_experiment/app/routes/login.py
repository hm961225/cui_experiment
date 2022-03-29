from flask import Blueprint, flash, redirect, request, render_template, session, url_for

from app.models import db
from app.models.user import User


login_bp = Blueprint("login_bp", __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('index')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            session['username'] = user.username
            flash("登录成功")
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
    return render_template('login.html')


@login_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template(('register.html'))