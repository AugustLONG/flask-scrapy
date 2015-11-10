# -*- coding: utf-8 -*-

# 回调函数，使用指定的 id 来加载用户
from datetime import datetime
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug import generate_password_hash, check_password_hash
from . import db, login_manager


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80  # 管理员权限


class Role(db.Model):
    __tablename__ = 'roles'
    # 这里自己把书和文档翻一遍
    # 按照一步一步来，先定义前面几个
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)

    # 还是要满足相互的映射关系
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')
    # 向 User模型中反向插入一个 role 属性
    permission = db.Column(db.Integer)
    # 还有在用户一开始注册的时候用的 default
    default = db.Column(db.Boolean, default = False, index = True)

    @staticmethod
    def insert_roles():  # 但是 True 和 False 之间的区别是？
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)  # 用的是异或处理
        }

        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


    def __repr__(self):
        return '<Role %r>' % self.name


# 定义用户表单，完成对应的关注功能
class Follow(db.Model):

    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key = True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key = True)
    time_stamp = db.Column(db.DateTime, default = datetime.utcnow())


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        # 这里牵涉到python的面向对象编程，是自己之后需要补充的地方
        # **kwargs 指的是 进行传值（有-号）的参数
        super(User, self).__init__(**kwargs)
        # 调用基类的构造函数

        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permission = 0xff).first()
            else:
                self.role = Role.query.filter_by(default = True).first()


    # 定义用户角色，还要和外键连接起来
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))

    # 还要满足相互的映射关系
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # 一个人可以写多篇文章
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    # 增加关于用户资料的部分
    name = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    gender = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default = datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow())

    comments = db.relationship('Comment',backref='author',lazy='dynamic')
    # 完成用户互相关注的部分

    # 要把左右两侧拆分成基本的一对多关系
    followers = db.relationship('Follow',
                                foreign_keys = [Follow.followed_id],
                                backref = db.backref('followed',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')

    followed = db.relationship('Follow',
                               foreign_keys = [Follow.follower_id],
                               backref = db.backref('followers',lazy='joined'),
                               lazy='dynamic',
                               cascade = 'all,delete-orphan')

    # 为了方便，还要增加很多的判断语句
    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None
    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id = user.id).first() is not None

    def follow(self,user):
        if not self.is_following(user):
            f = Follow(followers=self,followed=user)
            db.session.add(f)
    def unfollow(self,user):
        if self.is_followed_by(user):
            f=self.followed.filter_by('followed_id = user.id').first()
            db.session.remove(f)



    # 还有关于 last_seen 是如何做的
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def can(self, permission):
        return self.role is not None and \
               (self.role.permission & permission) == permission

    def is_adminisrator(self):
        return self.role.permission == 0xff


    # 为了生成一系列的虚拟数据
    @staticmethod
    def generate_fake(count = 100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()  #这里还是看文档

        for i in range(count):
            u = User(email = forgery_py.internet.email_address(),
                     username = forgery_py.internet.user_name(),
                     password = forgery_py.lorem_ipsum.word(),
                     name = forgery_py.name.full_name(),
                     about_me = forgery_py.lorem_ipsum.sentence(),
                     member_since = forgery_py.date.date())
            db.session.add(u)
            db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    # 类的继承

    def can(self, permission):
        return False

    def is_administor(self):
        return False


# 还要处理用户表单
class Post(db.Model):
    __tablename__ ='posts'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime, index = True, default = datetime.utcnow())  # 一定要有 default
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment',backref='post',lazy='dynamic')



    @staticmethod
    def generate_fake(count = 100):
        # 我感觉位置都可以，在哪儿引入都行
        from random import seed, randint
        import forgery_py

        seed()
        user_cont = User.query.count()
        for i in range(count):
            # 根据文档，limit是返回一个限制，而offset是返回一个范围
            u = User.query.offset(randint(0, user_cont - 1)).first()
            p = Post(body = forgery_py.lorem_ipsum.sentence(),
                     time_stamp = forgery_py.date.date(),
                     author = u)
            db.session.add(p)
            db.session.commit()


# 下面是要处理用户评论，和用户、文章之间都是一对多关系

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text,index=True)
    time_stamp = db.Column(db.DateTime,default=datetime.utcnow())

    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))




# 为的是处理没有进行登陆的用户，保证一致性
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()
    # 或者是 User.quert.get(int(user_id))

