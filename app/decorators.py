# -*- coding:utf-8 -*-
__author__ = 'Azcortex'

# 在这里我主要想实现的是将一些权限只对某些用户开放

from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

# 这里好多看不懂的，还是文档功底……