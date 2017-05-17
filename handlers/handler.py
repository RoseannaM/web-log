"""the main handler"""

import hmac
import webapp2  # pylint: disable=E0401

from google.appengine.ext import db


from env import get_secret

from utils import jinja_env

from models import User
#from models import Post


#this is the hmac secret var, it is stored in a seperate file 
#not included in the public repo. Please create your own secret :)
secret = get_secret()


def hash_str(s):
    """secure value with secret"""
    return hmac.new(secret, s).hexdigest()

def make_secure_val(s):
    """returns the secure value"""
    return  "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    """confirms the secure val"""
    array = h.split("|")[0]
    if h == make_secure_val(array):
        return array

class Handler(webapp2.RequestHandler):

    """Creates main page content"""
    def write(self, *a, **kw):
        """Creates text"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """template"""
        params['user'] = self.user
        tem = jinja_env.get_template(template)
        return tem.render(params)

    def login(self, user):
        self.set_cookie('user_id', str(user.key().id()))

    def logout(self):
        """Logout"""
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def set_cookie(self, name, value):
        """set the cookies"""
        cookie_value = make_secure_val(value)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_value))

    def read_cookie(self, name):
        """confirms cookie is secure"""
        cookie_value = self.request.cookies.get(name)
        return cookie_value and check_secure_val(cookie_value)

    def render(self, template, **kw):
        """render template"""
        self.write(self.render_str(template, **kw))

    def initialize(self, *a, **kw):
        """initalise the app"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

        