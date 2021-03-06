# coding=UTF8
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import urlfetch
from django.utils import simplejson

class Renjianer(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    user_name = db.StringProperty()
    user_id = db.IntegerProperty()
    left_name = db.StringProperty()
    left_id = db.IntegerProperty()
    right_name = db.StringProperty()
    right_id = db.IntegerProperty()


class RootHandler(webapp.RequestHandler):

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        rens = db.GqlQuery("SELECT * FROM Renjianer ORDER BY date DESC LIMIT 10")
        template_values = {"rens": rens}
        path = os.path.join(os.path.dirname(__file__), 'template/index.html')
        self.response.out.write(template.render(path, template_values))


class Neighbourhood(webapp.RequestHandler):
    def post(self):
        try:
            screen_name = self.request.get('content')
            #raise NameError(screen_name)
            rnjn_url = u'http://api.renjian.com/'
            # 1、请求user信息
            user_url = rnjn_url + u'users/show.json?id=' + screen_name;
            result = urlfetch.fetch(user_url)
            if result.status_code == 200:
                json = result.content
                you = simplejson.loads(json, encoding='UTF-8')
                ren = Renjianer(key_name=you['screen_name'])
                ren.user_name = you['screen_name']
                ren.user_id = you['id']
            else:
                you = {'error': 'urlfetch result: ' + unicode(result.status_code)}
                left = {'error': 'Fetching your infomation fail.' }
                right = {'error': 'Fetching your infomation fail.' }
            
            if not you.has_key('error'):
                # 2、请求左边用户信息
                user_url = rnjn_url + u'users/show.json?id=' + unicode(ren.user_id - 1);
                result = urlfetch.fetch(user_url)
                if result.status_code == 200:
                    json = result.content
                    left = simplejson.loads(json, encoding='UTF-8')
                    ren.left_name = left['screen_name']
                    ren.left_id = left['id']
                else:
                    left = {'error': 'urlfetch result: ' + unicode(result.status_code)}
                # 3、请求右边用户信息
                user_url = rnjn_url + u'users/show.json?id=' + unicode(ren.user_id + 1);
                result = urlfetch.fetch(user_url)
                if result.status_code == 200:
                    json = result.content
                    right = simplejson.loads(json, encoding='UTF-8')
                    ren.right_name = right['screen_name']
                    ren.right_id = right['id']
                else:
                    right = {'error': 'urlfetch result: ' + unicode(result.status_code)}
                # 4、放入数据库
                ren.put()

            if you.has_key('error'):
                you['message'] = "Fetching your infomation fail!<br /> Did you spell your <strong>screen_name</strong> or <strong>id</strong> correctly?"
            if left.has_key('error'):
                left['message'] = "Finding your left neighbour may got a problem, or you don't even have one :)."
            if right.has_key('error'):
                right['message'] = "Finding your left neighbour may got a problem, or you don't even have one :)."

            template_values = {
                'you': you,
                'left': left,
                'right': right,
                }
            
            path = os.path.join(os.path.dirname(__file__), 'template/result.html')
            self.response.out.write(template.render(path, template_values))
            #self.redirect('/')

        except Exception,ex:
            self.redirect(u'/error?message=' + 'Exception: ' + unicode(ex));
            return


class UsersHandler(webapp.RequestHandler):
    def get(self):
        rens = db.GqlQuery("SELECT * FROM Renjianer ORDER BY date DESC")
        template_values = {"rens": rens}
        path = os.path.join(os.path.dirname(__file__), 'template/users.html')
        self.response.out.write(template.render(path, template_values))


class ErrorHandler(webapp.RequestHandler):
    def get(self):
        self.request.charset = 'UTF-8'
        template_values = {
            'message': self.request.get('message').encode('UTF-8'),
            }
        path = os.path.join(os.path.dirname(__file__), 'template/error.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([
                                          ('/', RootHandler),
                                          ('/neighbourhood', Neighbourhood),
                                          ('/users', UsersHandler),
                                          ('/error', ErrorHandler)
                                         ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
