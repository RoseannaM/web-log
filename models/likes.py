"""The Like model"""

from google.appengine.ext import db

class Likes(db.Model):
    """The Like model"""
    #the user who liked the post
    user = db.StringProperty(required=True)
    #the post that was liked
    post = db.IntegerProperty(required=True)

