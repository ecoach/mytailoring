import re
from django.conf import settings

class Messages:
    m_docs = dict() 
     
    # NAV STRUCTURE ==> menu["TAB_TEXT"].append( ["SIDE_TEXT" "UNIQUE_URL", "MESSAGE_DOC"])
    def __init__(self):
        #self.m_docs["Welcome_Message"] = "Welcome_Message.messages"

        self.m_docs["Advice_1_Home"] = "Advice_1_Home.messages"
        self.m_docs["Advice_1_Homework"] = "Advice_1_Homework.messages"
        self.m_docs["Advice_1_Lecture"] = "Advice_1_Lecture.messages"
        self.m_docs["Advice_1_Exams"] = "Advice_1_Exams.messages"
        #self.m_docs["Advice_1_Survey"] = "Advice_1_Survey.survey"

        self.m_docs["Exam_1_Prep_Home"] = "Exam_1_Prep_Home.messages"
        self.m_docs["Exam_1_Prep_Homework"] = "Exam_1_Prep_Homework.messages"
        self.m_docs["Exam_1_Prep_Lecture"] = "Exam_1_Prep_Lecture.messages"
        self.m_docs["Exam_1_Prep_Exams"] = "Exam_1_Prep_Exams.messages"
        self.m_docs["Exam_1_Prep_Survey"] = "Exam_1_Prep_Survey.survey"

        self.m_docs["Exam_1_Response_Home"] = "Exam_1_Response_Home.messages"
        self.m_docs["Exam_1_Response_Homework"] = "Exam_1_Response_Homework.messages"
        self.m_docs["Exam_1_Response_Lecture"] = "Exam_1_Response_Lecture.messages"
        self.m_docs["Exam_1_Response_Exams"] = "Exam_1_Response_Exams.messages"
        self.m_docs["Exam_1_Response_Survey"] = "Exam_1_Response_Survey.survey"

        self.m_docs["Exam_2_Response_Home"] = "Exam_2_Response_Home.messages"
        self.m_docs["Exam_2_Response_Homework"] = "Exam_2_Response_Homework.messages"
        self.m_docs["Exam_2_Response_Lecture"] = "Exam_2_Response_Lecture.messages"
        self.m_docs["Exam_2_Response_Exams"] = "Exam_2_Response_Exams.messages"
        self.m_docs["Exam_2_Response_Survey"] = "Exam_2_Response_Survey.survey"
        self.m_docs["Exam_2_Response_Survey_Testimonial"] = "Exam_2_Response_Survey_Testimonial.survey"

        self.m_docs["Exam_3_Response_Home"] = "Exam_3_Response_Home.messages"
        self.m_docs["Exam_3_Response_Homework"] = "Exam_3_Response_Homework.messages"
        self.m_docs["Exam_3_Response_Lecture"] = "Exam_3_Response_Lecture.messages"
        self.m_docs["Exam_3_Response_Exams"] = "Exam_3_Response_Exams.messages"
        self.m_docs["Exam_3_Response_Survey"] = "Exam_3_Response_Survey.survey"

        self.m_docs["Final_Exam_Response_Home"] = "Final_Exam_Response_Home.messages"
        self.m_docs["Final_Exam_Response_Homework"] = "Final_Exam_Response_Homework.messages"
        self.m_docs["Final_Exam_Response_Lecture"] = "Final_Exam_Response_Lecture.messages"
        self.m_docs["Final_Exam_Response_Exams"] = "Final_Exam_Response_Exams.messages"
        self.m_docs["Final_Exam_Response_Survey"] = "Final_Exam_Response_Survey.survey"

        self.m_docs["Test_Survey"] = "Test_Survey.survey"
        self.m_docs["Opt_Out"] = "Opt_Out.survey"

        self.m_docs["Profile"] = "Profile.messages"
        self.m_docs["FAQ"] = "FAQ.messages"

        """
        self.m_docs["Exam_1_Prep_Advice"] = "Exam_1_Prep_Advice.messages"
        self.m_docs["Exam_1_Prep_Home"] = "Exam_1_Prep_Home.messages"
        self.m_docs["Exam_1_Prep_Profile"] = "Exam_1_Prep_Profile.messages"
        self.m_docs["Exam_1_Prep_Survey"] = "Exam_1_Prep_Survey.survey"

        self.m_docs["Exam_1_Response_Advice"] = "Exam_1_Response_Advice.messages"
        self.m_docs["Exam_1_Response_Home"] = "Exam_1_Response_Home.messages"
        self.m_docs["Exam_1_Response_Profile"] = "Exam_1_Response_Profile.messages"
        self.m_docs["Exam_1_Response_Status"] = "Exam_1_Response_Status.messages"
        self.m_docs["Exam_1_Response_Survey"] = "Exam_1_Response_Survey.survey"

        self.m_docs["Exam_2_Response_Advice"] = "Exam_2_Response_Advice.messages"
        self.m_docs["Exam_2_Response_Home"] = "Exam_2_Response_Home.messages"
        self.m_docs["Exam_2_Response_Profile"] = "Exam_2_Response_Profile.messages"
        self.m_docs["Exam_2_Response_Status"] = "Exam_2_Response_Status.messages"
        self.m_docs["Exam_2_Response_Survey"] = "Exam_2_Response_Survey.survey"
        #self.m_docs["Exam_2_Response_Status_Survey"] = "Exam_2_Response_Status_Survey.survey"

        self.m_docs["Exam_3_Response_Advice"] = "Exam_3_Response_Advice.messages"
        self.m_docs["Exam_3_Response_Home"] = "Exam_3_Response_Home.messages"
        self.m_docs["Exam_3_Response_Profile"] = "Exam_3_Response_Profile.messages"
        self.m_docs["Exam_3_Response_Status"] = "Exam_3_Response_Status.messages"
 
        self.m_docs["Final_Exam_Response_Home"] = "Final_Exam_Response_Home.messages"
        self.m_docs["Final_Exam_Response_Status"] = "Final_Exam_Response_Status.messages"
        self.m_docs["Final_Exam_Response_Survey"] = "Final_Exam_Response_Survey.survey"
        """ 

        self.m_docs["Debug_Message_2"] = "Debug_Message_2.messages"
        self.m_docs["Debug_Message"] = "Debug_Message.messages"
        self.m_docs["Widget_Test"] = "Widget_Test.messages"

    def getlist(self):
        ls = []
        for key in self.m_docs:
            ls.append(key)
        return sorted(ls)
    
    def pathto(self, key):
        try:
            msg = self.m_docs[key]
        except: 
            #msg = self.m_docs["FAQ"]
            msg = self.m_docs[self.getlist()[0]]
        ret = "Messages/" + msg
        return ret

    @classmethod
    def is_survey(self, msg):
        # check for a *.survey suffix
        re1 = re.compile(r'^.*\.survey$')
        res1 = re1.search(self.m_docs[msg])
        if res1 == None:
            return False
        else:
            return True

