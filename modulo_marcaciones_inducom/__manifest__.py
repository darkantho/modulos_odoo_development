{
    'name':'Marcaciones',
    'version':'1.0',
    'summary':'modulo de marcaciones del personal de inducom',
    'description':"""modulo encargado de llevar a cargo las marcaciones del personal""",
    'category':'Productivity',
    'sequence':-100,
    'website':'www.inducom-ec.com',
    'depends':[
        "mail",
    ],
    'data':[
        "data/marcaciones_mail_template.xml",
        "security/ir.model.access.csv",
        "views/marcaciones_views.xml",
        "views/menu_view.xml",
    ],
    'demo':[],
    'qweb':[],
    'installable':True,
    'application':True,
    'auto_install':False,
}