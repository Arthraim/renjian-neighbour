# coding=UTF8

import cgi
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


class MainHandler(webapp.RequestHandler):

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        rens = db.GqlQuery("SELECT * FROM Renjianer ORDER BY date DESC")
        template_values = {"rens": rens}
        path = os.path.join(os.path.dirname(__file__), 'template/index.html')
        self.response.out.write(template.render(path, template_values))
            

class Neighbourhood(webapp.RequestHandler):
    def post(self):
        ren = Renjianer()
        screen_name = cgi.escape(self.request.get('content'))
        
        rnjn_url = 'http://api.renjian.com/'
        # 1、请求user信息
        user_url = rnjn_url + 'users/show.json?id=' + screen_name;
        result = urlfetch.fetch(user_url)  
        if result.status_code == 200:
            json = result.content
            you = simplejson.loads(str(json))
            ren.user_name = you['screen_name']
            ren.user_id = you['id']
        else:
            you = {'error': str(result.status_code)}
        # 2、请求左边用户信息
        user_url = rnjn_url + 'users/show.json?id=' + str(ren.user_id - 1);
        result = urlfetch.fetch(user_url)  
        if result.status_code == 200:
            json = result.content
            left = simplejson.loads(str(json))
            ren.left_name = left['screen_name']
            ren.left_id = left['id']
        else:
            you = {'error': str(result.status_code)}
        # 3、请求右边用户信息
        user_url = rnjn_url + 'users/show.json?id=' + str(ren.user_id + 1);
        result = urlfetch.fetch(user_url)  
        if result.status_code == 200:
            json = result.content
            right = simplejson.loads(str(json))
            ren.right_name = right['screen_name']
            ren.right_id = right['id']
        else:
            you = {'error': str(result.status_code)}
        
        ren.put()
        
        template_values = {
            'you': you,
            'left': left,
            'right': right,
            }
        
        path = os.path.join(os.path.dirname(__file__), 'template/result.html')
        self.response.out.write(template.render(path, template_values))
        #self.redirect('/')
        
def main():
    application = webapp.WSGIApplication([
                                          ('/', MainHandler),
                                          ('/neighbourhood', Neighbourhood)
                                         ],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
