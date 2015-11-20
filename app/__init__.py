# -*- coding: utf-8 -*-
__author__ = 'Azcortex'

# 与此同时在这里的 app 应该是定义了所有的部分
from flask import Flask
from flask.ext.login import LoginManager,current_app,current_user
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import  config
from flask.ext.pagedown import  PageDown


# 以上这些是完成最基本的，还有其他，如分页等

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong' #定义保护强度
login_manager.login_view = 'auth.login' #定义登录的页面路由

# 还要求实现一个回调函数，在 models.py 中定义

def create_app(config_name):
    app = Flask(__name__)
    # 如果没有的话自然就是 default 了
    app.config.from_object(config[config_name])

    #进行各种初始化
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # 一直到最后，应该有这样一句
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')


    from .ugc import ugc as ugc_blueprint
    app.register_blueprint(ugc_blueprint,url_prefix='/ugc')

    from .business import business as business_blueprint
    app.register_blueprint(business_blueprint,url_prefix='/business')

    from .news import news as news_blueprint
    app.register_blueprint(news_blueprint,url_prefix='/news')


    return app

