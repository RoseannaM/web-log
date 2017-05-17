"""Mainpage handler"""
from handlers import Handler

class MainPage(Handler):
    """This is the main page of our app"""
    def get(self):
        """renders the welcome page"""
        self.render("blog_welcome_page.html")
