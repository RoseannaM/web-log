"""The post model"""

from models import Likes
from google.appengine.ext import db

from utils import render_str
import logging

class Post(db.Model):
    """The Post model"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.StringProperty(required=True)

    def render(self, user):
        """Renders each blog post"""
        #get the number of likes from the Likes model to pass
        #to the template
        likes = len(list(Likes.all(keys_only=True).filter('post =', self.key().id_or_name()).run()))

        #check if user has liked the post, set bool

        #need to get this query working, need the current user 
        liked = Likes.all(keys_only=True).filter('post =', self.key().id_or_name()).filter(
            'user =', user.name).get() != None

        logging.info(user)
        logging.info(liked)

        key = self.key().id_or_name()
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("blog_post_page.html", p=self, likes=likes, liked=liked, key=key)

