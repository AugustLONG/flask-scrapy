# -*- coding: utf-8 -*-

from . import main
from flask import render_template, redirect, url_for, abort, flash, request
from flask.ext.login import login_required, current_user, current_app
from ..models import User, Role, Post, Permission, Follow,Comment,Dmoz
from ..decorators import admin_required, permission_required
from .. import db
from .forms import EditProfileForm, PostForm,CommentForm


@main.route('/', methods = ['GET', 'POST'])
def index():
    # 想要实现只有已经登录的用户才能发表文章
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body = form.body.data,
                    author = current_user._get_current_object())  # 需要真是的用户名
        db.session.add(post)
        db.session.commit()
        flash('文章发表成功')
        return redirect(url_for(('main.index')))  # 我的理解是 不是所有的参数都要被传进去？

    # 下面是要把所有的文章都加载进去
    '''
    posts = Post.query.order_by(Post.time_stamp.desc()).all()
    return render_template('index.html',form=form,posts=posts)
    '''
    # 那么关于分页，到底是怎么做的？
    page = request.args.get('page', 1, type = int)
    pagination = Post.query.order_by(Post.time_stamp.asc()).paginate(page,
                    per_page = current_app.config['FLASK_POSTS_PER_PAGE'], error_out = False)

    posts = pagination.items
    return render_template('index.html', form = form, posts = posts,
                           pagination = pagination)


'''
@main.route('/user/<username>')
@login_required
def index():
    return render_template('user.html',username=username)
'''

# 看到了吧，如果是自己来写的话，第一次肯定不好，所以自己还是要多加练习
# 要对内部的逻辑结构更加清楚
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.time_stamp.desc()).all()
    return render_template('user.html', user = user, posts = posts)


@main.route('/edit-profile/<username>', methods = ['GET', 'POST'])
@login_required
def edit_profile(username):
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('修改资料成功')
        return redirect(url_for('main.user', username = current_user.username))
    form.name.data = current_user.username
    form.about_me.data = current_user.about_me
    return render_template('edit_user.html', form = form)


# 同时要保证为每篇博客生成唯一的链接
@main.route('/post/<int:id>',methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment=Comment(body = form.body.data,
                        author = current_user._get_current_object(),
                        post = post)
        db.session.add(comment)
        db.session.commit()
        flash('评论发表成功')
        return redirect(url_for('main.post',id = id))
    return render_template('post.html', posts = [post],form=form)


# 将post作为列表传进去，可以使用 _post.html

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
        '''
    f = Follow(followers = current_user, followed = user)
    db.session.add(f)
    db.session.commit()
    '''
    current_user.follow(user)
    flash('已成功关注')
    return redirect(url_for('main.user', username = username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    f = current_user.followed.filter_by(followed_id = user.id).first()
    db.session.delete(f)
    db.session.commit()

    flash('已经取消关注')
    return redirect(url_for('main.user', username = username))
    # return render_template('user.html',user=user)


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username = username).first()
    # 因为在查看的时候还有分页，所以就，恩，分页的内容之后再说
    # 自己先完成自己的内容
    return render_template('followers.html', user = user)

'''
@main.route('/get')
def getdmozdata():
    dmoz = Dmoz.query.all()
    return render_template('dmoz.html',dmoz=dmoz)
'''