# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

from ..models import Permission

# 为了让某个变量能够随时在上下文中找到，使用上下文处理器
@main.app_context_processor
def inject_permissions():
    return dict(Permission = Permission)