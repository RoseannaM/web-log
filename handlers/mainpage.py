"""Mainpage handler"""
from handlers import Handler

class MainPage(Handler):
    """This is the main page of our app"""
    def get(self):
        """renders the welcome page"""
        #if the user is currently logged in, redirect to the blog page
        if self.user:
            self.redirect("/blog")
        else:
            self.render("blog_welcome_page.html")
