"""Comment post handler"""

from google.appengine.ext import db

import cgi
from handlers import Handler

from models import Comments

import logging

from utils import blog_key


class Comment(Handler):

    """On post creation redirect to the comment page"""
    def get(self, post_id):
        """render the comment page"""
        if self.user:
            self.render("blog_newcomment_page.html")
        else:
            self.redirect("/login")

    def post(self, post_id):
        """Create Comment in db"""

        logging.info("comment")
        if not self.user:
            self.redirect('/blog')
            return

        content = self.request.get("content")
        user = self.user.name
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        # blogpost = db.get(key)
        logging.info(user)

        #escaping the html to avoid xss
        escaped_cont = cgi.escape(content)

        if content and user:
            comment = Comments(content=escaped_cont, user=user, post=int(post_id))
            comment.put()

            self.redirect('/blog/%s' % str(post_id))
        else:
            error = "Comment not included"
            self.render("blog_newcomment_page.html", content=content, error=error)
