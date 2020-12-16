# -*- coding: utf-8 -*-
{
    'name': "method_repair_invoice",

    'summary': """
                Creación de facturas a partir las ordenes de reparación
                """,

    'description': """
        Reemplazo el metodo nativo que crea las facturas en el contabilidad
    """,

    'author': "Method",
    'website': "http://www.method.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp_repair'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
