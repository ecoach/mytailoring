from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.conf import settings
from djangotailoring.views import TailoredDocView
from djangotailoring.project import getsubjectloader
from mynav.nav import main_nav

"""
from djangotailoring.subjects import DjangoSubjectLoader
from djangotailoring.views import UserProfileSubjectMixin, LoginRequiredMixin
from djangotailoring.surveys.views import SinglePageSurveyView, SimpleSurveyView
"""

def message_view(request, **kwargs):
    return render(request, 'messages.html', {
        "main_nav": main_nav(request.user, 'courses')
    })
    return HttpResponse("You're looking at the test message page")


class ECoach_Message_View(TailoredDocView):
    #m_messages = Messages()

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        #Log_Request(request)
        #configure_source_data(request.user.username)
        # load the nav object
        #self.m_nav = Nav(request.path)
        return super(ECoach_Message_View, self).dispatch(*args, **kwargs)

    @property 
    def message_document(self): 
        #msgid = self.m_nav.get_msgdoc()
        return "Messages/testing.messages"
        msg = self.m_messages.pathto(msgid)
        # return "Surveys/testsurvey.survey"

    @property 
    def template_name(self):
        template = 'mycoach/messages.html'
        return template
 
    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Message_View, self).get_context_data(**kwargs)
        #context["nav"] = self.m_nav
        return context
 
