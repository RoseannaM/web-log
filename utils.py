"""Global methods"""

import os
import jinja2
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir))

def render_str(template, **params):
    """Render the template"""
    t = jinja_env.get_template(template)
    return t.render(params)

def render(self, template, **kw):
    """render template"""
    self.write(self.render_str(template, **kw))

def blog_key(name='default'):
    """Sets value of the blog's parent"""
    return db.Key.from_path('blogs', name)
