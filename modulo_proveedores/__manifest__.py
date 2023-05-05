{
    'name': 'Proveedores',
    'version': '1.0',
    'summary': 'modulo de proveedores',
    'description': """modulo encargado de registrar a los proveedores""",
    'category': 'Productivity',
    'sequence': -100,
    'website': 'www.inducom-ec.com',
    'depends': [
        "mail",
        "modulo_clientes"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/proveedor_menu.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}