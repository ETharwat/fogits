# -*- coding: utf-8 -*-
{
    'name': "Portal Inbox",

    'summary': """
        Messaging System""",

    'description': """
        This module help student (Portal User) to communicate with teachers (Internal User) through messaging system 
    """,

    'author': "Eslam Tharwat",
    'website': "eslam.tharwaat@gmail.com",

    # for the full list
    'category': 'Portal',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','portal','openeducat_core'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/incoming.xml',
        'views/templates.xml',
        'data/data.xml',
    ],

}