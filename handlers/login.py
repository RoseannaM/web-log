from handlers import Handler
from models import User

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
