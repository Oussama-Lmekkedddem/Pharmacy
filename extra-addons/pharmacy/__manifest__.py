{
    'name': 'Pharmacy',
    'version': '1.0',
    'category': 'Custom',
    'author': 'Oussama & Aymen',
    'description': 'A module to manage dashboards for clients, owners, and admin in a pharmacy system.',
    'depends': ['base', 'website', 'web'], # 'mail', 'account', 'product'],
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
        'security/ir.model.access.csv',
        'security/groups.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/pharmacy/static/css/style.css',
            '/pharmacy/static/js/script.js',
        ],
    },
    'icon': '/pharmacy/static/description/icon.jpg',
    'installable': True,
    'application': True,
}

# 'data/email_template.xml',