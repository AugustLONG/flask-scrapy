# -*- coding:utf-8 -*-
from flask import  render_template
from . import main

# 应该也是文档里的东西
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@main.app_errorhandler(500)
def internel_serve_error(e):
    return render_template('500.html'),500