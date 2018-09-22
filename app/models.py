from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.chanels import chanel_list
from app.themes import themes_list
from sqlalchemy.exc import IntegrityError


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rss_chanel_id = db.Column(db.Integer, db.ForeignKey('chanels.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(64), index=True)
    admin = db.Column(db.Boolean, default=False)
    theme = db.Column(db.Integer, db.ForeignKey('themes.id'), default=5)

    chanels = db.relationship('Follow', foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic', cascade='all, delete-orphan'
                              )

    @property
    def password(self):
        raise AttributeError('password not saved in db')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, chanel):
        if not self.is_following(chanel):
            f = Follow(follower=self, chanel=chanel)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, chanel):
        f = self.chanels.filter_by(rss_chanel_id=chanel.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self, chanel):
        return Follow.query.filter_by(follower_id=self.id, rss_chanel_id=chanel.id).first() is not None


class RSSChanel(db.Model):
    __tablename__ = 'chanels'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    reference = db.Column(db.String(1024), index=True, unique=True)
    chanelname = db.Column(db.String(64), index=True, unique=True)

    followers = db.relationship('Follow', foreign_keys=[Follow.rss_chanel_id],
                               backref=db.backref('chanel', lazy='joined'),
                               lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def add_chanels():
        for reference, chanelname in chanel_list.items():
            chanel = RSSChanel(reference=reference,
                               chanelname=chanelname)
            try:
                db.session.add(chanel)
            except IntegrityError:
                db.session.rollback()
            else:
                db.session.commit()


class Theme(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    themename = db.Column(db.String(64), index=True, unique=True)
    reference = db.Column(db.String(1024), index=True, unique=True)

    users = db.relationship('User', backref='current_theme', lazy='dynamic')

    @staticmethod
    def add_themes():
        for reference, themename in sorted(themes_list.items(), key=lambda x: x[1]):
            theme = Theme(reference=reference,
                          themename=themename)
            try:
                db.session.add(theme)
            except IntegrityError:
                db.session.rollback()
            else:
                db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
