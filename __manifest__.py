{

    'name': 'Technical Order  ',
    'version': '1.0.0',
    'author': 'mohamed',
    'sequence': -19,
    'website': ' ',
    'category': '',
    'summary': '',
    'description': """""",
    'demo': [],
    'depends': ['sale','base','purchase','mail'],
    'data': ['security/group.xml',
             "security/ir.model.access.csv",
             'data/email_template.xml',
             'data/sequence.xml',
             'views/technical_order_views.xml',
             'wizard/technical_wizard_views.xml',
             "report/report.xml",
             'report/technical_order_report.xml',
             'views/res_partner_inherit.xml',
             ],
    # 'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}
