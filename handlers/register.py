"""Register handler"""

#models
from models import User

#handlers
from handlers import SignUpHandler

class Register(SignUpHandler):
    """Register handler"""
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
            