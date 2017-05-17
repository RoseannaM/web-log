"""The signup handler"""

import re
from handlers import Handler

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    """username check"""
    return username and USER_RE.match(username)

def valid_password(password):
    """password check"""
    return password and PASSWORD_RE.match(password)

def valid_email(email):
    """email check"""
    return not email or EMAIL_RE.match(email)


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
        """signup complete"""
        raise NotImplementedError

