{
    'name': 'Pharmacy',
    'version': '1.0',
    'category': 'Custom',
    'author': 'Oussama & Aymen',
    'description': 'A module to manage dashboards for clients, owners, and admins in a pharmacy system.',
    'depends': ['base', 'website', 'web'],
    'data': [
        'views/client.xml',
        'views/medicine.xml',
        'views/pharmacy.xml',
        'views/owner_login.xml',
        'views/owner_logup.xml',
        'views/owner_layout.xml',
        'views/owner_stock.xml',
        'views/owner_reservation.xml',

        'views/status_pending.xml',
        'views/status_declined.xml',
        'security/groups.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            '/pharmacy/static/css/style.css',
            '/pharmacy/static/js/script.js',
        ],
    },
    'installable': True,
    'application': True,
}


# 'views/menu.xml',
# 'security/ir.model.access.csv',
#    'views/client_login.xml',
#         'views/client_logup.xml',
#         'views/client_page.xml',

# 'views/admin_approval.xml',