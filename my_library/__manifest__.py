{
    'name': "My library",
    'version': '13.0.1.0.1',
    'summary': "Manage books easily",
    'description': """
Manage Library
==============
Description related to library.
""",
    'post_init_hook': 'add_book_hook',
    'author': "Your name",
    'website': "http://www.example.com",
    'category': 'Library',
    'version': '13.0.1',
    'depends': ['base_setup', 'website'],
    'data': [

        'views/library_book.xml',
        'views/library_book_categ.xml',
        'views/library_book_rent.xml',
        'wizard/library_book_rent_wizard.xml',
        'wizard/library_book_return_wizard.xml',
        'views/library_rent_statistics.xml',
        'views/res_config_settings.xml',
        'views/templates.xml',
        'security/groups.xml',
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'data/data.xml'

    ],
    'demo': [
        'data/demo.xml'
    ],'assets': {
        'web.assets_frontend': [
            'my_library/static/src/js/my_library.js',
            'my_library/static/src/css/my_library.css',
            'my_library/static/src/scss/my_library.scss'

        ],
    },
}
