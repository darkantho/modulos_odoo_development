{
    'name': 'Rics',
    'version': '1.0',
    'summary': 'modulo de Rics',
    'description': """modulo encargado de generar los Rics""",
    'category': 'Productivity',
    'sequence': -100,
    'website': 'www.inducom-ec.com',
    'depends': [
        "web_timeline",
        "mail",
        "modulo_productos",
        "modulo_clientes",
        "modulo_solicitudes"
    ],
    'data': [
        "data/ric_sequence.xml",
        "data/ric_mail_template.xml",
        "security/ir.model.access.csv",
        "reports/report_rics_main.xml",
        "reports/ric_template_pdf.xml",
        "views/menu_view.xml",
        "views/ric_view.xml",

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}