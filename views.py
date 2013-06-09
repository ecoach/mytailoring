from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.mail import EmailMultiAlternatives
from djangotailoring.views import TailoredDocView
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from mycoach.nav import Nav, Messages, StaffNav, DataLoaderNav
from django.conf import settings
from django.contrib.auth.models import User
from djangotailoring.project import getsubjectloader
from djangotailoring.subjects import DjangoSubjectLoader
from django.views.generic import TemplateView
from mycoach.models import UserProfile
from mydata4.models import Source1
from mycoach.viewmixins import configure_source_data
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from djangotailoring.views import UserProfileSubjectMixin, LoginRequiredMixin
from djangotailoring.surveys.views import SinglePageSurveyView, SimpleSurveyView

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def mylogout(request):
    return HttpResponseRedirect("https://weblogin.umich.edu/cgi-bin/logout")

class ECoach_Message_View(TailoredDocView):
    m_messages = Messages()

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        #Log_Request(request)
        configure_source_data(request.user.username)
        # load the nav object
        self.m_nav = Nav(request.path)
        return super(ECoach_Message_View, self).dispatch(*args, **kwargs)

    @property 
    def message_document(self): 
        msgid = self.m_nav.get_msgdoc()
        msg = self.m_messages.pathto(msgid)
        return "Messages/testing.messages"
        # return "Surveys/testsurvey.survey"

    @property 
    def template_name(self):
        template = 'mycoach/messages.html'
        return template
 
    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Message_View, self).get_context_data(**kwargs)
        context["nav"] = self.m_nav
        return context
 
class ECoach_Single_Survey_Mixin(LoginRequiredMixin, UserProfileSubjectMixin, SinglePageSurveyView):
    m_messages = Messages()
    survey_document = "path/to/survey.survey"
    source = 'sourceTable'
    survey_id = 'uniqueId'

    def dispatch(self, request, *args, **kwargs):
        request = args[0]
        #Log_Request(request)
        # psudo constructor
        # self.m_nav = kwargs.get("nav")
        # HACK-ALERT self.m_nav = kwargs["nav"]
        self.m_nav = Nav(request.path, data_status=4)
        return super(ECoach_Single_Survey_Mixin, self).dispatch(*args, **kwargs)

    @property 
    def template_name(self):
        has_side = self.m_nav.decide_template()
        if has_side: 
            template = 'mycoach/side.html'
        else:
            template = 'new_base.html'
            #template = 'mycoach/surveys.html' 
        return template
 
    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Single_Survey_Mixin, self).get_context_data(**kwargs)
        context["nav"] = self.m_nav
        return context

    def on_valid_submission(self):
        self.save_subject(self.request_subject)

    def handle_end_of_survey(self):
        return redirect('/')

class ECoach_Multi_Survey_Mixin(LoginRequiredMixin, UserProfileSubjectMixin, SimpleSurveyView):
    m_messages = Messages()
    survey_document = "none"
    source = 'none' # example
    survey_id = 'none' # example

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        configure_source_data(request.user.username)
        #Log_Request(request)
        return super(ECoach_Multi_Survey_Mixin, self).dispatch(*args, **kwargs)

    @property 
    def template_name(self):
        template = 'mycoach/surveys.html'
        return template
 
    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Multi_Survey_Mixin, self).get_context_data(**kwargs)
        #context["nav"] = self.m_nav
        return context

    def on_valid_submission(self):
        self.save_subject(self.request_subject)

    def handle_end_of_survey(self):
        return redirect('/')

def Gen_Staff_View(request, **kwargs):
    # authenticate
    staffmember = request.user.is_staff
    if not staffmember:
        #Log_Request(request)
        return redirect('/')

    return render_to_response('staff_page.html', 
        {   'steps': ['Step1: xxx','Step2: xxx',  'Step3: xxx', 'Step4: xxx'], 
            'tasks': ['Email Students', 'Site Statistics', 'Upload Data', 'Export Data']
        })


class Survey01_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey01.survey"
    source = 'Source1'
    survey_id = 'Survey01'
    # HACK-ALERT - set the property which makes survey re-take-able
   
    def dispatch(self, request, *args, **kwargs):
        # psudo constructor
        return super(Survey01_View, self).dispatch(request, *args, **kwargs)

    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)    
        return redirect(settings.DOMAIN_MTS)


