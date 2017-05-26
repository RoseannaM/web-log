"""List of blogs handler"""

from handlers import Handler
from google.appengine.ext import db

class BlogFront(Handler):
    """Front page of blogs"""
    def get(self):
        if not self.user:
            self.redirect("/login")
            return
        """"Get the posts"""
        #select the posts from the db, send to template
        posts = db.GqlQuery("select * from Post order by created desc")
        self.render('blog_front_page.html', posts=posts, user=self.user)
        