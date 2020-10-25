from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from datetime import datetime

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email = db.Column(db.String(255),unique = True, nullable = False)
    secure_password = db.Column(db.String(255),unique = True,nullable = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    pitchy = db.relationship('Pitchy',backref = 'user',lazy = 'dynamic')
    comment = db.relationship('Comment',backref = 'user',lazy = 'dynamic')
    likes = db.relationship('Likes',backref = 'user',lazy = 'dynamic')
    dislikes = db.relationship('Dislikes',backref = 'user',lazy = 'dynamic')

    # Creating write only class property password
    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password)

    def save_u(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'


class Pitchy(db.Model):
    __tablename__ = 'pitchy'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    post = db.Column(db.String(255),nullable = False)
    comment = db.relationship('Comment',backref = 'pitchy',lazy = 'dynamic')
    likes = db.relationship('Likes',backref = 'pitchy',lazy = 'dynamic')
    dislikes = db.relationship('Dislikes',backref = 'pitchy',lazy = 'dynamic')
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    category = db.Column(db.String(255),index = True,nullable = False)

    def save_p(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitchy {self.post}'


class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    pitchy_id = db.Column(db.Integer,db.ForeignKey('pitchy.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_likes(cls,id):
        likes = Likes.query.filter_by(pitchy_id = id).all()
        return likes
    
    def __repr__(self):
        return f'{self.user_id}:{self.pitchy_id}'

class Dislikes(db.Model):
    __tablename__ = 'dislikes'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    pitchy_id = db.Column(db.Integer,db.ForeignKey('pitchy.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_dislikes(cls,id):
        dislikes = Dislikes.query.filter_by(pitchy_id = id).all()
        return dislikes

    def __repr__(self):
        return f'{self.user_id}:{self.pitchy_id}'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    pitchy_id = db.Column(db.Integer,db.ForeignKey('pitchy.id'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitchy_id):
        comments = Comment.query.filter_by(pitchy_id = pitchy_id).all()
        return comments

    def __repr__(self):
        return f'comment:{self.comment}'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

