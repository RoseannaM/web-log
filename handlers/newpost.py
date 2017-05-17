"""Creat new post handler"""

import cgi
from models import Post
from models import Likes
from handlers import Handler
from utils import blog_key

import logging


class NewPost(Handler):
    """On post creation redirect to the post"""
    def get(self):
        """render the post"""
        if self.user:
            self.render("blog_newpost_page.html")
        else:
            self.redirect("/login")

    def post(self):
        """Create Post in db"""
        logging.info("newpost")
        if not self.user:
            self.redirect('/blog')
            return

        subject = self.request.get("subject")
        content = self.request.get("content")
        author = self.user.name

        #escaping the html to avoid xss
        escaped_sub = cgi.escape(subject)
        escaped_cont = cgi.escape(content)

        if subject and content and author:
            post = Post(parent=blog_key(), subject=escaped_sub, content=escaped_cont, author=author)
            post.put()

            self.redirect('/blog/%s' % str(post.key().id()))
        else:
            error = "Subject and content not included"
            self.render("blog_newpost_page.html", subject=subject,
                        content=content, author=author, error=error)
