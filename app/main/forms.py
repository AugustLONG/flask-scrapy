# -*- coding:utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import  Required,Length
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField


class EditProfileForm(Form):
    name = StringField(u'真实姓名')
    about_me = TextAreaField(u'自我描述')
    submit = SubmitField(u'提交更改')

class PostForm(Form):
    body = PageDownField(u'想说些什么')
    submit = SubmitField(u'提交')

class CommentForm(Form):
    body = StringField(u'发表你的评论',validators=[Required()])
    submit = SubmitField(u'提交')