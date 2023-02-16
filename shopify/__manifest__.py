# -*- coding: utf-8 -*-
{
    'name': "Shopify",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'auth_signup', 'web', 'http_routing'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/s_config.xml",
        "views/s_store_info.xml",
        "views/s_xero_config.xml",
        "views/s_store_order.xml",
        "views/s_products.xml",
        "views/s_combo.xml",
        "views/s_combo_reprot.xml",
        # "views/xero_info.xml",
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