class Nav:

    def __init__(self, requested):
        self.m_subsite = settings.URL_SUB
        self.m_requested = [] # not initializing this killed me for 2 hours!
        self.m_menu = dict()

        # main menu tab items (can be a super set, just has to be in order)
        self.m_tabs = ([
        "Home", 
        "Homework", 
        "Lecture", 
        "Exams", 
        "Profile", 
        "FAQ",
        ])

        # nav data structure to populate
        for tt in self.m_tabs:
            self.m_menu[tt] = []

        # STRUCTURE ==> menu["TAB_TEXT"].append( ["SIDE_TEXT" "UNIQUE_URL", "MESSAGE_DOC"])
        # ---everyone must have one entry under "Home"---

        
        self.m_menu["Profile"].append(["Profile", "Profile", "Profile"])
        self.m_menu["FAQ"].append([" ", "faq", "FAQ"])
       
        self.m_menu["Home"].append(["Advice Exam_1_Response", "Advice_Exam_1_Response", "Exam_1_Response_Home"])
        self.m_menu["Homework"].append(["Homework Exam_1_Response", "Homework_Exam_1_Response", "Exam_1_Response_Homework"])
        self.m_menu["Lecture"].append(["Lecture Exam_1_Response", "Lecture_Exam_1_Response", "Exam_1_Response_Lecture"])
        self.m_menu["Exams"].append(["Exams Exam_1_Response", "Exams_Exam_1_Response", "Exam_1_Response_Exams"])

        """ 
        self.m_menu["Home"].append(["Final Exam Response", "Final_Exam_Response", "Final_Exam_Response_Home"])

        self.m_menu["Home"].append(["Advice Exam_3_Response", "Advice_Exam_3_Response", "Exam_3_Response_Home"])
        self.m_menu["Homework"].append(["Homework Exam_3_Response", "Homework_Exam_3_Response", "Exam_3_Response_Homework"])
        self.m_menu["Lecture"].append(["Lecture Exam_3_Response", "Lecture_Exam_3_Response", "Exam_3_Response_Lecture"])
        self.m_menu["Exams"].append(["Exams Exam_3_Response", "Exams_Exam_3_Response", "Exam_3_Response_Exams"])

        self.m_menu["Home"].append(["Advice Exam_2_Response", "Advice_Exam_2_Response", "Exam_2_Response_Home"])
        self.m_menu["Homework"].append(["Homework Exam_2_Response", "Homework_Exam_2_Response", "Exam_2_Response_Homework"])
        self.m_menu["Lecture"].append(["Lecture Exam_2_Response", "Lecture_Exam_2_Response", "Exam_2_Response_Lecture"])
        self.m_menu["Exams"].append(["Exams Exam_2_Response", "Exams_Exam_2_Response", "Exam_2_Response_Exams"])

        self.m_menu["Home"].append(["Advice Exam_1_Prep", "Advice_Exam_1_Prep", "Exam_1_Prep_Home"])
        self.m_menu["Homework"].append(["Homework Exam_1_Prep", "Homework_Exam_1_Prep", "Exam_1_Prep_Homework"])
        self.m_menu["Lecture"].append(["Lecture Exam_1_Prep", "Lecture_Exam_1_Prep", "Exam_1_Prep_Lecture"])
        self.m_menu["Exams"].append(["Exams Exam_1_Prep", "Exams_Exam_1_Prep", "Exam_1_Prep_Exams"])

        self.m_menu["Home"].append(["Advice 1", "Advice_1", "Advice_1_Home"])
        self.m_menu["Homework"].append(["Homework 1", "Homework_1", "Advice_1_Homework"])
        self.m_menu["Lecture"].append(["Lecture 1", "Lecture_1", "Advice_1_Lecture"])
        self.m_menu["Exams"].append(["Exams 1", "Exams_1", "Advice_1_Exams"])
        """

        # prune out the dead tabs
        tabs = dict()
        for tt in self.m_menu:
            if len(self.m_menu[tt]) > 0:
                # save requested url
                tabs[tt] = self.m_menu[tt]
        self.m_menu = tabs 

        # rustle up the menu selection
        self.map_requested(requested)

    def map_requested(self, req):
        req = str(req.lstrip('/'))
        req = req[len(self.m_subsite):]
        req = req.split('/')[0]

        for tab in self.m_menu:
            ii = 0
            for sub in self.m_menu[tab]:
                if req == sub[1]:
                    # hopefully we find the request, save the tab and number of sub
                    self.m_requested.append(tab)
                    self.m_requested.append(ii)
                    self.m_requested.append(sub[1])
                    return
                ii += 1
        # everyone has a home tab, if we found no match default to it's first element
        self.m_requested.append(self.m_tabs[0])
        self.m_requested.append(0)
        self.m_requested.append("/")
           
    def get_requested_url(self):
        # not in use noted on July 22nd 2012
        return "/" + self.m_requested[2] + "/"
 
    def get_msgdoc(self):
        # dig through everthing
        # find the url and return the message doc key
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        ret = self.m_menu[tab][sub][2]
        return ret

    def sidemenu(self):
        # this nav structure sort of assumes single unique string identifiers for resources....
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        subs = []
        if len(self.m_menu[tab]) > 1:
            for ss in self.m_menu[tab]:
                tab = self.m_requested[0]
                sub = self.m_requested[1]
                comp = self.m_menu[tab][sub][1]
                if ss[1] == comp:
                    css = "current_side_item"
                else:
                    css = "side_item"
                href = self.m_subsite + ss[1]
                txt = ss[0]
                subs.append([txt, css, href])
        return subs

    def is_survey(self):
        msg = self.get_msgdoc()
        ret = Messages.is_survey(msg)
        return ret
 
    def decide_template(self):
        sides = self.sidemenu()
        # greater than two because if there's only one sub we don't display/acknowledge a side menu
        if len(sides) > 1:
            return True
        else:
            return False

    def topmenu(self):
        #self.menu["Home"].append([" ", "JanX_Home", "Advice_X_Home"])
        # [word, class, href]
        # [key, key=selected, sub[0]]
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        tabs = [] 
        for tt in self.m_menu: 
            if tt == tab: # mark the one you're on
                css = "current_page_item"
            else:
                css = "page_item" # leave the rest
            href = self.m_subsite + self.m_menu[tt][0][1]
            txt = tt
            tabs.append([txt, css, href])

        # sort/set the order
        ret = []
        for tt in self.m_tabs: 
            for ii in tabs:
                if ii[0] == tt:
                    ret.append(ii)
                    break
        return ret
          
