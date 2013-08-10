from django.db import models
from djangotailoring.userprofile import (BaseUserProfile, register_profile_post_save_handler)
from django.contrib.auth.models import User
import base64
import json
from datetime import datetime

# mydataX imports
from django.conf import settings
from django.utils.importlib import import_module
mydata = import_module(settings.MYDATA)
Source1 = mydata.models.Source1

# Create your models here.

# notes on linking users to courses
# me = request.user
# mc = ECoachCourse(name='physics140', message_project='W_12', term='Winter 2012', department='physics') 
# mc.students.add(me.get_profile()) 
# mc.save

class UserProfile(BaseUserProfile):
    @property
    def tailoringid(self):
        return self.user.username

    #enrolled = models.NullBooleanField()

    #<user preferences>
    _prefs = models.TextField(db_column='_prefs', blank=True)

    def set_pref(self, data):
        if type(data) is dict:
            self._prefs = base64.encodestring(json.dumps(data))

    def get_pref(self):
        ret = dict()
        try: # avoid null issues, and any others
            ret = json.loads(base64.decodestring(self._prefs))
        except:
            pass
        return ret

    # dictionary of preferences
    prefs = property(get_pref, set_pref)
    #</user preferences>

    # Must specify related_name on all relations.
    #courses = models.ManyToManyField(ECoachCourse, related_name='students') 
    #courses = models.ManyToManyField('myselector.ECoachCourse', related_name='students', through='user_id') 

register_profile_post_save_handler(UserProfile)


