"""Main file"""
import webapp2  # pylint: disable=E0401

#handlers
from handlers import MainPage, Register, Login, Logout, BlogFront, DeletePost
from handlers import NewPost, PostPage, LikePost, Comment, EditComment, DeleteComment, EditPost

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Register),
    ('/login', Login),
    ('/blog/?', BlogFront),
    ('/blog/newpost', NewPost),
    ('/blog/([0-9]+)', PostPage),
    ('/blog/([0-9]+)/editpost', EditPost),
    ('/blog/([0-9]+)/like', LikePost),
    ('/blog/([0-9]+)/deletepost', DeletePost),
    ('/blog/([0-9]+)/addcomment', Comment),
    ('/blog/([0-9]+)/editcomment', EditComment),
    ('/blog/([0-9]+)/deletecomment', DeleteComment),
    ('/logout', Logout),
], debug=True)
