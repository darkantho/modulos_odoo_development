{
    'name': 'Cobranzas',
    'version': '1.0',
    'summary': 'modulo de cobranzas',
    'description': """modulo encargado de almacenar los pagos pendientes""",
    'category': 'Productivity',
    'sequence': -100,
    'website': 'www.inducom-ec.com',
    'depends': [
        "web_timeline",
        "mail",
        "modulo_productos",
    ],
    'data': [
        "data/cobranzas_template.xml",
        "security/ir.model.access.csv",
        "views/menu_view.xml",
        "views/cobros_menu.xml",

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
