from . import ugc
from flask import render_template, redirect, url_for, abort, flash, request
from ..models import v2ex
from .. import db

@ugc.route('/v2ex')
def  v2ex():

	# can't read the content,the memory problem
	# got '<function v2ex at 0x7f8ef24bd758>'

	content = db.session.query(v2ex).all()

	return render_template('v2ex.html',content=content)