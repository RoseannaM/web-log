"""Like post handler"""

from google.appengine.ext import db

from handlers import Handler
from models import Likes
from models import User
from utils import render_str
from utils import blog_key

import logging


class LikePost(Handler):
    """This allows liking a post"""

    def get(self, post_id):
        """render the like page"""
        if not self.user:
            self.redirect("/login")
            return

    def post(self, post_id):
        # get post
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        blogpost = db.get(key)

        #confirm existance of the post
        if not blogpost:
            self.error(404)
            return

        author = blogpost.author
        user = self.user.name

        #user can't like their own posts
        if user == author:
            self.error(400)
            return

        #if user is not the author of the post
        if user != author:
            # check if they have allready liked before
            key = str(self.user.key().id_or_name()) + ',' + post_id
            liked = Likes.get_by_key_name(key)

            #if not none, that means user liked allready
            if liked is not None:
                liked.delete()
            else:
                #adding a like with a unique constraint key_name
                likes = Likes(key_name=str(self.user.key().id_or_name()) + ',' + post_id,
                              user=user, post=int(post_id))
                likes.put()


