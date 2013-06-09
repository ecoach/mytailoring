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
    mview = ECoach_Message_View.as_view()
    return mview(
        request, 
        message='testing',
        #message='widgets', 
        t_name='mycoach/messages.html',
        main_nav=main_nav(request.user, 'student_view')
        )

    #return render(request, 'messages.html', {
    #    "main_nav": main_nav(request.user, 'student_view')
    #})
    #return HttpResponse("You're looking at the test message page")

class ECoach_Message_View(TailoredDocView):

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        self.template_name = kwargs['t_name']
        self.message_document = 'Messages/' + kwargs['message'] + '.messages'
        self.main_nav = kwargs['main_nav']
        #configure_source_data(request.user.username)
        return super(ECoach_Message_View, self).dispatch(*args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Message_View, self).get_context_data(**kwargs)
        context["main_nav"] = self.main_nav
        return context
 
