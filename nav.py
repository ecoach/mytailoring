from django.core.urlresolvers import reverse
from django.conf import settings

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
    all_messages = [] 
    for ff in allfiles():
        all_messages.append([ff,'', reverse('mycoach:message_view', kwargs={'msg_id' : ff.split('.')[0]}), 'any', ff])
   
    inbox_nav = [] 
    for nn in all_messages:
        # style the selected option
        #if nn[4] == selected:
        if str(nn[4]) == '.'.join([str(selected), 'messages']):
            nn[1] = 'current'
        # permission?
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
    return  msg_files

