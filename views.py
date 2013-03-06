from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.mail import EmailMultiAlternatives #send_mail, EmailMessage, 
#from django.contrib.auth import login, authenticate, logout
from djangotailoring.views import TailoredDocView
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
#from django.core.context_processors import csrf
from mycoach5.nav import Nav, Messages, StaffNav, DataLoaderNav
from mycoach5 import settings
from django.contrib.auth.models import User
from djangotailoring.project import getsubjectloader
from djangotailoring.subjects import DjangoSubjectLoader
from django.views.generic import TemplateView
from mycoach5.models import ELog, Survey_Log, UserProfile, Digestion, Digestion_Column
from mydata5.models import Source1
from mycoach5.viewmixins import SurveyTestcaseDataPrefillerMixin, configure_source_data
from mycoach5.forms import ( 
    Data_Loader_File_Upload_Form, 
    Data_Loader_File_Review_Form,
    Data_Loader_Data_Digest_Form,
    Data_Loader_MTS_Load_Form,
    Data_Loader_Archive_Form
    )
from mypump.csvfile import CsvFile, MapFile
from django.views.generic.edit import FormView

from django.shortcuts import redirect
#from djangotailoring.surveys.views import SimpleSurveyView
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

    Log_Request(request)
    # load the nav object
    nav = Nav(request.path)
    return ECoach_Message_View.as_view()(request, nav=nav)  

class ECoach_Message_View(TailoredDocView):
    m_messages = Messages()

    def dispatch(self, *args, **kwargs):
        # psudo constructor
        request = args[0]
        Log_Request(request)
        configure_source_data(request.user.username)
        # load the nav object
        self.m_nav = Nav(request.path)
        return super(ECoach_Message_View, self).dispatch(*args, **kwargs)

    @property 
    def message_document(self): 
        msgid = self.m_nav.get_msgdoc()
        msg = self.m_messages.pathto(msgid)
        return msg

    @property 
    def template_name(self):
        has_side = self.m_nav.decide_template()
        if has_side: 
            template = 'mycoach/side.html'
        else:
            template = 'mycoach/messages.html'
        return template
 
    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(ECoach_Message_View, self).get_context_data(**kwargs)
        context["nav"] = self.m_nav
        return context
 
