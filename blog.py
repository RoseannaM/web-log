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

# from env import get_secret

#this is the hmac secret var, it is stored in a seperate file 
#not included in the public repo. Please create your own secret :)
# secret = get_secret()

hash_secret = "thisisasecret"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

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

def valid_username(username):
    """username check"""
    return username and USER_RE.match(username)


def valid_password(password):
    """password check"""
    return password and PASSWORD_RE.match(password)

def valid_email(email):
    """email check"""
    return not email or EMAIL_RE.match(email)


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

class MainPage(Handler):
    """This is the main page of our app"""
    def get(self):
        """renders the welcome page"""
        self.render("blog_welcome_page.html")

# user info
def make_salt():
    """creates the salt"""
    salt = ""
    for i in range(5):
        salt += random.choice(string.letters)
    return salt

def make_pw_hash(name, pw, salt=None):
    """hashes the password"""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    """validates the password on signin"""
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

def users_key(group = 'default'):
    """Create the user key"""
    return db.Key.from_path('users', group)

class User(db.Model):
    """creates our user in the database"""
    #email is optional
    email = db.StringProperty()
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

    @classmethod
    def by_id(cls, uid):
        """get user by id classmethod"""
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """get user by name"""
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """create new user"""
        password = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    name=name,
                    password=password,
                    email=email)

    @classmethod
    def login(cls, name, pw):
        """user login in"""
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.password):
            return u

class SignUpHandler(Handler):
    """Sign up page"""
    def get(self):
        """creating the form"""
        self.render('blog_signup_page.html')

    def post(self):
        """This is setting the signup post"""
        is_error = False
        self.user_name = self.request.get('username')
        self.user_password = self.request.get('password')
        self.user_verifiy = self.request.get('verify')
        self.user_email = self.request.get('email')

        username_error = ""
        password_error = ""
        email_error = ""
        verify_error = ""

        if not valid_username(self.user_name):
            username_error = "Not a valid username"
            is_error = True

        if not valid_password(self.user_password):
            password_error = "Not a valid password"
            is_error = True

        if self.user_password != self.user_verifiy:
            verify_error = "Passwords do not match"

        # check if email is entered and vaild, optional field
        if self.user_email and not valid_email(self.user_email):
            email_error = "The email is not valid"
            is_error = True

        if is_error:
            self.render('blog_signup_page.html',
                        name=self.user_name,
                        username_error=username_error,
                        password_error=password_error,
                        verify_error=verify_error,
                        email_error=email_error)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

class Register(SignUpHandler):
    def done(self):
        """"Register new user method"""
        u = User.by_name(self.user_name)
        if u:
            msg = 'That user already exists.'
            self.render('blog_signup_page.html', username_error=msg)
        else:
            u = User.register(self.user_name, self.user_password, self.user_email)
            #add user to the datatbase
            u.put()
            #log the user in
            self.login(u)
            self.redirect('/blog')

class Login(Handler):
    """Login page"""
    def get(self):
        """Login page render"""
        self.render('blog_login_page.html')

    def post(self):
        """Login page post"""
        user_name = self.request.get('username')
        user_password = self.request.get('password')

        u = User.login(user_name, user_password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('blog_login_page.html', name=user_name, error=msg)

class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')

def blog_key(name='default'):
    """Sets value of the blog's parent"""
    return db.Key.from_path('blogs', name)

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

class BlogFront(Handler):
    """Front page of blogs"""
    def get(self):
        """"Get the posts"""
        #select the posts from the db, send to template
        posts = db.GqlQuery("select * from Post order by created desc")
        self.render('blog_front_page.html', posts=posts)

class PostPage(Handler):
    """Post page"""
    def get(self, post_id):
        """Blog post"""
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        cssid = str(post.key().id())
        logging.info(cssid)
        if not post:
            self.error(404)
            return
        self.render("blog_post_permalink.html", post=post, cssid=cssid)

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
        if not self.user:
            self.redirect('/blog')
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "Subject and content not included"
            self.render("blog_newpost_page.html", subject=subject, content=content, error=error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Register),
    ('/login', Login),
    ('/blog/?', BlogFront),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/newpost', NewPost),
    ('/logout', Logout),
], debug=True)
