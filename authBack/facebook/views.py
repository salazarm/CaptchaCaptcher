import urllib
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from fb_graph import GraphAPI
from django.db.models import get_model
from facebook.models import FacebookProfile
from exception import *
import logging


def login_fb(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """
   
    args = {
    'client_id': settings.FACEBOOK_APP_ID,
    'scope': settings.FACEBOOK_SCOPE,
    'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback/')
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))
         

    
def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """
    code = request.GET.get('code')

    try:
        user = authenticate(token=code, request=request)
        if user.is_active:
            login(request, user)
    except:
        pass
    return HttpResponseRedirect("/home/")

def post_to_wall(request):
    try:
        fb_user = FacebookProfile.objects.get(user=request.user)
        graph = GraphAPI(fb_user.access_token)
        graph.put_object("me", "feed", message="Hello from eager panda!")
        state = 'facebook msg posted'
    except FacebookProfile.DoesNotExist:
        state = 'no facebook accnt'

    return HttpResponse(state)
