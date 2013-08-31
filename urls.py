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
    url(r'^message/(?P<msg_id>.*)/$', login_required(Single_Message_View.as_view()), {'template': 'mycoach/messages.html'}, name='message_view'),
    url(r'^messageframe/(?P<msg_id>.*)/$', login_required(Single_Message_View.as_view()), {'template': 'mycoach/messageframe.html'}, name='message_frame_view'),

    # surveys
    url(r'^survey/(?P<survey_id>.*)/(?P<page_id>.*)$', login_required(Single_Survey_View.as_view()), {'template': 'mycoach/surveys.html'}),
    url(r'^surveyframe/(?P<survey_id>.*)/(?P<page_id>.*)$', login_required(Single_Survey_View.as_view()), {'template': 'mycoach/surveyframe.html'}),

    # re-use the message view to view surveys
    url(r'^', login_required(Single_Message_View.as_view()), {'msg_id': 'home', 'template': 'mycoach/messages.html'}, name='default'),
)


