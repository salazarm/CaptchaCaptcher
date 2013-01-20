import json, urllib
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class FacebookProfile(models.Model):
    user = models.ForeignKey(User)
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150)

    def get_facebook_profile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
        return json.load(fb_profile)

