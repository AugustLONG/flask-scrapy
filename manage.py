# -*- coding: utf-8 -*-
__author__ = 'Azcortex'

# 从这里面要引入好多东西
import os
from app import create_app, db
from app.models import User, Role ,Permission,Post
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')  # 之前在__init__里面定义的东西用到了
manager = Manager(app)
migrate = Migrate(app, db)

# 接下来要在 shell 中添加语言
def make_shell_context():
    return dict(app = app, db = db, User = User, Role = Role,Post=Post,Permission=Permission)


manager.add_command('shell', Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

# 为了添加单元测试功能
@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
