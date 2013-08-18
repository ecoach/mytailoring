from django.core.urlresolvers import reverse
from django.conf import settings
from djangotailoring.tailoringrequest import TailoringRequest
from djangotailoring.subjects import DjangoSubjectLoader
from djangotailoring.project import getproject

def inbox_nav(user, selected):
    
    all_messages = [
            #'text'         
            #   'styling_class(es)',    
            #       'links_to'
            #           'permission_required'
            #               'selected'
            ["[DEMO] Kenny's first demo message<br>(testing.message)", 
                '',  
                    reverse('mycoach:message_view', kwargs={'msg_id' : 'testing'}),
                        'any',
                            'testing',

            ],
            ["[Demo] Widgets open house<br>(widgets.message)", 
                '',  
                    reverse('mycoach:message_view', kwargs={'msg_id' : 'widgets'}),
                        'any',
                            'widgets',

            ],
            ["[PRACTICE Chem 130]<br>(chem130.message)", 
                '',  
                    reverse('mycoach:message_view', kwargs={'msg_id' : 'chem130'}),
                        'any',
                            'chem130',

            ],
            ["[PRACTICE MCDB 310]<br>(mcdb310.message)", 
                '',  
                    reverse('mycoach:message_view', kwargs={'msg_id' : 'mcdb310'}),
                        'any',
                            'mcdb310',

            ],
            ["[PRACTICE Stats 250]<br>(stats250.message)", 
                '',  
                    reverse('mycoach:message_view', kwargs={'msg_id' : 'stats250'}),
                        'any',
                            'stats250',

            ],
            ["[PRACTICE Physics 140,240,135,235]<br>(physicsXYZ.message)", 
                '',  
                    reverse('mycoach:message_view', kwargs={'msg_id' : 'physicsXYZ'}),
                        'any',
                            'physicsXYZ',

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

def allfiles():
    from os import listdir
    from os.path import isfile, join
    the_dir = settings.DIR_MYDATA + settings.MPROJ_NAME + '/Messages/'
    msg_files = [ f for f in listdir(the_dir) if isfile(join(the_dir,f)) ]
    all_messages = []
    for ff in msg_files:
        all_messages.append([ff, '', reverse('mycoach:message_view', kwargs={'msg_id' : ff.split('.')[0]}), 'any', ff.split('.')[0]])
    return  all_messages

def usermessages(user):
    project = getproject()
    docpath = settings.DIR_MYDATA + settings.MPROJ_NAME + '/Messages/inbox.messages'
    subject = user.get_profile().tailoringsubject
    ibm = TailoringRequest(project, docpath, subject)
    if not 'InboxControl' in ibm.sections.keys():
        return allfiles() 
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
        all_messages.append([ff[1], '', reverse('mycoach:message_view', kwargs={'msg_id' : ff[0]}), 'any', ff[0]])
    return  all_messages
