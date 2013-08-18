from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.conf import settings
from djangotailoring.views import TailoredDocView
from djangotailoring.project import getsubjectloader
from datetime import date
from datetime import datetime
from mynav.nav import main_nav
from .nav import inbox_nav
from djangotailoring.subjects import DjangoSubjectLoader
from djangotailoring.views import UserProfileSubjectMixin, LoginRequiredMixin
from djangotailoring.surveys.views import SinglePageSurveyView, SimpleSurveyView
# mydataX imports
from django.utils.importlib import import_module
mydata = import_module(settings.MYDATA)
#Source1 = mydata.models.Source1
myutils = import_module(settings.MYDATA + '.utils')
configure_source_data = myutils.configure_source_data

class Single_Message_View(TailoredDocView):

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        self.template_name = kwargs['template']
        self.message_document = 'Messages/' + kwargs['msg_id'] + '.messages'
        self.inbox_nav = inbox_nav(request.user, kwargs['msg_id'])
        self.main_nav = main_nav(request.user, 'student_view')
        configure_source_data(request.user.username)
        return super(Single_Message_View, self).dispatch(*args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(Single_Message_View, self).get_context_data(**kwargs)
        context["main_nav"] = self.main_nav
        context["inbox_nav"] = self.inbox_nav
        return context

class Single_Survey_View(LoginRequiredMixin, UserProfileSubjectMixin, SimpleSurveyView):
    survey_document = "none"
    source = 'none' # example
    survey_id = 'none' # example

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        self.template = kwargs['template']
        self.survey_id = kwargs['survey_id']
        self.survey_document = 'Surveys/' + self.survey_id + '.survey'
        if self.survey_id == "CommonSurvey": # hack since this is the only common source survey, for now
            self.source = 'Common1'
        else:
            self.source = 'Source1'
        configure_source_data(request.user.username)
        #Log_Request(request)
        return super(Single_Survey_View, self).dispatch(*args, **kwargs)

    def get_source(self):
        return self.source
    
    def get_survey_document(self):
        return self.survey_document
    
    @property 
    def template_name(self):
        return self.template
 
    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(Single_Survey_View, self).get_context_data(**kwargs)
        #context["nav"] = self.m_nav
        return context

    def on_valid_submission(self):
        self.save_subject(self.request_subject)

    def handle_end_of_survey(self):
        return redirect(reverse('mycoach:default'))


