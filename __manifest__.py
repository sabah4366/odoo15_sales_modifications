# -*- coding: utf-8 -*-
{
    'name': "sales task",
    'summary': """ sales task """,
    'description': """ sales task""",
    'sequence':-300,
    'author': "Class",
    'website': "http://www.yourcompany.com",
    'category': '',
    'version': '0.1',
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/sale_menu.xml',
        'views/project_estimation_view.xml',
        'views/description.xml',
        'views/sale_order_inherit.xml',
        'views/color_master.xml',
        'views/job_order.xml',
        'report/report.xml',
        'report/job_order_report_template.xml',

    ],


    'demo': [],
    'application':True,
    'auto_install': False,
    'licence':'LGPL-3'
}
