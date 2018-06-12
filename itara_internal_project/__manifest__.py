
{
    'name': 'Itara Internal Project',
    'version': '1.0',
    'category': 'Generic Modules/Account',
    'summary': 'Analysis Report, Stages of the project',
    'description': """This module contains the Project Management Features""",
    'author': 'Itara',
    'website': "https://www.odoo.com/page/project-management",
    'images':['static/description/testing.png',],
    'depends': ['base', 'account', 'sale', 'sale_timesheet','project_task_code','project'],
    'data': ['data/view.xml','data/sale_order_report.xml'],
    'demo': [ ],
    'test': [ ],
    'installable': True,
    'auto_install': False,
    'application': True,
  }
