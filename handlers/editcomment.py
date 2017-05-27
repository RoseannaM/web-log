"""Edit comment handler"""
from google.appengine.ext import db

import cgi
from models import Comments
from models import Likes
from handlers import Handler
from utils import blog_key

import logging


class EditComment(Handler):
    """Render single comment handler"""

    def get(self, comment_id):
        """Blog post"""
        if not self.user:
            self.redirect("/login")
            return
        comment = Comments.get_by_id(int(comment_id))

        if not comment:
            self.error(404)
            return

        if self.user:
            content = comment.content
            post_id = comment.post
            self.render("blog_editcomment_page.html", key=post_id,
                        content=content, user=self.user)
        else:
            self.redirect("/login")

    def post(self, comment_id):
        """Add Edited-comment to db"""

        if not self.user:
            self.redirect('/blog')
            return

        content = self.request.get("content")
        author = self.user.name

        #escaping the html to avoid xss
        escaped_cont = cgi.escape(content)

        comment = Comments.get_by_id(int(comment_id))

        if content:
            user = self.user.name
            comment_author = comment.user

            #confirm the comment exists and the user is the author
            if comment and user == comment_author:

                comment.content = content
                comment.put()
                self.redirect('/blog/%s' % comment.post)

        else:
            error = "Content not included"
            self.render("blog_editcomment_page.html", key=comment.post, error=error)
       