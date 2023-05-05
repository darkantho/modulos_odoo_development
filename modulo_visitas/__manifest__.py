{
    'name': 'Visitas',
    'version': '1.0',
    'summary': 'modulo de visitas',
    'description': """modulo encargado de registrar las visitas del personal de ventas""",
    'category': 'Productivity',
    'sequence': -100,
    'website': 'www.inducom-ec.com',
    'depends': [
        "mail",
        "modulo_clientes",
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/main_menu.xml",
        "views/visita_menu.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}