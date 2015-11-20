# -*- coding: utf-8 -*-
# 这应该是成系统的，引入映射关系，引入数据库，引入表格


from . import auth
from flask import render_template, url_for, redirect, request,flash
from flask.ext.login import login_required, current_user, login_user, logout_user
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db

# 登录页面的首页应该是在 main 上面定义跌

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    # 是登录而不是注册角色，自己有点混了
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('登陆成功')
            # 而重定向的时候应该返回到用户在登陆之前想要返回的那个界面
            # 虽然并没有太大意义…………
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form = form)  # 逻辑清楚




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # 以后可能还需要再增加一个验证条件
    flash('注销成功')
    return redirect(url_for('main.index'))


@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        # 但是找不到验证用户名和密码是否有重合的地方啊
        flash('success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)


#在每次登录请求前运行
@auth.before_app_request
def before_request():
    # 它是在什么时候会再次运行？
    if current_user.is_authenticated:
        current_user.ping()