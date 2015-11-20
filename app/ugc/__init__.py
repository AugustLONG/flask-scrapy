# -*- coding: utf-8 -*-
__author__ = 'Azcortex'

from flask import Blueprint

ugc = Blueprint('ugc',__name__)
# name就是.auth

from . import  views