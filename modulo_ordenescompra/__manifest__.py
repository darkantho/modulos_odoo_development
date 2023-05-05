{
    'name':'Ordenes de compra',
    'version':'1.0',
    'summary':'modulo de ordenes de compra',
    'description':"""modulo encargado de registrar las ordenes de compra""",
    'category':'Productivity',
    'sequence':-100,
    'website':'www.inducom-ec.com',
    'depends':[
        "web_timeline",
        "mail",
        "modulo_productos",
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/menu_view.xml",
        "views/compras_view.xml"

    ],
    'demo':[],
    'qweb':[],
    'installable':True,
    'application':True,
    'auto_install':False,
}