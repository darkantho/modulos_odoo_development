{
    'name':'Postventa',
    'version':'1.0',
    'summary':'modulo de Postventa',
    'description':"""modulo encargado de generar las Postventa""",
    'category':'Productivity',
    'sequence':-100,
    'website':'www.inducom-ec.com',
    'depends':[
        "web_timeline",
        "mail",
        "modulo_productos",
    ],
    'data': [
        "data/cron_orders_postventa.xml",
        "data/mail_template.xml",
        "security/ir.model.access.csv",
        "views/menu_view.xml",
        "views/postventa_view.xml"

    ],
    'demo':[],
    'qweb':[],
    'installable':True,
    'application':True,
    'auto_install':False,
}