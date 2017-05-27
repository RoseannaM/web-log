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
        """delete the post"""
        #check user is logged in
        if not self.user:
            self.redirect("/login")
            return

        post = Post.get_by_id(int(post_id), parent=blog_key())
        user = self.user.name
        post_author = post.author
        #confirm the post exists and the user is the author
        if post and user == post_author:
            post.delete()
