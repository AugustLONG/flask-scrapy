# -*- coding:utf-8 -*-
__author__ = 'Azcortex'

import  unittest
from flask import current_app
from app import create_app,db

class BasicsTestCase(unittest.TestCase):

    def setup(self):
        self.app=create_app('testing')
        self.app_context = self.app.app_context()
        #self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        #self.app_context.pop()  # 那么这些都是来干什么的

    def test_app_exists(self):
        self.assertFalse(current_app is None)



