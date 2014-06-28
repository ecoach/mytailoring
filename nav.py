from django.core.urlresolvers import reverse
from django.conf import settings
from djangotailoring.tailoringrequest import TailoringRequest
from djangotailoring.subjects import DjangoSubjectLoader
from djangotailoring.project import getproject

def inbox_nav(user, selected):
    
    all_messages = [ # leave as an example
            #'text'         
            #   'styling_class(es)',    
            #       'links_to'
            #           'permission_required'
            #               'selected'
            ["[DEMO] Kenny's first demo message<br>(testing.message)", 
                '',  
                    reverse('mytailoring:message_view', kwargs={'msg_id' : 'testing'}),
                        'any',
                            'testing',

            ]
        ]

    # overwrite the inbox defined statically above
    all_messages = usermessages(user)
    inbox_nav = [] 
    for nn in all_messages:
        # style the selected option
        if nn[4] == selected:
            nn[1] = 'current'
        # permission
        if nn[3] == 'any':
            inbox_nav.append(nn)
        elif nn[3] == 'staff' and user.is_staff:
            inbox_nav.append(nn)
    return inbox_nav

def all_messages_nav(user, selected):
    all_messages = allfiles() 
    inbox_nav = [] 
    for nn in all_messages:
        # style the selected option
        if nn[4] == selected:
            nn[1] = 'current'
        # permission
        if nn[3] == 'any':
            inbox_nav.append(nn)
        elif nn[3] == 'staff' and user.is_staff:
            inbox_nav.append(nn)
    inbox_nav = sorted(inbox_nav, key=lambda student: inbox_nav[4]) 
    return inbox_nav

def allfiles():
    from os import listdir
    from os.path import isfile, join
    the_dir = settings.DIR_PROJ + settings.MPROJ_NAME + '/Messages/'
    msg_files = [ f for f in listdir(the_dir) if isfile(join(the_dir,f)) ]
    all_messages = []
    for ff in msg_files:
        all_messages.append([ff, '', reverse('mypublisher:message_review', kwargs={'msg_id' : ff.split('.')[0]}), 'any', ff.split('.')[0]])
    return  all_messages

def usermessages(user):
    project = getproject()
    docpath = settings.DIR_PROJ + settings.MPROJ_NAME + '/Messages/inbox.messages'
    subject = user.get_profile().tailoringsubject
    ibm = TailoringRequest(project, docpath, subject)
    elemtree = ibm.render_section('InboxControl')
    messages = elemtree[0]
    inbox = []
    for mm in messages: 
        for prop in mm:
            if prop.tag == 'file':
                msg_file = prop.text
            elif prop.tag == 'subject':
                msg_subject = prop.text
        inbox.append([msg_file, msg_subject])
    all_messages = []
    for ff in inbox:
        all_messages.append([ff[1], '', reverse('mytailoring:message_view', kwargs={'msg_id' : ff[0]}), 'any', ff[0]])
    return  all_messages
