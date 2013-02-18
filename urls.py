from django.conf.urls.defaults import patterns, include, url
from mycoach5.views import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import redirect_to
from mycoach5 import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ecoach.views.home', name='home'),
    # url(r'^ecoach/', include('ecoach.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^'+settings.URL_SUB+'admin/', include(admin.site.urls)),

    # login
    url(r'^'+settings.URL_SUB+'login/$', 'django.contrib.auth.views.login', {'template_name': 'mycoach/login.html'}),
    url(r'^'+settings.URL_SUB+'logout', mylogout, name='mylogout'),

    # surveys
    url(r'^'+settings.URL_SUB+'Opt_In/(?P<page_id>.*)$', login_required(Opt_Out_Survey_View.as_view())),
    url(r'^'+settings.URL_SUB+'Initial_Survey/(?P<page_id>.*)$', login_required(Advice_1_Survey_View.as_view())),
    url(r'^'+settings.URL_SUB+'Exam_1_Prep_Survey/(?P<page_id>.*)$', login_required(Exam_1_Prep_Survey_View.as_view())),
    url(r'^'+settings.URL_SUB+'Exam_1_Response_Survey/(?P<page_id>.*)$', login_required(Exam_1_Response_Survey_View.as_view())),
    url(r'^'+settings.URL_SUB+'Exam_2_Response_Survey/(?P<page_id>.*)$', login_required(Exam_2_Response_Survey_View.as_view())),
    url(r'^'+settings.URL_SUB+'Exam_2_Response_Survey_Testimonial/(?P<page_id>.*)$', login_required(Exam_2_Response_Survey_Testimonial_View.as_view())),
    url(r'^'+settings.URL_SUB+'Exam_3_Response_Survey/(?P<page_id>.*)$', login_required(Exam_3_Response_Survey_View.as_view())),
    url(r'^'+settings.URL_SUB+'Final_Exam_Response_Survey/(?P<page_id>.*)$', login_required(Final_Exam_Response_Survey_View.as_view())),

    # staff
    url(r'^'+settings.URL_SUB+'staff/message_viewer/', login_required(Message_Viewer_View.as_view()), name='none'),
    url(r'^'+settings.URL_SUB+'staff/copy_student/', login_required(Copy_Student_View.as_view()), name='none'),
    url(r'^'+settings.URL_SUB+'staff/usage_stats/', login_required(Usage_Stats_View.as_view()), name='none'),
    url(r'^'+settings.URL_SUB+'staff/email_students/', login_required(Email_Students_View.as_view()), name='none'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/file_upload/', login_required(data_loader_file_upload), name='data_loader_file_upload'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/mp_map_download/', login_required(mp_map_download), name='mp_map_download'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/file_review/', login_required(data_loader_file_review), name='data_loader_file_review'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/data_digest/', login_required(data_loader_data_digest), name='data_loader_data_digest'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/mts_load/', login_required(data_loader_mts_load), name='data_loader_mts_load'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/archive/', login_required(data_loader_archive), name='data_loader_archive'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/help/', login_required(data_loader_help), name='data_loader_help'),
    url(r'^'+settings.URL_SUB+'staff/data_loader/', login_required(data_loader_file_upload), name='data_loader'),
    url(r'^'+settings.URL_SUB+'staff/', login_required(Gen_Staff_View), name='gen_staff_view'),

    # services
    url(r'^'+settings.URL_SUB+'download_analysis_db/', login_required(Download_Analysis_View), name='download_lite_db'),
    url(r'^'+settings.URL_SUB+'download_mysql_db/', login_required(Download_Mysql_View), name='download_mysql'),
    url(r'^'+settings.URL_SUB+'use_data.log/$', login_required(Use_View), name='none'),
    url(r'^'+settings.URL_SUB+'', login_required(ECoach_Message_View.as_view()), name='home'),
)

