import cgi, urllib, json

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError
import logging
from facebook.models import FacebookProfile
from exception import *


class FacebookBackend:
    def authenticate(self, token=None, request=None):
        """ Reads in a Facebook code and asks Facebook if it's valid and what user it points to. """
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback/'+invite_token+"/"+is_sign_up),
            'code': token,
        }
        # Get a legit access token

        target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
        response = cgi.parse_qs(target)

        
        if not 'access_token' in response:
            raise UserDidNotGivePermissionException
        access_token = response['access_token'][-1]

        # Read the user's profile information
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s&fields=id,username,email,first_name,last_name,gender,birthday' % access_token)
        fb_profile = json.load(fb_profile)

        try:
            # Try and find existing user
            fb_user = FacebookProfile.objects.get(facebook_id=fb_profile['id'])
            user = fb_user.user
            
            fb_user.access_token = access_token
            fb_user.save()

        except FacebookProfile.DoesNotExist:
            
            # Not all users have usernames
            username = fb_profile['id']
            try:
                user = User.objects.get(email = fb_profile['email'])
                fb_user = FacebookProfile(user=user, facebook_id=fb_profile['id'], access_token=access_token)
                fb_user.save()
                return user
            except User.DoesNotExist:
                try:
                    user = User.objects.create_user(username)
                except IntegrityError:
                    # Username already exists, make it unique

                    user = User.objects.create_user(fb_profile['id'], fb_profile['email'])


                
                user.is_active = True # change to false if using email activation
                user.first_name = fb_profile["first_name"]
                user.last_name = fb_profile["last_name"]
                user.set_password("from facebook so doesnt matter")
                user.save()

                fb_user = FacebookProfile(user=user, facebook_id=fb_profile['id'], access_token=access_token)
                fb_user.save()


        return user
 
