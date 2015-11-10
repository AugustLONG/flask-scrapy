# -*- coding: utf-8 -*-
__author__ = 'Azcortex'

from flask import Blueprint

auth = Blueprint('auth',__name__)
# name就是.auth

from . import  views