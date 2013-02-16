from django.db import models
from djangotailoring.userprofile import (BaseUserProfile, register_profile_post_save_handler)
from django.contrib.auth.models import User
import base64
import json
from datetime import datetime

from mydata5.models import Source1

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

# model for logging user data
class ELog(models.Model):
    who = models.ForeignKey(User, to_field='username', db_column='who') 
    mwhen = models.DateTimeField()
    what = models.CharField(max_length=200)

class Survey_Log(models.Model):
    who = models.ForeignKey(User, to_field='username', db_column='who') 
    mwhen = models.DateTimeField()
    survey = models.CharField(max_length=200)

class CsvDataFile(models.Model):
    # [12m Digestion__data_file] 
    path = models.CharField(max_length=260)
    name = models.CharField(max_length=260)

    def __unicode__(self):
        return str(self.id) + '_' + self.name

    def disk_name(self):
        return self.__unicode__()
    
class CsvMapFile(models.Model):
    # [12m Digestion__map_file]
    path = models.CharField(max_length=260)
    name = models.CharField(max_length=260)

    def __unicode__(self):
        return str(self.id) + '_' + self.name

    def disk_name(self):
        return self.__unicode__()

DIGESTION_FUNCTION_CHOICES = (
    ('sum', 'Sum([cols])'),
    ('avg', 'Average([cols])'),
    ('pick', 'Pick(col)'),
)

class Digestion(models.Model):
    # [12m Digestion_Column__digestion]
    user = models.ForeignKey(User, to_field='username') 
    created = models.DateTimeField(auto_now=False,blank=True, null=True)
    name = models.CharField(max_length=100)
    map_file = models.ForeignKey(CsvMapFile, null=True)
    data_file = models.ForeignKey(CsvDataFile, null=True)
    data_file_id_column = models.IntegerField(null=True)
    function = models.IntegerField(null=True)
    inserts = models.IntegerField(null=True)
    overwrites = models.IntegerField(null=True)
    mts_characteristic = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.id) + '_' + self.name

    def get_name(self):
        return self.__unicode__()

    def get_id_column(self):
        if self.data_file_id_column > 0:
            return self.data_file_id_column
        else:
            self.data_file_id_column = 1
            self.save()
            return self.data_file_id_column 
    
class Digestion_Column(models.Model):
    column_number = models.IntegerField()
    digestion = models.ForeignKey(Digestion)


