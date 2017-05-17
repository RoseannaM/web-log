"""logout handler"""

from handlers import Handler
from google.appengine.ext import db


class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')


