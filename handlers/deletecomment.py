"""Delete comment handler"""

from google.appengine.ext import db

from handlers import Handler
from models import Comments
from models import User
from utils import render_str
from utils import blog_key

import logging


class DeleteComment(Handler):
    """This deletes the comment"""

    def get(self, comment_id):
        """render the like page"""
        if not self.user:
            self.redirect("/login")
            return

    def post(self, comment_id):
        # get comment and delete it
        postcomment = Comments.get_by_id(int(comment_id))

        #confirm existance of the comment
        if not postcomment:
            self.error(404)
            return
        user = self.user.name
        post_author = postcomment.user
        #confirm the post exists and the user is the author
        if postcomment and user == post_author:
            postcomment.delete()
      