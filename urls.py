from django.conf.urls.defaults import patterns, include, url
from mycoach.views import message_view
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # surveys
    #url(r'^survey/(?P<survey_id>.*)/(?P<page_id>.*)$', login_required(survey_view), name='survey_view'),

    # messages
    #url(r'^(?P<msg_id>.*)$', login_required(message_view), name='message_view'),
    url(r'^(?P<msg_id>.*)$', message_view, name='message_view'),
)


