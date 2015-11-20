# -*- coding: utf-8 -*-
__author__ = 'Azcortex'

import os

basedir = os.path.abspath(os.path.dirname(__file__))
# 上面为了定义数据采用标准

class Config:
    # 一些常用的直接记录就好
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 一些东西在自己写的时候，分页，再用
    FLASK_ADMIN_EMAIL = 'evened@163.com'
    FLASK_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    SQLALCHEMY_BINDS ={
    #'website':'mysql://root:402840evenedMYSQL@localhost:3307/website',

    # for the development config
    # changet 'username/password/dbname' to yours'
    'scrapy':'mysql://username:password@localhost:3307/dbname',
    
}




class TestingConfig(Config):
    TESTING = True #这看起来是自己定义的一个
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'date-test.sqlite')

    SQLALCHEMY_BINDS ={
    'scrapy':'mysql://username:password@localhost:3307/dbname',
    
}

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-pro.sqlite')
    SQLALCHEMY_BINDS ={
    'scrapy':'mysql://username:password@localhost:3307/dbname',
    
}


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-pro.sqlite')


# 下面要引入一个字典来完成对选择的默认
config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}
