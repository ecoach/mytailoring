from django.conf.urls.defaults import patterns, include, url
from mycoach5.views import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import redirect_to

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
    url(r'^mts5/admin/', include(admin.site.urls)),

    # login
    url(r'^mts5/login/$', 'django.contrib.auth.views.login', {'template_name': 'mycoach5/login.html'}),
    url(r'^mts5/logout', mylogout),

    # surveys
    url(r'^mts5/Opt_In/(?P<page_id>.*)$', login_required(Opt_Out_Survey_View.as_view())),
    url(r'^mts5/Initial_Survey/(?P<page_id>.*)$', login_required(Advice_1_Survey_View.as_view())),
    url(r'^mts5/Exam_1_Prep_Survey/(?P<page_id>.*)$', login_required(Exam_1_Prep_Survey_View.as_view())),
    url(r'^mts5/Exam_1_Response_Survey/(?P<page_id>.*)$', login_required(Exam_1_Response_Survey_View.as_view())),
    url(r'^mts5/Exam_2_Response_Survey/(?P<page_id>.*)$', login_required(Exam_2_Response_Survey_View.as_view())),
    url(r'^mts5/Exam_2_Response_Survey_Testimonial/(?P<page_id>.*)$', login_required(Exam_2_Response_Survey_Testimonial_View.as_view())),
    url(r'^mts5/Exam_3_Response_Survey/(?P<page_id>.*)$', login_required(Exam_3_Response_Survey_View.as_view())),
    url(r'^mts5/Final_Exam_Response_Survey/(?P<page_id>.*)$', login_required(Final_Exam_Response_Survey_View.as_view())),

    # staff
    url(r'^mts5/staff/message_viewer/', login_required(Message_Viewer_View.as_view()), name='none'),
    url(r'^mts5/staff/copy_student/', login_required(Copy_Student_View.as_view()), name='none'),
    url(r'^mts5/staff/usage_stats/', login_required(Usage_Stats_View.as_view()), name='none'),
    url(r'^mts5/staff/email_students/', login_required(Email_Students_View.as_view()), name='none'),
    url(r'^mts5/staff/data_loader/file_upload/', login_required(data_loader_file_upload), name='data_loader_file_upload'),
    url(r'^mts5/staff/data_loader/mp_map_download/', login_required(mp_map_download), name='mp_map_download'),
    url(r'^mts5/staff/data_loader/file_review/', login_required(data_loader_file_review), name='data_loader_file_review'),
    url(r'^mts5/staff/data_loader/data_digest/', login_required(data_loader_data_digest), name='data_loader_data_digest'),
    url(r'^mts5/staff/data_loader/mts_load/', login_required(data_loader_mts_load), name='data_loader_mts_load'),
    url(r'^mts5/staff/data_loader/archive/', login_required(data_loader_archive), name='data_loader_archive'),
    url(r'^mts5/staff/data_loader/help/', login_required(data_loader_help), name='data_loader_help'),
    url(r'^mts5/staff/data_loader/', login_required(data_loader_file_upload), name='data_loader'),
    url(r'^mts5/staff/', login_required(Gen_Staff_View), name='gen_staff_view'),

    # services
    url(r'^mts5/download_analysis_db/', login_required(Download_Analysis_View), name='download_lite_db'),
    url(r'^mts5/download_mysql_db/', login_required(Download_Mysql_View), name='download_mysql'),
    url(r'^mts5/use_data.log/$', login_required(Use_View), name='none'),
    url(r'^mts5/', login_required(ECoach_Message_View.as_view()), name='home'),
)