def Download_Mysql_View(request):
    import os, time

    # if not admin don't do it
    staffmember = request.user.is_staff
    if not staffmember:
        return redirect('/')

    # send the results
    try:
        now = time.strftime('%Y-%m-%d-%H-%M-%S')         
        file_name = "mydb_" + now + ".sql"
        file_path = settings.DIR_COACH + "uploads/backups/" + file_name
        
        os.system("mysqldump -u ecoach -pecoach " + settings.DB_NAME + " > " + file_path)

        fsock = open(file_path,"rb")
        response = HttpResponse(fsock, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + file_name            
    except IOError:
        response = HttpResponseNotFound("error creating backup database file")

    return response

def Download_Analysis_View(request):
    return redirect('/') # until it's fixed
    import os.path
    from mycoach5.scripts.loader import Loader

    # if not admin don't do it
    staffmember = request.user.is_staff
    if not staffmember:
        return redirect('/')

    # run the mysql to sqlite dump
    ld = Loader()                                                                                                    
    ld.dumplite()
    
    # send the results
    try:
        file_name = "analysis.db"
        file_path = "/srv/www/" + file_name
        fsock = open(file_path,"rb")
        response = HttpResponse(fsock, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + file_name            
    except IOError:
        response = HttpResponseNotFound()

    return response

class ECoach_Single_Survey_Mixin(LoginRequiredMixin, UserProfileSubjectMixin, SinglePageSurveyView):
    m_messages = Messages()
    survey_document = "Messages/Survey01.survey"
    source = 'Source1'
    survey_id = 'none'

    def dispatch(self, request, *args, **kwargs):
        request = args[0]
        Log_Request(request)
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
            template = 'mycoach/messages.html'
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
        Log_Request(request)
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
        Log_Request(request)
        return redirect('/')

    return Message_Viewer_View.as_view()(request)

class Message_Viewer_View(TailoredDocView):
    #template_name='mycoach/admin.html'
    template_name='mycoach/message_viewer.html'
    m_subloader = getsubjectloader()
    m_messages = Messages()
    @property 
    def message_document(self): 
        return self.m_messages.pathto(self.request.GET.get("messages"))

    def dispatch(self, request, *args, **kwargs):
        # psudo constructor
        configure_source_data(request.user.username)
        Log_Request(request)
        # load the nav object
        self.m_nav = StaffNav(request.path)

        return super(Message_Viewer_View, self).dispatch(request, *args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        from django.db.models import Count, Avg # import the aggregators of interest
        context = super(Message_Viewer_View, self).get_context_data(**kwargs)
        context["args"] = self.request.GET

        min_clicks = 10
        active = User.objects.annotate(clicks=Count('elog')).filter(clicks__gt=min_clicks).order_by('username')
        ids = [] 
        for aa in active:
            ids.append(aa.username) 

        message_list = self.m_messages.getlist()

        message_choice = self.request.GET.get("messages")
        if message_choice == None:
            message_choice = message_list[0]

        student_choice = self.request.GET.get("students")
        if student_choice == None:
            student_choice = ids[0]

        context["student_choices"] = ids
        context["message_choices"] = message_list
        context["student_choice"] = student_choice
        context["message_choice"] = message_choice 
        context["user"] = self.request.user
        context["nav"] = self.m_nav       
 
        return context

    def get_subject(self):
        # over ride to get someone else's subject
        try:
            sub = self.m_subloader.get_subject(self.request.GET.get("students"))[0]
        except:
            sub = self.m_subloader.empty_subject()[0]
        return sub

def data_loader_file_upload(request):
    Log_Request(request)

    configure_source_data(request.user.username)

    profile = request.user.get_profile()
    prefs = profile.prefs

    try:
        digestion = Digestion.objects.get(pk=prefs["digestion_pk"])
    except:  
        digestion = Digestion(user=request.user)
        digestion.save()
        prefs['digestion_pk'] = digestion.id
        profile.prefs = prefs
        profile.save()
 
    try:
        active_csv_data = digestion.data_file.disk_name()
    except:
        active_csv_data = "*no data files uploaded*"
    try:
        active_csv_map = digestion.map_file.disk_name()
    except:
        active_csv_map = "*no map files uploaded*"

   
    if request.method == 'POST':
        form = Data_Loader_File_Upload_Form(
            request=request,
            data=request.POST, 
            files=request.FILES
        )
        if form.is_valid():
            # Do valid form stuff here
            form.save_data(digestion)
            return redirect('data_loader_file_upload')
    else:
        try:
            df = digestion.data_file.id
        except: 
            df = 0   
        try:
            mf = digestion.map_file.id
        except:
            mf = 0
        form = Data_Loader_File_Upload_Form(
            request=request,
            initial={'select_datafile' : df, 'select_idmap': mf}
        )

    return render(request, 'mycoach/data_loader_file_upload.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_loader": DataLoaderNav(request.path),
        "active_csv_map": active_csv_map,
        "active_csv_data": active_csv_data
    })

def mp_map_download(request):
    import os

    # if not admin don't do it
    staffmember = request.user.is_staff
    if not staffmember:
        return redirect('/')

    # send the results
    try:
        file_name = "mp_name_map.csv"
        file_path = os.path.dirname(__file__) + '/uploads/other/' + file_name
        
        f = open(file_path, 'w')
        # select MP_Name, user_id from mydata5_Source1 where not MP_Name=user_id group by MP_Name;  
        new = Source1.objects.exclude(user_id__in=User.objects.filter(is_staff=True).values_list('username', flat=True)).values_list('MP_Name', 'user_id')
        # old = Source1.objects.mp_names()
        ss = ""
        # for nn in mp_names:
        for nn in new:
            ss += str(nn[0]) + "," + str(nn[1]) + "\n"
        ss = ss[0:len(ss)-1]
        f.write(ss)
        f.close()

        fsock = open(file_path,"rb")
        response = HttpResponse(fsock, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=' + file_name            
    except IOError:
        response = HttpResponseNotFound("error creating the file")

    return response

     

def data_loader_file_review(request):
    Log_Request(request)

    configure_source_data(request.user.username)

    profile = request.user.get_profile()
    prefs = profile.prefs

    try:
        digestion = Digestion.objects.get(pk=prefs["digestion_pk"])
    except:  
        digestion = Digestion(user=request.user)
        digestion.save()
        prefs['digestion_pk'] = digestion.id
        profile.prefs = prefs
        profile.save()

    try:
        # anyone who has logged into the system is reserved from mapping
        reserved = User.objects.values_list('username')
        reserved = [x[0] for x in reserved]
        mapp  = MapFile(digestion.map_file.path, digestion.map_file.disk_name(), reserved) # assume id in row 1
    except:
        pass # for now...

    # rows map
    try:
        map_file_row_cnt  = mapp.get_row_cnt() 
    except:
        map_file_row_cnt = "*error: unable to count rows*"
    # cols map
    try:
        map_file_col_cnt = mapp.get_col_cnt()
    except:
        map_file_col_cnt =  "*error: unable to count cols*"
    # id sample map
    try:
        map_file_sample = mapp.get_id_sample()
    except:
        map_file_sample =  ["*error: unable to find id sample*"]
    # duplicates in map 
    try:
        map_file_dups = mapp.validate_duplicates()
    except:
        map_file_dups = []
    # reserved in map 
    try:
        map_file_reserved = mapp.validate_reserved()
    except:
        map_file_reserved = []
    # sample ids in map
    try:
        map_file_id_sample = mapp.get_id_sample()
    except:
        map_file_id_sample = [] 
  
    # data  
    try: 
        data  = CsvFile(digestion.data_file.path, digestion.data_file.disk_name(), digestion.get_id_column())
    except:
        return redirect('data_loader_file_upload')

    # make id replacements in data
    try:
        remapped_ids = data.idremap(mapp)
    except:
        remapped_ids = []
 

    # rows data
    try:
        data_file_row_cnt = data.get_row_cnt() 
    except:
        data_file_row_cnt = "*error: unable to count rows*"
    # cols data
    try:
        data_file_col_cnt = data.get_col_cnt()
    except:
        data_file_col_cnt =  "*error: unable to count cols*"
    # id sample data
    try:
        data_file_id_sample = data.get_id_sample()
    except:
        data_file_id_sample =  "*error: unable to find id sample*"
    # id verify
    try:
        data_file_duplicate_ids = data.duplicate_ids()
    except:
        data_file_duplicate_ids = []
   
    if request.method == 'POST':
        form = Data_Loader_File_Review_Form(
            data=request.POST, 
            choices = data.heads_tuple()
        )
        if form.is_valid():
            # Do valid form stuff here
            form.save_data(digestion)
            return redirect('data_loader_file_review')
    else:
        form = Data_Loader_File_Review_Form(
            initial = {'select_id_column' : digestion.get_id_column()},
            choices = data.heads_tuple()
        )
    
    return render(request, 'mycoach/data_loader_file_review.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_loader": DataLoaderNav(request.path),
        "active_row_cnt": data_file_row_cnt,
        "active_col_cnt": data_file_col_cnt,
        "active_id_column": data.get_id_header() + " ( column " + str(digestion.get_id_column()) + " )",
        "active_id_sample": data_file_id_sample,
        "remapped_ids": remapped_ids,
        "duplicate_ids": data_file_duplicate_ids,
        "map_file_row_cnt": map_file_row_cnt,
        "map_file_col_cnt": map_file_col_cnt,
        "map_file_dups": map_file_dups,
        "map_file_reserved": map_file_reserved,
        "map_file_id_sample": map_file_id_sample,
    })

def data_loader_data_digest(request):
    Log_Request(request)

    configure_source_data(request.user.username)

    profile = request.user.get_profile()
    prefs = profile.prefs

    try:
        digestion = Digestion.objects.get(pk=prefs["digestion_pk"])
    except:  
        digestion = Digestion(user=request.user)
        digestion.save()
        prefs['digestion_pk'] = digestion.id
        profile.prefs = prefs
        profile.save()

    try:
        # anyone who has logged into the system is reserved from mapping
        reserved = User.objects.values_list('username')
        reserved = [x[0] for x in reserved]
        mapp  = MapFile(digestion.map_file.path, digestion.map_file.disk_name(), reserved) # assume id in row 1
    except:
        pass # for now...

    # rows map
    try:
        map_file_row_cnt  = mapp.get_row_cnt() 
    except:
        map_file_row_cnt = "*error: unable to count rows*"
    # cols map
    try:
        map_file_col_cnt = mapp.get_col_cnt()
    except:
        map_file_col_cnt =  "*error: unable to count cols*"
    # id sample map
    try:
        map_file_sample = mapp.get_id_sample()
    except:
        map_file_sample =  ["*error: unable to find id sample*"]
    # duplicates in map 
    try:
        map_file_dups = mapp.validate_duplicates()
    except:
        map_file_dups = []
    # reserved in map 
    try:
        map_file_reserved = mapp.validate_reserved()
    except:
        map_file_reserved = []
    # sample ids in map
    try:
        map_file_id_sample = mapp.get_id_sample()
    except:
        map_file_id_sample = [] 

    # data  
    try:
        data  = CsvFile(digestion.data_file.path, digestion.data_file.disk_name(), digestion.get_id_column())
    except:
        return redirect('data_loader_file_upload')

    # make id replacements in data
    try:
        remapped_ids = data.idremap(mapp)
    except:
        remapped_ids = []
 
    # mts charactoristic
    if digestion.mts_characteristic and len(digestion.mts_characteristic) > 0:
        mts_char = digestion.mts_characteristic
        mts_char_report = mts_char
    else:
        mts_char = []
        mts_char_report = "*no mts char selected*"
    # digestion function
    if digestion.function > 0:
        digestion_function = data.get_function_name(digestion.function)
        digestion_function_select = data.get_function_id(digestion.function)
    else:
        digestion_function = "*digestion funtion not selected*" 
        digestion_function_select = 0
    # digestion columns
    try:
        digestion_columns = Digestion_Column.objects.all().filter(digestion=digestion.id).values_list('column_number')
        digestion_columns = [x[0] for x in digestion_columns]
        digestion_columns_select = digestion_columns
    except:
        #digestion_columns = "*digestion columns not selectd*" 
        digestion_columns = []
        digestion_columns_select = []

    chars = Source1._meta.get_all_field_names()
    chars.remove('id')
    chars.remove('user_id')
    chars.remove('updated')
    chars.remove('uid')
    chars = sorted(chars)
    chars = tuple((cc, cc) for cc in chars)

    if request.method == 'POST':
        form = Data_Loader_Data_Digest_Form(
            data=request.POST, 
            function_choices = data.functions_tuple(),
            column_choices = data.columns_tuple(),
            mts_char_choices = chars
        )
        if form.is_valid():
            # Do valid form stuff here
            form.save_data(digestion)
            return redirect('data_loader_data_digest')
    else:
        form = Data_Loader_Data_Digest_Form(
            initial = {'digestion_function' : digestion_function_select, 'digestion_columns' : digestion_columns_select, 'mts_char' : mts_char},
            function_choices = data.functions_tuple(),
            column_choices = data.columns_tuple(),
            mts_char_choices = chars
        )
    try:
        data.execute(digestion.function, digestion_columns_select) 
    except:
        pass
    return render(request, 'mycoach/data_loader_data_digest.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_loader": DataLoaderNav(request.path),
        "digestion_function": digestion_function,
        "digestion_columns": digestion_columns,
        "mts_char": mts_char_report,
        "digestion_result" : data.get_mts(), 
    })

def data_loader_mts_load(request):
    Log_Request(request)

    configure_source_data(request.user.username)

    profile = request.user.get_profile()
    prefs = profile.prefs

    try:
        digestion = Digestion.objects.get(pk=prefs["digestion_pk"])
    except:  
        digestion = Digestion(user=request.user)
        digestion.save()
        prefs['digestion_pk'] = digestion.id
        profile.prefs = prefs
        profile.save()

    try:
        # anyone who has logged into the system is reserved from mapping
        reserved = User.objects.values_list('username')
        reserved = [x[0] for x in reserved]
        mapp  = MapFile(digestion.map_file.path, digestion.map_file.disk_name(), reserved) # assume id in row 1
    except:
        pass # for now...

    # rows map
    try:
        map_file_row_cnt  = mapp.get_row_cnt() 
    except:
        map_file_row_cnt = "*error: unable to count rows*"
    # cols map
    try:
        map_file_col_cnt = mapp.get_col_cnt()
    except:
        map_file_col_cnt =  "*error: unable to count cols*"
    # id sample map
    try:
        map_file_sample = mapp.get_id_sample()
    except:
        map_file_sample =  ["*error: unable to find id sample*"]
    # duplicates in map 
    try:
        map_file_dups = mapp.validate_duplicates()
    except:
        map_file_dups = []
    # reserved in map 
    try:
        map_file_reserved = mapp.validate_reserved()
    except:
        map_file_reserved = []
    # sample ids in map
    try:
        map_file_id_sample = mapp.get_id_sample()
    except:
        map_file_id_sample = [] 

    # data
    try:
        data  = CsvFile(digestion.data_file.path, digestion.data_file.disk_name(), digestion.get_id_column())
    except:
        return redirect('data_loader_file_upload')
        
    # make id replacements in data
    try:
        remapped_ids = data.idremap(mapp)
    except:
        remapped_ids = []
 
    # digestion name
    if digestion.name and len(digestion.name) > 0:
        digestion_name = digestion.name
        digestion_name_reprint = digestion_name
    else:
        digestion_name = "*digestion not named*" 
        digestion_name_reprint = ''

    if request.method == 'POST': 
        form = Data_Loader_MTS_Load_Form(
            data=request.POST, 
        )
        if form.is_valid():
            # Do valid form stuff here
            if form.save_data(digestion, request.user, data):
                return redirect('data_loader_archive')
            else:
                return redirect('data_loader_mts_load')
    else:
        form = Data_Loader_MTS_Load_Form(
            initial = {'digestion_name' : digestion_name_reprint},
        )

    return render(request, 'mycoach/data_loader_mts_load.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_loader": DataLoaderNav(request.path),
        "digestion_id" : digestion.id, 
        "digestion_name": digestion_name,
        "digestion": digestion,
    })

