from django.conf.urls.defaults import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # surveys
    #url(r'^survey/(?P<page_id>.*)$', login_required(survey_view), name='survey_view'),

    # messages
    url(r'^message/(?P<msg_id>.*)$', login_required(message_view), name='message_view'),
    # re-use the message view to view surveys
    url(r'^survey/(?P<survey_id>.*)$', login_required(survey_preview_view), name='survey_preview'),
    url(r'^', login_required(message_view), {'msg_id': ''}, name='default'),
    #url(r'^', login_required(ECoach_Message_View.as_view()), name='home'),
)


