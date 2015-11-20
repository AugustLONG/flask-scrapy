# -*- coding: utf-8 -*-
__author__ = 'Azcortex'

from flask import Blueprint

news = Blueprint('news',__name__)
# name就是.auth

from . import  views