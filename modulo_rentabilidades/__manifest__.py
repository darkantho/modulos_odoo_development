{
    'name': 'Rentabilidades',
    'version': '1.0',
    'summary': 'modulo de Rentabilidades',
    'description': """modulo encargado de llevar a cargo las Rentabilidades de las OT""",
    'category': 'Productivity',
    'sequence': -100,
    'website': 'www.inducom-ec.com',
    'depends': [
        "mail",
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/main_menu.xml",
        "views/rentabilidad_interface.xml",
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False
}