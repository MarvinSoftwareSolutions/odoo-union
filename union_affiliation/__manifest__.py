# -*- coding: utf-8 -*-
{
    'name': "Sindicato - Afiliaciones",
    'summary': """
        Módulo de gestion de gremial de afiliados.""",
    'author': "Mueve",
    'website': "https://github.com/Mueve-TEC",
    'category': 'Union',
    'version': '1.0',
    "license": "AGPL-3",
    'depends': ['base','mail'],
    'data': [
        'security/affiliation_security.xml',
        'security/ir.model.access.csv',
        'data/affiliation_number_seq.xml',
        'data/affiliation_type_default.xml',
        'wizards/affiliation_number.xml',
        'views/affiliate_views.xml',
        'views/affiliate_child_views.xml',
        'views/affiliate_type_views.xml',
        'views/affiliation_period_views.xml',
        'views/affiliation_configuration_view.xml',
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "installable": True,
}
