from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.conf import settings
from djangotailoring.views import TailoredDocView
from djangotailoring.project import getsubjectloader
from mynav.nav import main_nav
from .nav import inbox_nav
"""
from djangotailoring.subjects import DjangoSubjectLoader
from djangotailoring.views import UserProfileSubjectMixin, LoginRequiredMixin
from djangotailoring.surveys.views import SinglePageSurveyView, SimpleSurveyView
"""

def message_view(request, **kwargs):
    mview = ECoach_Message_View.as_view()
    # hack the default message for now
    if kwargs['msg_id'] != '':
        msg = kwargs['msg_id']
    else:
        msg = 'testing'
    return mview(
        request, 
        message=msg, 
        t_name='mycoach/messages.html',
        inbox_nav=inbox_nav(request.user, msg),
        main_nav=main_nav(request.user, 'student_view')
        )

class ECoach_Message_View(TailoredDocView):

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        self.template_name = kwargs['t_name']
        self.message_document = 'Messages/' + kwargs['message'] + '.messages'
        self.inbox_nav = kwargs['inbox_nav']
        self.main_nav = kwargs['main_nav']
        #configure_source_data(request.user.username)
        return super(ECoach_Message_View, self).dispatch(*args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Message_View, self).get_context_data(**kwargs)
        context["main_nav"] = self.main_nav
        context["inbox_nav"] = self.inbox_nav
        return context

def survey_preview_view(request, **kwargs):
    mview = ECoach_Survey_Preview_View.as_view()
    # hack the default message for now
    if kwargs['survey_id'] != '':
        survey = kwargs['survey_id']
    else:
        survey = 'testsurvey'
    return mview(
        request, 
        survey=survey, 
        t_name='mycoach/messages.html',
        inbox_nav=inbox_nav(request.user, survey),
        main_nav=main_nav(request.user, 'student_view')
        )

class ECoach_Survey_Preview_View(TailoredDocView):

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        self.template_name = kwargs['t_name']
        self.message_document = 'Surveys/' + kwargs['survey'] + '.survey'
        self.inbox_nav = kwargs['inbox_nav']
        self.main_nav = kwargs['main_nav']
        #configure_source_data(request.user.username)
        return super(ECoach_Survey_Preview_View, self).dispatch(*args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Survey_Preview_View, self).get_context_data(**kwargs)
        context["main_nav"] = self.main_nav
        context["inbox_nav"] = self.inbox_nav
        return context

"""
class ECoach_Survey_Preview_View(TailoredDocView):

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        self.template_name = kwargs['t_name']
        self.message_document = 'Surveys/' + kwargs['message'] + '.messages'
        self.main_nav = kwargs['main_nav']
        #configure_source_data(request.user.username)
        return super(ECoach_Message_View, self).dispatch(*args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Survey_Preview_View, self).get_context_data(**kwargs)
        context["main_nav"] = self.main_nav
        return context

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

class ECoach_Survey_View(ECoach_Multi_Survey_Mixin):
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
"""

