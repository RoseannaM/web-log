"""View single post page handler"""

from google.appengine.ext import db
from handlers import Handler
from utils import blog_key

class PostPage(Handler):
    """Post page"""
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
            self.render("blog_post_permalink.html", post=post, cssid=cssid, user=self.user)
        else:
            self.redirect("/login")
