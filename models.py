from google.appengine.ext import db


class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    author = db.UserProperty(required=True, auto_current_user=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_updated = db.DateTimeProperty(auto_now=True)

