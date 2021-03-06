from flask.ext.login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String, Float, SmallInteger, DateTime, Text
from sqlalchemy.orm import relationship
from pyhackers.db import DB as db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nick = Column(db.Text, unique=True, index=True)
    email = Column(db.Text, index=True, unique=True)
    password = Column(db.Text)
    first_name = Column(db.Text, nullable=True)
    last_name = Column(db.Text, nullable=True)

    follower_count = Column(Integer, nullable=True)
    following_count = Column(Integer, nullable=True)

    lang = Column(String(5), nullable=True)
    loc = Column(String(50), nullable=True)

    pic_url = Column(String(200))

    role = Column(db.Integer, default=1, nullable=False)

    social_accounts = relationship('SocialUser', lazy='dynamic')

    def __str__(self):
        return unicode(self.nick)

    def __repr__(self):
        return unicode(self.jsonable())

    def jsonable(self):
        return dict(
            id=self.id,
            nick=self.nick,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            followers=self.follower_count,
            following=self.following_count,
            lang=self.lang,
            loc=self.loc,
            picture=self.pic_url
        )


class SocialUser(db.Model):
    __tablename__ = 'social_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    email = Column(String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relation(User)
    nick = Column(String(64), index=True)
    acc_type = Column(String(2), nullable=False)
    follower_count = Column(Integer, nullable=True)
    following_count = Column(Integer, nullable=True)
    ext_id = Column(String(50))
    access_token = Column(String(100))
    hireable = Column(Boolean)

    def __repr__(self):
        return '<SocialUser %s-%s->' % (self.acc_type, self.user_id)


def new_user(nick, email):
    u = User()
    u.nick = nick
    u.email = email
    db.session.add(u)
    db.session.commit()