class StaffNav:

    def __init__(self, requested):
        self.m_subsite = settings.URL_SUB + 'staff/'
        self.m_requested = [] # not initializing this killed me for 2 hours!
        self.m_menu = dict()

        # main menu tab items (can be a super set, just has to be in order)
        self.m_tabs = ([
        "Message Viewer",
        "Copy Student",
        "User Stats",
        "Data Loader",
        "Email Students",
        ])

        # nav data structure to populate
        for tt in self.m_tabs:
            self.m_menu[tt] = []

        # STRUCTURE ==> menu["TAB_TEXT"].append( ["SIDE_TEXT" "UNIQUE_URL"])
        # ---everyone must have one entry---
       
        self.m_menu["Message Viewer"].append(["", "message_viewer"])
        self.m_menu["Copy Student"].append(["", "copy_student"])
        self.m_menu["User Stats"].append(["", "usage_stats"])
        self.m_menu["Data Loader"].append(["", "data_loader"])
        self.m_menu["Email Students"].append(["", "email_students"])

        # prune out the dead tabs
        tabs = dict()
        for tt in self.m_menu:
            if len(self.m_menu[tt]) > 0:
                # save requested url
                tabs[tt] = self.m_menu[tt]
        self.m_menu = tabs 

        # rustle up the menu selection
        self.map_requested(requested)

    def map_requested(self, req):
        req = str(req.lstrip('/'))
        req = req[len(self.m_subsite):]
        req = req.split('/')[0]

        for tab in self.m_menu:
            ii = 0
            for sub in self.m_menu[tab]:
                if req == sub[1]:
                    # hopefully we find the request, save the tab and number of sub
                    self.m_requested.append(tab)
                    self.m_requested.append(ii)
                    self.m_requested.append(sub[1])
                    return
                ii += 1
        # everyone has a tab, if we found no match default to it's first element
        self.m_requested.append(self.m_tabs[0])
        self.m_requested.append(0)
        self.m_requested.append("/")
           
    def side_menu(self):
        # this nav structure sort of assumes single unique string identifiers for resources....
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        subs = []
        if len(self.m_menu[tab]) > 1:
            for ss in self.m_menu[tab]:
                tab = self.m_requested[0]
                sub = self.m_requested[1]
                comp = self.m_menu[tab][sub][1]
                if ss[1] == comp:
                    css = "current_side_item"
                else:
                    css = "side_item"
                href = self.m_subsite + ss[1]
                txt = ss[0]
                subs.append([txt, css, href])
        return subs

    def decide_template(self):
        sides = self.sidemenu()
        # greater than two because if there's only one sub we don't display/acknowledge a side menu
        if len(sides) > 1:
            return True
        else:
            return False

    def main_menu(self):
        #self.menu["Home"].append([" ", "JanX_Home", "Advice_X_Home"])
        # [word, class, href]
        # [key, key=selected, sub[0]]
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        tabs = [] 
        for tt in self.m_menu: 
            if tt == tab: # mark the one you're on
                css = "current_page_item"
            else:
                css = "page_item" # leave the rest
            href = self.m_subsite + self.m_menu[tt][0][1]
            txt = tt
            tabs.append([txt, css, href])

        # sort/set the order
        ret = []
        for tt in self.m_tabs: 
            for ii in tabs:
                if ii[0] == tt:
                    ret.append(ii)
                    break
        return ret
          
