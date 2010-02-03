# coding=UTF8
#import os
import urllib2
#from django.template import 
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from core.models import Renjianer

def indexRequest(request):
    # SELECT * FROM Renjianer ORDER BY date DESC LIMIT 10
    rens = Renjianer.objects.order_by('-date')[0:10]
    rens.query.group_by = ['user_name']
    return render_to_response('index.html', {"rens": rens})

def neighbourhood(request):
    if request.method == 'POST':
        screen_name = request.POST.get('content').lstrip().rstrip()
        if not screen_name:
            return HttpResponseRedirect('/error?message=Did you input anything?')
        #raise NameError(screen_name)
        rnjn_url = 'http://api.renjian.com/'
        # 1、请求user信息
        user_url = rnjn_url + 'users/show.json?id=' + screen_name.encode('UTF-8')
        try:
            retval = urllib2.urlopen(user_url)
            json = retval.read()
            you = simplejson.loads(json, encoding='UTF-8')
            ren = Renjianer()
            ren.user_name = you['screen_name']
            ren.user_id = you['id']
        except urllib2.HTTPError, ex:
            you = {'error': 'API request result: ' + unicode(ex.code)}
            left = {'error': 'Fetching your infomation fail.' }
            right = {'error': 'Fetching your infomation fail.' }
        except ValueError, ex:
            return HttpResponseRedirect('/error?message=User [' + screen_name + '] may not exist. (' + ex.message + ')')
        
        if not you.has_key('error'):
            # 2、请求左边用户信息
            user_url = rnjn_url + 'users/show.json?id=' + unicode(ren.user_id - 1);
            try:
                retval = urllib2.urlopen(user_url)
                json = retval.read()
                left = simplejson.loads(json, encoding='UTF-8')
                ren.left_name = left['screen_name']
                ren.left_id = left['id']
            except urllib2.HTTPError, ex:
                left = {'error': 'API request result: ' + unicode(ex.code)}
            # 3、请求右边用户信息
            user_url = rnjn_url + 'users/show.json?id=' + unicode(ren.user_id + 1);
            try:
                retval = urllib2.urlopen(user_url)
                json = retval.read()
                right = simplejson.loads(json, encoding='UTF-8')
                ren.right_name = right['screen_name']
                ren.right_id = right['id']
            except urllib2.HTTPError, ex:
                right = {'error': 'API request result: ' + unicode(ex.code)}
            # 4、放入数据库
            if ren:
                ren.save()

        if you.has_key('error'):
            you['message'] = "Fetching your infomation fail!\n Did you spell your screen_name or id correctly?"
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
#        self.redirect('/error?message=' + 'Exception: ' + unicode(ex));
#        return


def users(request):
    rens = Renjianer.objects.all().order_by('-date').distinct(True)
    return render_to_response('users.html', {"rens": rens})

def error(request):
    return render_to_response('error.html', {'message': request.GET.get('message'),})