{
    'name':'Solicitudes',
    'version':'1.0',
    'summary':'modulo de Solicitudes',
    'description':"""modulo encargado de generar Solicitudes """,
    'category':'Productivity',
    'sequence':-100,
    'website':'www.inducom-ec.com',
    'depends':[
        "web_timeline",
        "mail",
        "modulo_productos",
    ],
    'data': [
        "data/sol_sequence.xml",
        "data/mail_template_sol.xml",
        "reports/report_sol_main.xml",
        "reports/solicitud_pdf.xml",
        "security/ir.model.access.csv",
        "views/menu_view.xml",
        "views/new_sol_view.xml",
    ],
    'demo':[],
    'qweb':[],
    'installable':True,
    'application':True,
    'auto_install':False,
}