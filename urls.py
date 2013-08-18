from django.conf.urls.defaults import patterns, include, url
from .views import *
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # messages
    url(r'^message/(?P<msg_id>.*)$', login_required(message_view), name='message_view'),
    url(r'^messageframe/(?P<msg_id>.*)$', login_required(message_frame_view), name='message_frame_view'),
    url(r'^messageframerotating/(?P<rotate_count>.*)/(?P<rotation_start_date>.*)/(?P<rotate_frequency>.*)/(?P<msg_id>.*)$', login_required(message_frame_rotating_view), name='message_view'),

    # surveys
    url(r'^survey/(?P<survey_id>.*)/(?P<page_id>.*)$', login_required(Single_Survey_View.as_view()), {'template': 'mycoach/surveys.html'}),
    url(r'^surveyframe/(?P<survey_id>.*)/(?P<page_id>.*)$', login_required(Single_Survey_View.as_view()), {'template': 'mycoach/surveyframe.html'}),

    # re-use the message view to view surveys
    url(r'^', login_required(message_view), {'msg_id': ''}, name='default'),

)