def data_loader_archive(request):
    Log_Request(request)

    configure_source_data(request.user.username)

    profile = request.user.get_profile()
    prefs = profile.prefs

    profile = request.user.get_profile()
    prefs = profile.prefs

    try:
        digestion = Digestion.objects.get(pk=prefs["digestion_pk"])
    except:  
        digestion = Digestion(user=request.user)
        digestion.save()
        prefs['digestion_pk'] = digestion.id
        profile.prefs = prefs
        profile.save()

    if request.method == 'POST': 
        form = Data_Loader_Archive_Form(
            data=request.POST, 
        )
        if form.is_valid():
            # Copy the old digestion
            new = form.cleaned_data['digestion'] # still old
            cols = Digestion_Column.objects.filter(digestion=new.id) # old cols
            new.id = digestion.id # becomes new
            new.user = digestion.user # becomes new
            new.save() # save new
            Digestion_Column.objects.filter(digestion=new.id).delete() # delete existing cols
            for cc in cols:     # copy old cols
                cc.id = None    # become new
                cc.digestion_id = new.id
                cc.save() 
            return redirect('data_loader_archive')
    else:
        form = Data_Loader_Archive_Form()

    return render(request, 'mycoach/data_loader_archive.html', {
        "form": form,
        "args": request.GET,
        "nav_staff": StaffNav(request.path),
        "nav_loader": DataLoaderNav(request.path),
        "digestion_name": digestion.get_name(),
        "digestion": digestion,
    })

