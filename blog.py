"""Main file"""
import webapp2  # pylint: disable=E0401

#handlers
from handlers import MainPage, Register, Login, Logout, BlogFront, NewPost, PostPage, LikePost

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Register),
    ('/login', Login),
    ('/blog/?', BlogFront),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)/like', LikePost),
    ('/logout', Logout),
], debug=True)
