"""Delete post handler"""

from google.appengine.ext import db

from handlers import Handler
from models import Post
from models import User
from utils import render_str
from utils import blog_key

import logging


class DeletePost(Handler):
    """This deletes the post"""
    def get(self, post_id):
        """render the like page"""
        if not self.user:
            self.redirect("/login")
            return

    def post(self, post_id):
        #get post and delete it
        post = Post.get_by_id(int(post_id), parent=blog_key())
        post.delete()
