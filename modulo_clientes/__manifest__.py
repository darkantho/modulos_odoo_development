{
    'name':'Clientes',
    'version':'1.0',
    'summary':'modulo clientes inducom',
    'description':"""modulo encargado de guardar clientes inducom""",
    'category':'Productivity',
    'sequence':-100,
    'website':'www.inducom-ec.com',
    'depends':[],
    'data':[
        "data/client_data.xml",
        "security/ir.model.access.csv",
        "views/main_view.xml",
        "views/client_view.xml",
    ],
    'demo':[],
    'qweb':[],
    'installable':True,
    'application':True,
    'auto_install':False,


}