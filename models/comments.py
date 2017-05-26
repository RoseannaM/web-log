"""The comments model"""

from google.appengine.ext import db
from utils import render_str

import logging

class Comments(db.Model):
    """The Comments model"""
    #the user who created the comment
    user = db.StringProperty(required=True)
    #the post that was commented on
    post = db.IntegerProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self, user):
        """render comment"""
        # this is the comment key, not the post key
        key = self.key().id_or_name()
        blogkey = self.post

        #check if user has commeneted on the post, set bool
        # commented = Comments.all(keys_only=True).filter('post =', blogkey).filter(
        #     'user =', user.name).get() != None

        blogcomments = Comments.all()
        postcomments = blogcomments.filter('post =', blogkey).get()

        # if postcomments.post == blogkey and postcomments.user == user.name:
        #     commented = True
        # else:
        #     commented = False

        self._render_text = self.content.replace('\n', '<br>')
        return render_str("blog_comment_page.html", c=self, blogkey=blogkey, user=user.name, key=key)


