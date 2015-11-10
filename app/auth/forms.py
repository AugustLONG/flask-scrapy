# -*- coding: utf-8 -*-
__author__ = 'Azcortex'

from ..models import User
from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import Required,Email,Length,EqualTo
from wtforms import ValidationError


class LoginForm(Form):
    # 几个肯定要有的，用户名，密码，是否记住我，以及提交按钮
    email = StringField(u'邮箱',validators=[Required(),Email(),
                                         Length(1,20)])
    password = PasswordField(u'密码',validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'提交')

class RegistrationForm(Form):
    email = StringField(u'登录邮箱',validators=[Required(),Email()])
    username = StringField(u'用户名',validators=[Required(),Length(1,64)])
    password = PasswordField(u'密码',validators=[Required(),EqualTo('password2',
                                                                 message=u'两次密码不同')])
    password2 = PasswordField(u'密码确认',validators=[Required()])
    submit = SubmitField(u'提交信息')

    def verify_email(self,field):
        user = User.query.filter_by(email = field.data).first()
        if user is not None:
            raise ValidationError('the email alrady exists')

    def verify_username(self,field):
        user = User.query.filter_by(username = field.data).first()
        if user is not None:
            raise ValidationError(u'用户名已存在')