class DataLoaderNav:

    def __init__(self, requested):
        self.m_subsite = settings.URL_SUB + 'staff/data_loader/'
        self.m_requested = [] # not initializing this killed me for 2 hours!
        self.m_unique = ''
        self.m_menu = dict()

        # main menu tab items (can be a super set, just has to be in order)
        self.m_tabs = ([
        "1. Upload File",
        "2. Review File",
        "3. Digest Data",
        "4. Commit",
        "Archive",
        "Help",
        ])

        # nav data structure to populate
        for tt in self.m_tabs:
            self.m_menu[tt] = []

        # STRUCTURE ==> menu["TAB_TEXT"].append( ["SIDE_TEXT" "UNIQUE_URL"])
        # ---everyone must have one entry---
       
        self.m_menu["1. Upload File"].append(["", "file_upload"])
        self.m_menu["2. Review File"].append(["", "file_review"])
        self.m_menu["3. Digest Data"].append(["", "data_digest"])
        self.m_menu["4. Commit"].append(["", "mts_load"])
        self.m_menu["Archive"].append(["", "archive"])
        self.m_menu["Help"].append(["", "help"])

        # prune out the dead tabs
        tabs = dict()
        for tt in self.m_menu:
            if len(self.m_menu[tt]) > 0:
                # save requested url
                tabs[tt] = self.m_menu[tt]
        self.m_menu = tabs 

        # rustle up the menu selection
        self.map_requested(requested)

    def reverse(self):
        return '/' + self.m_subsite + self.m_unique + '/'

    def map_requested(self, req):
        req = str(req.lstrip('/'))
        req = req[len(self.m_subsite):]
        req = req.split('/')[0]
        self.m_unique = req

        for tab in self.m_menu:
            ii = 0
            for sub in self.m_menu[tab]:
                if self.m_unique == sub[1]:
                    # hopefully we find the request, save the tab and number of sub
                    self.m_requested.append(tab)
                    self.m_requested.append(ii)
                    self.m_requested.append(sub[1])
                    return
                ii += 1
        # everyone has a tab, if we found no match default to it's first element
        self.m_requested.append(self.m_tabs[0])
        self.m_requested.append(0)
        self.m_requested.append("/")
           
    def side_menu(self):
        # this nav structure sort of assumes single unique string identifiers for resources....
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        subs = []
        if len(self.m_menu[tab]) > 1:
            for ss in self.m_menu[tab]:
                tab = self.m_requested[0]
                sub = self.m_requested[1]
                comp = self.m_menu[tab][sub][1]
                if ss[1] == comp:
                    css = "current_side_item"
                else:
                    css = "side_item"
                href = self.m_subsite + ss[1]
                txt = ss[0]
                subs.append([txt, css, href])
        return subs

    def decide_template(self):
        sides = self.sidemenu()
        # greater than two because if there's only one sub we don't display/acknowledge a side menu
        if len(sides) > 1:
            return True
        else:
            return False

    def main_menu(self):
        #self.menu["Home"].append([" ", "JanX_Home", "Advice_X_Home"])
        # [word, class, href]
        # [key, key=selected, sub[0]]
        tab = self.m_requested[0]
        sub = self.m_requested[1]
        tabs = [] 
        for tt in self.m_menu: 
            if tt == tab: # mark the one you're on
                css = "current_page_item"
            else:
                css = "page_item" # leave the rest
            href = self.m_subsite + self.m_menu[tt][0][1]
            txt = tt
            tabs.append([txt, css, href])

        # sort/set the order
        ret = []
        for tt in self.m_tabs: 
            for ii in tabs:
                if ii[0] == tt:
                    ret.append(ii)
                    break
        return ret
          


