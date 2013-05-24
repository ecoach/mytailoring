from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.mail import EmailMultiAlternatives #send_mail, EmailMessage, 
from djangotailoring.views import TailoredDocView
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from mycoach.nav import Nav, Messages, StaffNav, DataLoaderNav
from mysettings import settings_mts4
from django.contrib.auth.models import User
from djangotailoring.project import getsubjectloader
from djangotailoring.subjects import DjangoSubjectLoader
from django.views.generic import TemplateView
from mycoach.models import UserProfile
#from mylogger.models import Log_Request
from mydata4.models import Source1
from mycoach.viewmixins import SurveyTestcaseDataPrefillerMixin, configure_source_data
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from djangotailoring.views import UserProfileSubjectMixin, LoginRequiredMixin
from djangotailoring.surveys.views import SinglePageSurveyView, SimpleSurveyView

def mylogout(request):
    return HttpResponseRedirect("https://weblogin.umich.edu/cgi-bin/logout")

def Generic_View(request, **kwargs):
    """
    # ALL SURVEYS WILL BE OPTIOANAL
    # -----------------------
    # look up user's surveys
    rwho = request.user.username
    rwhat = ECoach_SurveySep4_View.survey_id
    survey = None
    try:
        survey = Survey_Log.objects.filter(who=request.user, survey=rwhat)
    except: 
        pass
    # redirect to survey if needed 
    if len(survey) < 1: 
        Log_Request(request)
        return redirect(settings.DOMAIN_MTS + rwhat + '/')
    # -----------------------
    """

    #Log_Request(request)
    # load the nav object
    nav = Nav(request.path)
    return ECoach_Message_View.as_view()(request, nav=nav)  

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

#class BaselineSurveyView(LoginRequiredMixin, UserProfileSubjectMixin, AutoSaveSubjectDataMixin, LogPageViewMixin, SimpleSurveyView):
class ECoach_Multi_Survey_Mixin(SurveyTestcaseDataPrefillerMixin, LoginRequiredMixin, UserProfileSubjectMixin, SimpleSurveyView):
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

    return Message_Viewer_View.as_view()(request)

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
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey02_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey02.survey"
    source = 'Source1'
    survey_id = 'Survey02'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey03_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey03.survey"
    source = 'Source1'
    survey_id = 'Survey03'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey04_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey04.survey"
    source = 'Source1'
    survey_id = 'Survey04'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey05_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey05.survey"
    source = 'Source1'
    survey_id = 'Survey05'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey06_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey06.survey"
    source = 'Source1'
    survey_id = 'Survey06'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey07_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey07.survey"
    source = 'Source1'
    survey_id = 'Survey07'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey08_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey08.survey"
    source = 'Source1'
    survey_id = 'Survey08'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)

class Survey09_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey09.survey"
    source = 'Source1'
    survey_id = 'Survey09'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS + 'survey_thankyou/')

def survey_thankyou(request):
    return render(request, 'mycoach/thankyou.html', {})

class Survey10_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey10.survey"
    source = 'Source1'
    survey_id = 'Survey10'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings_mts4.DOMAIN_MTS)


