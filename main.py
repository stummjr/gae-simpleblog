# -*- encoding:utf-8 -*-
import os
import webapp2
from models import BlogPost
from google.appengine.api import users
from google.appengine.ext.webapp import template


template_dir = os.path.join(os.path.dirname(__file__), 'templates')


class BlogMainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write(
            template.render(template_dir + '/front.html',
                            {'posts': BlogPost.all()}))


class BlogPostViewHandler(webapp2.RequestHandler):

    def get(self, post_id=None):
        if post_id is not None:
            try:
                post = BlogPost.get_by_id(int(post_id))
                self.response.out.write(
                    template.render(template_dir + '/detail.html',
                                    {'post': post}))
            except:
                self.response.out.write("Erro: post não encontrado!")


class BlogNewPostHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user is not None:
            self.response.out.write(
                template.render(template_dir + '/form.html',
                                {'title': 'Escrever post'}))
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        author = users.get_current_user()
        if author is not None:
            subject = self.request.get('subject')
            content = self.request.get('content')
            if subject and content:
                b = BlogPost(subject=subject, content=content)
                b.put()
                self.redirect("/blog/post/" + str(b.key().id()))
            else:
                error = 'Ambos os campos são obrigatórios'
                self.response.out.write(
                    template.render(template_dir + '/form.html',
                                    {'title': 'Escrever post', 'error': error,
                                     'subject': subject, 'content': content}))
        else:
            self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication(
    [("/blog", BlogMainHandler),
     ("/blog/newpost", BlogNewPostHandler),
     ('/blog/post/(\d+)', BlogPostViewHandler),
     ],
    debug=True)
