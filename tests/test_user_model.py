# -*- coding:utf-8 -*-

import unittest
import datetime
import time
from app import create_app,db
from app.models import User,Role,Permission,AnonymousUser

class UserModelTestCast(unittest.TestCase):

    def setup(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        #self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        #self.app_context.pop()

    def test_password_setter(self):
        # 这个程序是为了测试密码是否可读？
        user = User(password='cat')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password='cat')
        # 下面的 with 是做什么用的没有明白
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password='123')
        self.assertTrue(user.verify_password('123'))
        self.assertFalse(user.verify_password('456'))

    def test_password_salts_are_random(self):
        user1=User(password='123')
        user2=User(password='123')
        self.assertTrue(user1.password_hash != user2.password_hash)
    # 很显然，这些测试都是非常的，来完成各样不同的功能

    def test_roles_and_permission(self):
        user_admin = User(email='evened@163.con',username='admin',password='123')
        self.assertTrue(self.can(Permission.ADMINISTER))

        user_usual = User(email='123@163.com',username='usual',password='123')
        self.assertTrue(self.can(Permission.WRITE_ARTICLES))
        self.assertFalse(self.can(Permission.ADMINISTER))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.WRITE_ARTICLES))
