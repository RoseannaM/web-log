"""Edit post handler"""
from google.appengine.ext import db

import cgi
from models import Post
from models import Likes
from handlers import Handler
from utils import blog_key

import logging


class EditPost(Handler):
    """View single post page handler"""

    def get(self, post_id):
        if not self.user:
            self.redirect("/login")
            return
        """Blog post"""
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        cssid = str(post.key().id())
        if not post:
            self.error(404)
            return
        if self.user:
            subject = post.subject
            content = post.content
            author = post.author
            self.render("blog_edit_post_page.html", key=post_id, subject=subject,
                        content=content, author=author, user=self.user)
        else:
            self.redirect("/login")

    def post(self, post_id):
        """Add Edited-Post in db"""
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
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            user = self.user.name
            post_author = post.author

            #confirm the post exists and the user is the author
            if post and user == post_author:

                post.content = content
                post.subject = subject
                post.put()

                self.redirect('/blog/%s' % str(post.key().id()))
        else:
            if subject:
                error = "Content not included"
            if content:
                error = "Subject not included"
            else:
                error = "Subject  and Content not included"
                
            self.render("blog_edit_post_page.html", key=post_id, subject=subject,
                        content=content, author=author, error=error)
