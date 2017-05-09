"""Main file"""
import logging

from google.appengine.ext import db

import os
import string
import webapp2  # pylint: disable=E0401
import jinja2
import re
import random
import hashlib
import hmac
from string import letters

class Post(db.Model):
    """The Post model"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        """Renders each blog post"""
        key = self.key().id_or_name()
        logging.info(key)
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("blog_post_page.html", p=self,key=key)