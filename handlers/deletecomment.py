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
        logging.info(postcomment)
        postcomment.delete()
      