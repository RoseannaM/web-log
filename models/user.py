"""User model"""

import random
import hashlib
import string

from google.appengine.ext import db


# user info
def make_salt():
    """creates the salt"""
    salt = ""
    for i in range(5):
        salt += random.choice(string.letters)
    return salt

def make_pw_hash(name, pw, salt=None):
    """hashes the password"""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    """validates the password on signin"""
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

def users_key(group = 'default'):
    """Create the user key"""
    return db.Key.from_path('users', group)


class User(db.Model):
    """creates our user in the database"""
    #email is optional
    email = db.StringProperty()
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

    @classmethod
    def by_id(cls, uid):
        """get user by id classmethod"""
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """get user by name"""
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """create new user"""
        password = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    password=password,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        """user login in"""
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.password):
            return u