def data_loader_help(request):

    return render(request, 'mycoach/data_loader_help.html', {
        "nav_staff": StaffNav(request.path),
        "nav_loader": DataLoaderNav(request.path),
    })

class Copy_Student_View(TemplateView):
    #template_name='mycoach/admin.html'
    template_name='mycoach/copy_student.html'
 
    def dispatch(self, request, *args, **kwargs):
        from django.db.models import Count, Avg # import the aggregators of interest
        # psudo constructor
        #self.m_nav = kwargs["nav"]
        Log_Request(request)
        configure_source_data(request.user.username)
        # load the nav object
        self.m_nav = StaffNav(request.path)

        self.m_copy = request.GET.get("copy_student")

        # attempt to copy the student data
        try:        
            me = Source1.objects.filter(user_id=request.user.username)[0]
            you = Source1.objects.filter(user_id=self.m_copy)[0]
            you.pk = me.pk
            you.uid = me.uid # this is effectively to ensure the user_id attribute of the table is correct
            you.save()
        except:
            pass

        min_clicks=1
        #self.m_students = User.objects.annotate(clicks=Count('elog', distinct=True)).filter(clicks__gt=min_clicks).order_by('username').values(
        #self.m_students = User.objects.annotate(clicks=Count('elog', distinct=True)).order_by('username').values(
        self.m_students = User.objects.values(
            'username', 
            'source1__user_id', 
            'source1__First_Survey_Complete', 
            'source1__MP_Name',
            'source1__First_Name',
            'source1__Last_Name',
            'source1__Gender',
            'source1__Course',
            'source1__Cum_GPA_Survey',
            'source1__Semesters_Completed',
            'source1__College',
            'source1__Grade_Want',
            'source1__Confidence').filter(source1__First_Survey_Complete='Yes').annotate(clicks=Count('elog', distinct=True)).order_by('username')

        return super(Copy_Student_View, self).dispatch(request, *args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(Copy_Student_View, self).get_context_data(**kwargs)
        context["args"] = self.request.GET
        context["user"] = self.request.user
        context["nav"] = self.m_nav
        context["students"] = self.m_students
        context["copy_student"] = self.m_copy
        return context

class Usage_Stats_View(TemplateView):
    template_name='mycoach/usage_stats.html'
 
    def dispatch(self, request, *args, **kwargs):
        from django.db.models import Count, Avg, Q # import the aggregators of interest
        # psudo constructor
        Log_Request(request)
        configure_source_data(request.user.username)
        # load the nav object
        self.m_nav = StaffNav(request.path)
      
        """
        # which day of the week are people clicking
        select 
            ff.course as course,
            DAYNAME(ll.mwhen) as dow,
            count(*) as cnt
        from mycoach5_elog as ll
        inner join mydata5_Source1data as ff on ff.user_id=ll.who
        group by ff.course, dow
    order by course, cnt;
        """
 
        Source1_students = Source1.objects.exclude(user_id='jtritz').exclude(user_id='mhuberth').exclude(user_id='tamckay').exclude(user_id='amymoors').exclude(user_id='no_data').exclude(user_id='jaredtritz@gmail.com').exclude(user_id='katemiller1027@gmail.com').exclude(user_id='murdockw')
        User_students = User.objects.exclude(username='jtritz').exclude(username='mhuberth').exclude(username='tamckay').exclude(username='amymoors').exclude(username='no_data').exclude(username='jaredtritz@gmail.com').exclude(username='katemiller1027@gmail.com').exclude(username='murdockw')
        ELog_students = ELog.objects.values('what').exclude(who='jtritz').exclude(who='mhuberth').exclude(who='tamckay').exclude(who='amymoors').exclude(who='jaredtritz@gmail.com').exclude(who='katemiller1027@gmail.com').exclude(who='murdockw')

        self.m_surveys_completed = len(Source1_students.filter(First_Survey_Complete="Yes"))
        self.m_surveys_incomplete = len(User_students.filter(elog__what__contains="Survey").annotate(ecnt=Count('elog__what', distinct=True)).annotate(scnt=Count('survey_log__id', distinct=True)).filter(scnt__lt=1))
        self.m_surveys_not_started = len(User_students.exclude(elog__what__contains="Survey").distinct('username'))

        #self.m_memorize_personal = len(Source1_students.filter(Q(Memorize_personal="Strongly_Agree") | Q(Memorize_personal="Agree")))
        self.m_memorize_personal = len(Source1_students.filter((Q(Memorize_personal="Strongly_Agree") | Q(Memorize_personal="Agree")) & Q(First_Survey_Complete="Yes")))
        self.m_math_confidence = len(Source1_students.filter((Q(Math_Confidence="Strongly_Agree") | Q(Math_Confidence="Agree")) & Q(First_Survey_Complete="Yes")))
        self.m_trust_calc = len(Source1_students.filter((Q(Trust_Calculation="Strongly_Agree") | Q(Trust_Calculation="Agree")) & Q(First_Survey_Complete="Yes")))
        self.m_hard_work_solve = len(Source1_students.filter((Q(Hard_work_personal_cant_solve="Strongly_Disagree") | Q(Hard_work_personal_cant_solve="Disagree")) & Q(First_Survey_Complete="Yes")))
        self.m_innate = len(Source1_students.filter((Q(Innate="Strongly_Disagree") | Q(Innate="Disagree")) & Q(First_Survey_Complete="Yes")))
        self.m_memorize_general = len(Source1_students.filter((Q(Memorize_general="Strongly_Agree") | Q(Memorize_general="Agree")) & Q(First_Survey_Complete="Yes")))
        self.m_recall_formula = len(Source1_students.filter((Q(Recall_Formula="Strongly_Agree") | Q(Recall_Formula="Agree")) & Q(First_Survey_Complete="Yes")))
        self.m_apply_principles = len(Source1_students.filter((Q(Apply_Principles="Strongly_Disgree") | Q(Apply_Principles="Disagree")) & Q(First_Survey_Complete="Yes")))
        self.m_hard_work_understand = len(Source1_students.filter((Q(Hard_work_personal_understand="Strongly_Disgree") | Q(Hard_work_personal_understand="Disagree")) & Q(First_Survey_Complete="Yes")))

        self.m_slc_interest = len(Source1_students.filter(Q(SLC_Interest="Signed_Up") | Q(SLC_Interest="Yes_Not_Signed_Up")))

        self.m_clicks_student = ELog_students.values('who').exclude(what__contains="Survey").annotate(wcnt=Count('who')).order_by('-wcnt')

        self.m_clicks_page = ELog_students.values('what').exclude(what__contains="Survey").annotate(wcnt=Count('what')).order_by('-wcnt')  

        return super(Usage_Stats_View, self).dispatch(request, *args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(Usage_Stats_View, self).get_context_data(**kwargs)
        context["nav"] = self.m_nav

        #context["surveys"] = dict({'completed140': 20})
        context["surveys"] = Source1.objects.survey_breakdown()

        #context["surveys_completed"] = self.m_surveys_completed
        context["surveys_completed"] = Source1.objects.with_surveys()
        context["surveys_incomplete"] = self.m_surveys_incomplete
        context["surveys_not_started"] = self.m_surveys_not_started

        context["memorize_personal"] = self.m_memorize_personal
        context["math_confidence"] = self.m_math_confidence
        context["trust_calc"] = self.m_trust_calc
        context["hard_work_solve"] = self.m_hard_work_solve
        context["innate"] = self.m_innate
        context["memorize_general"] = self.m_memorize_general
        context["recall_formula"] = self.m_recall_formula
        context["apply_principles"] = self.m_apply_principles
        context["hard_work_understand"] = self.m_hard_work_understand

        context["slc_interest"] = self.m_slc_interest

        context["clicks_student"] = self.m_clicks_student

        context["clicks_page"] = self.m_clicks_page
        return context

def Use_View(request):
    import datetime
    # do a little logging...
    rwhat = request.GET['what'] 
    rwho = request.user.username
    rwhen = datetime.datetime.now()

    log = ELog(who=request.user, mwhen=rwhen, what=rwhat)
    log.save()

    return HttpResponse("We want to record which accordions are opened so that we have some indication of what part of these messages are reaching the user.")
 
def Log_Survey(request, survey_id):
    import datetime
    # do a little logging...
    # rwhat = request.GET['what'] 
    rwhat = survey_id 
    rwho = request.user.username
    rwhen = datetime.datetime.now()

    log = Survey_Log(who=request.user, mwhen=rwhen, survey=rwhat)
    log.save()

def Log_Request(request):
    import datetime
    # do a little logging...
    rwhat = request.path
    rwho = request.user.username
    rwhen = datetime.datetime.now()

    log = ELog(who=request.user, mwhen=rwhen, what=rwhat)
    log.save()       

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

class Survey02_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey02.survey"
    source = 'Source1'
    survey_id = 'Survey02'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey03_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey03.survey"
    source = 'Source1'
    survey_id = 'Survey03'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey04_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey04.survey"
    source = 'Source1'
    survey_id = 'Survey04'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey05_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey05.survey"
    source = 'Source1'
    survey_id = 'Survey05'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey06_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey06.survey"
    source = 'Source1'
    survey_id = 'Survey06'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey07_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey07.survey"
    source = 'Source1'
    survey_id = 'Survey07'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey08_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey08.survey"
    source = 'Source1'
    survey_id = 'Survey08'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey09_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey09.survey"
    source = 'Source1'
    survey_id = 'Survey09'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

class Survey10_View(ECoach_Multi_Survey_Mixin):
    survey_document = "Messages/Survey10.survey"
    source = 'Source1'
    survey_id = 'Survey10'
    # HACK-ALERT - set the property which makes survey re-take-able
    
    def handle_end_of_survey(self):
        Log_Survey(self.request, self.survey_id)
        return redirect(settings.DOMAIN_MTS)

def mycheckout(request):
    import pwd, os, pexpect
    # os.system("source /Users/jtritz/scripts/mycheckout.sh") 
    # return 
    # uid = pwd.getpwnam('jtritz')[2]
    # os.setuid(uid)
    os.system("source /home/jtritz/scripts/mycheckout.sh") 

    child = pexpect.spawn('sudo apachectl -k graceful')
    # child.expect('[sudo] password for .*:')
    # child.sendline(password)
    child.interact()

def mycheckback(request):
    return HttpResponse('reboot done')

class Email_Students_View(TailoredDocView):
    template_name='mycoach/email_students.html'

    def dispatch(self, request, *args, **kwargs):
        # psudo constructor
        configure_source_data(request.user.username)
        Log_Request(request)
        # load the nav object
        self.m_nav = StaffNav(request.path)
         
        if request.user.username == 'jtritz' and request.GET.get("trigger") == 'checked':
            self.construct_sendto()
            self.construct_bcc()
            self.construct_subject()
            self.construct_htmlcontent()
            self.construct_attachments()    
            #self.mysend_mail()

        return super(Email_Students_View, self).dispatch(request, *args, **kwargs)

    #over ride context creation for the template
    def get_context_data(self, **kwargs):
        context = super(Email_Students_View, self).get_context_data(**kwargs)
        context["args"] = self.request.GET
        #context["student_choices"] = ids
        context["user"] = self.request.user
        context["nav"] = self.m_nav       
 
        return context

    def mysend_mail(self):
        #sentfrom = 'tamckay@umich.edu'
        sentfrom = 'ecoach-help@umich.edu'
        sendto = self.m_sendto
        bcc = self.m_bcc
        subject = self.m_subject 
        bodytext = 'html message'
        html_content = self.m_htmlcontent 
        message = EmailMultiAlternatives(
            subject, 
            bodytext, 
            sentfrom,
            sendto, 
            bcc, 
            headers = {'Reply-To': 'ecoach-help@umich.edu'}
        )
        message.attach_alternative(html_content, "text/html")
        #message.attach_file(self.m_attached_filepath)
        message.send()

    def construct_sendto(self):
        self.m_sendto = ['jtritz@umich.edu', 'tamckay@umich.edu', 'mhuberth@umich.edu']
        #self.m_sendto = ['jtritz@umich.edu']

    def construct_bcc(self):
        #self.m_bcc = get_recipients_partial_survey()
        #self.m_bcc = []
        #self.m_bcc = get_recipients_message_release()
        self.m_bcc = get_recipients_signup_reminder()

    def construct_subject(self):
        #self.m_subject = 'Reminder 2: Sign up for ECoach!'
        #self.m_subject = "ECoach exam 1 prep messages"
        #self.m_subject = 'Reminder 3: Sign up for ECoach before your 1st exam!'
        #self.m_subject = "ECoach exam 1 response messages"
        self.m_subject = "Reminder 4: Sign up for ECoach before it's too late!"

    def construct_htmlcontent(self):
        #self.m_htmlcontent = get_html_content_partial_survey()
        #self.m_htmlcontent = get_html_content_reminder2()
        #self.m_htmlcontent = get_html_content_exam1_prep_release()
        #self.m_htmlcontent = get_html_content_reminder3()
        #self.m_htmlcontent = get_html_content_exam1_response_release()
        self.m_htmlcontent = get_html_content_reminder4()

    def construct_attachments(self):
        self.m_attached_filepath = '/home/jared/bitbucket/ecoach_webapps/mycoach5/grade_prediction.png'

def savethis():
    from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
    #send_mail('Subject hello', 'Here is the message.', 'ecoach-help@umich.edu', ['jtritz@umich.edu', 'jaredtritz@gmail.com'], fail_silently=False)
    sentfrom = 'tamckay@umich.edu'
    #sentfrom = 'jtritz@umich.edu'
    sendto = ['jtritz@umich.edu', 'tamckay@umich.edu', 'mhuberth@umich.edu']
    #sendto = ['jtritz@umich.edu']
    #bcc = ['jaredtritz@gmail.com', 'timamckay@gmail.com']
    #bcc = get_recipients_signup_reminder()
    bcc = get_recipients_partial_survey()
    subject = 'Reminder 2: Sign up for ECoach!'
    #bodytext = 'Example message...'
    bodytext = 'html message'
    #html_content = get_html_content_reminder2()
    html_content = get_html_content_partial_survey()
    #message = EmailMessage(
    message = EmailMultiAlternatives(
        subject, 
        bodytext, 
        sentfrom,
        sendto, 
        bcc, 
        headers = {'Reply-To': 'ecoach-help@umich.edu'}
    )
    message.attach_alternative(html_content, "text/html")

    #message.attach('design.png', img_data, 'image/png')
    #message.attach_file('/home/jared/bitbucket/ecoach_webapps/mycoach5/static/mycoach5/fall/images/ecoach_logo90x90.png')
    #message.attach_file('/Users/jtritz/grade_prediction.png')
    message.attach_file('/home/jared/bitbucket/ecoach_webapps/mycoach5/grade_prediction.png')
    if self.request.user.username == 'jtritz':
        pass #message.send()

    """
    message = EmailMultiAlternatives(
        subject, 
        text_content, 
        from_email, 
        [to])
    """



def get_recipients_signup_reminder():
    recips = Source1.objects.exclude(First_Survey_Complete="Yes").exclude(Opt_Out="Out").exclude(Course_Reg__isnull=True).values_list('user_id') 
    ret = []
    for rr in recips:
        ret.append(str(rr[0]) + '@umich.edu') 
        
    return ret

def get_recipients_partial_survey():
    """
    select * from mycoach5_elog as e1 inner join (select user_id from mydata5_Source1data where First_Survey_Complete is null and Opt_Out="In") as res1 on res1.user_id=e1.who order by who
    """
    recips = Source1.objects.exclude(First_Survey_Complete__isnull=True).exclude(Opt_Out="In").exclude(Course_Reg__isnull=True).values_list('user_id') 
    ret = []
    for rr in recips:
        ret.append(str(rr[0]) + '@umich.edu') 
        
    return ret
        
def get_recipients_message_release():
    recips = Source1.objects.filter(First_Survey_Complete="Yes").exclude(Course_Reg__isnull=True).values_list('user_id') 
    ret = []
    for rr in recips:
        ret.append(str(rr[0]) + '@umich.edu') 
        
    return ret

def get_html_content_exam1_prep_release():
    html_content = """
    <p>
    Hello,
    </p>

    <p>
    With your first midterm just around the corner E<sup>2</sup>Coach has released its second set of <b>tailored</b> messages.  These messages are aimed at reminding you how important the first exam is and helping direct your preperation.
    </p>
    
    <p>
    You can find your messages here: <a href='https://ecoach.lsa.umich.edu/w13physics/'>https://ecoach.lsa.umich.edu/w13physics/</a>
    </p>

    <p>
    Sincerely,
    </p>

    <p>
    Your E<sup>2</sup>Coaches: 
    </p>

    Tim McKay: Arthur F. Thurnau Professor of Physics, Director of the LSA Honors Program
    <br>
    Madeline Huberth: E<sup>2</sup>Coach Tailoring Specialist, 2011 UM Physics Grad and Gates Cambridge Scholar 
    <br>
    Jared Tritz: E<sup>2</sup>Coach Programmer, Founder of Cransort, designs fruit sorting machines
    """
    return html_content
 
def get_html_content_partial_survey():
    html_content = """
    <p>
    Hello,
    </p>

    <p>
    It appears you partially completed the sign up survey for ECoach...
    </p>
    """
    return html_content
    
def get_html_content_reminder2():
    html_content = """
<p>
Greetings! 
</p>

<p>
Introductory Physics is challenging, and we'd like to offer you the opportunity to take advantage of E<sup>2</sup>Coach: our new Expert Electronic Coach for students taking on tough classes at Michigan. 
</p>

<p>
We have built this system especially for physics to provide you with personalized feedback, encouragement, and advice from former students, all based on your background and how you're doing in the class. E<sup>2</sup>Coach was first launched in January 2012, and students who have used it have outperformed those who don't by a quarter letter grade (moving from a B+ to an A- for example). It really helps to get specific advice and use it to optimize your studying!
</p>

<p>
Among many other things, E<sup>2</sup>Coach will help you to know whether you're on track by giving you personal grade predictions after every exam, you will find an example from last term attached. This term you will be able to adjust your future scores and see where your grade lands.
</p>

<p>
This student really struggled on the first exam, recognized he was in trouble and adopted changes to his study habits recommended by E<sup>2</sup>Coach. He more than double his second exam score and ended up improving from a D to a B-! He was able to learn from former students who found their way to success in this class. Here's an example of their advice:
</p>

<p>
<center>
<i>
"Change your Study Habits. Find new study tactics and find out your exact week points.  One of my friends was too proud to ask for help, and when she did ask she would pretend like she understood the explanation the first time when really she needed more help. If you don't understand something, fix it!"
</i>
</center>
</p>

<p>
To take advantage of the free personalized support E<sup>2</sup>Coach provides, please go to: <a href='https://ecoach.lsa.umich.edu/w13physics/Opt_In/'>https://ecoach.lsa.umich.edu/w13physics/Opt_In/</a> and opt in.  Then complete the 10 minute survey telling us more about your background, why you're taking this class, and how you plan to go about it. That's all you need to do. Using this information and the course gradebook, E<sup>2</sup>Coach will immediately start giving you personalized advice. You'll get a big batch of advice this week before the first exam, in response to each of the three midterms, and again at the end of the course.  You may also opt out from this survey and we won't send you any more reminder email!
</p>

<p>
If you want to learn more first go to <a href='https://ecoach.lsa.umich.edu/'>https://ecoach.lsa.umich.edu/</a>, and you'll land on the course selection page. From there, you can learn more about what E<sup>2</sup>Coach has to offer. Each semester we've added new functionality and the advice engine is getting better.  The 'Press' tab on that page will show you some articles and podcasts about the system. If you have questions or comments about the system please send an email to ecoach-help@umich.edu.
</p>

<p>
Sincerely,
</p>

<p>
Your E<sup>2</sup>Coaches: 
</p>

Tim McKay: Arthur F. Thurnau Professor of Physics, Director of the LSA Honors Program
<br>
Madeline Huberth: E<sup>2</sup>Coach Tailoring Specialist, 2011 UM Physics Grad and Gates Cambridge Scholar 
<br>
Jared Tritz: E<sup>2</sup>Coach Programmer, Founder of Cransort, designs fruit sorting machines
        """
    return html_content

def get_html_content_reminder3():
    html_content = """
<p>
Hello again :)
</p>

<p>
This is your last reminder to sign up for E<sup>2</sup>Coach before the first exam! Sign up now and recieve <b>tailored</b> exam prep messages meant to focus and encourage you.
</p>

<p>
Later in the semester the tailored version of E<sup>2</sup>Coach will help you to know whether you're on track by giving you personal grade predictions after every exam. This term you will be able to adjust your future scores and see where your grade lands.
</p>

<p>
To take advantage of the free personalized support E<sup>2</sup>Coach provides, please go to: <a href='https://ecoach.lsa.umich.edu/w13physics/Opt_In/'>https://ecoach.lsa.umich.edu/w13physics/Opt_In/</a> and opt in.  Then complete the 10 minute survey telling us more about your background, why you're taking this class, and how you plan to go about it. That's all you need to do. Using this information along with data from the gradebook, E<sup>2</sup>Coach will provide you personalized support throughout the semester.  If you don't want to sign up for E<sup>2</sup>Coach or recieve any more reminders the first survey question allows you to opt out.  
</p>

<p>
If you want to learn more first go to <a href='https://ecoach.lsa.umich.edu/'>https://ecoach.lsa.umich.edu/</a>, and you'll land on the course selection page. From there, you can learn more about what E<sup>2</sup>Coach has to offer. Each semester we've added new functionality and the advice engine is getting better.  The 'Press' tab on that page will show you some articles and podcasts about the system. If you have questions or comments about the system please send an email to ecoach-help@umich.edu.
</p>

<p>
Sincerely,
</p>

<p>
Your E<sup>2</sup>Coaches: 
</p>

Tim McKay: Arthur F. Thurnau Professor of Physics, Director of the LSA Honors Program
<br>
Madeline Huberth: E<sup>2</sup>Coach Tailoring Specialist, 2011 UM Physics Grad and Gates Cambridge Scholar 
<br>
Jared Tritz: E<sup>2</sup>Coach Programmer, Founder of Cransort, designs fruit sorting machines
        """
    return html_content

def get_html_content_exam1_response_release():
    html_content = """
<p>
Hello and congratulations on completing the first exam :)
</p>

<p>
If you haven't noticed it yet your E<sup>2</sup>Coach account was updated last night in response to the first exam data.  Some of you will find messages there enouraging you to keep going with whatever you did and some of you who didn't do as well will find messages aimed at helping you realize what changes are likely to help.  In all cases there is normalized class performance data to review, so here are your messages: <a href='https://ecoach.lsa.umich.edu/w13physics/'>https://ecoach.lsa.umich.edu/w13physics/</a>.  Also, the grade prediction has boxes to edit your future scores and predict your grade :) 
</p>

<p>
Enjoy and let us know if there is anything we can do to help.
</p>

<p>
Sincerely,
</p>

<p>
Your E<sup>2</sup>Coaches: 
</p>

Tim McKay: Arthur F. Thurnau Professor of Physics, Director of the LSA Honors Program
<br>
Madeline Huberth: E<sup>2</sup>Coach Tailoring Specialist, 2011 UM Physics Grad and Gates Cambridge Scholar 
<br>
Jared Tritz: E<sup>2</sup>Coach Programmer, Founder of Cransort, designs fruit sorting machines
        """
    return html_content

def get_html_content_reminder4():
    html_content = """
<p>
Your first exam is out of the way! Whether you did well or not E<sup>2</sup>Coach may be of value to you as you gear up for the next midterm.
</p>

<p>
We are still allowing late sign ups to E<sup>2</sup>Coach for a couple more weeks and registered users will recieve personal advice as well as access to normative data about class performance.  To enroll in E<sup>2</sup>Coach simply go here and complete the online survey <a href='https://ecoach.lsa.umich.edu/w13physics/Opt_In/'>https://ecoach.lsa.umich.edu/w13physics/Opt_In/</a>.  From the same link you can choose to opt out and not receive further email reminders as well.
</p>

<p>
Most sincerely,
</p>

<p>
Your E<sup>2</sup>Coaches: 
</p>

Tim McKay: Arthur F. Thurnau Professor of Physics, Director of the LSA Honors Program
<br>
Madeline Huberth: E<sup>2</sup>Coach Tailoring Specialist, 2011 UM Physics Grad and Gates Cambridge Scholar 
<br>
Jared Tritz: E<sup>2</sup>Coach Programmer, Founder of Cransort, designs fruit sorting machines
        """
    return html_content


