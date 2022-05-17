from . import db, login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    bio = db.Column(db.String(255),default ='My default Bio')
    profile_pic_path = db.Column(db.String(150),default ='default.png')
    secure_password = db.Column(db.String, nullable=False)
    blogs=db.relationship('Blogs', backref='user')
    comment=db.relationship('Comments', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("You can't read the password")

    @password.setter
    def password(self,password):
        self.secure_password=generate_password_hash(password)   

    def verify_password(self,password):
        return check_password_hash(self.secure_password,password) 
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"User('{self.name}')"


class Blogs(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))  
    comments = db.relationship('Comments', backref='comments', lazy='dynamic')

    def __init__(self, heading,  body, user_id):
        self.heading = heading
        self.body = body
        self. user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Comments(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def get_comment(id):
        comment = Comments.query.all(id=id)
        return comment


    def __repr__(self):
        return f'Comment {self.comment}'


class Follower(db.Model):
    __tablename__='follower'

    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True,index=True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Follower {self.email}'