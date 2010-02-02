# coding=UTF8
import os
from django import template
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from core.models import Renjianer

def indexRequest(request):
    # SELECT * FROM Renjianer ORDER BY date DESC LIMIT 10
    rens = Renjianer.objects.order_by('-date')[0:10]
    return render_to_response('index.html', {"rens": rens})

def neighbourhood(request):
    if request.method == 'POST':
        screen_name = request.POST.get('content')
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
        
        return render_to_response('result.html', template_values)

    elif request.method == 'GET':
        return HttpResponseRedirect('/')

#    try:
#    except Exception,ex:
#        self.redirect(u'/error?message=' + 'Exception: ' + unicode(ex));
#        return


def users(request):
    rens = Renjianer.objects.all().order_by('-date').distinct(True)
    return render_to_response('users.html', {"rens": rens})

def error(request):
    return render_to_response('error.html', {'message': request.GET.get('message'),})