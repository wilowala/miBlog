
from . import main
from flask import render_template, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..requests import get_quotes
from ..models import Follower, User, Comments, Blogs
from .. import db
from .forms import UpdateProfile, CreatePost, ContactForm
import secrets
import os
from PIL import Image

@main.route('/')
def home():
    blogs = Blogs.query.all()
    arr =  []
    for blog in blogs:
        arr.append({'heading': blog.heading,'body':blog.body})
    print(arr)
    return render_template('index.html', blogs=arr)

@main.route('/quotes')
def quotes():
    quotes = get_quotes()
    return render_template('quotes.html', quotes = quotes)

@main.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html',form=form )


@main.route('/profile',methods = ['POST','GET'])
@login_required
def profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.profile_pic_path = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Succesfully updated your profile')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    profile_pic_path = url_for('static', filename='assets/'+ User.profile_pic_path) 
    return render_template('profile/profile.html',  form = form, profile_pic_path=profile_pic_path)

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/updateprofile.html',form =form)


@main.route('/new-blog', methods=['POST','GET'])
@login_required
def new_blog():
    followers = Follower.query.all()
    form = CreatePost()
    if form.validate_on_submit():
        heading = form.heading.data
        body = form.body.data
        user_id =  current_user._get_current_object().id
        blog = Blogs(heading=heading,body=body,user_id=user_id)
        blog.save()
        flash('You Posted a new Blog')
        return redirect(url_for('main.home'))
    return render_template('newblog.html', form = form, followers=followers)

@main.route('/blog')
def blog(id):
    comments = Comments.query.filter_by(id).all()
    print(comments)
    return render_template(blogs=blogs, comments=comments)

@main.route('/blog/<blog_id>/update', methods = ['GET','POST'])
@login_required
def updateblog(blog_id):
    blog = Blogs.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = CreatePost()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for('main.blog',id = blog.id)) 
    if request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('newblog.html', form = form)


@main.route('/comment/<blog_id>', methods = ['Post','GET'])
@login_required
def comment(blog_id):
    blog = Blogs.query.get(blog_id)
    comment =request.form.get('newcomment')
    new_comment = Comments(comment = comment, user_id = current_user._get_current_object().id, blog_id=blog_id)
    new_comment.save()
    return redirect(url_for('main.blog',id = blog.id))

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Follower(email = email)
    new_subscriber.save_subscriber()
    # mail_message("Subscribed to D-Blog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/blog/<blog_id>/delete', methods = ['POST','GET'])
@login_required
def delete_post(blog_id):
    blog = Blogs.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))

@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    blogs = Blogs.query.filter_by(user=user).order_by(Blogs.posted.desc()).paginate(page = page, per_page = 4)
    return render_template('userposts.html',blogs=blogs,user = user)