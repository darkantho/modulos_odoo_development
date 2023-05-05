{
    'name':'productos',
    'version':'1.0',
    'summary':'modulo productos inducom',
    'description':"""modulo encargado de guardar productos inducom""",
    'category':'Productivity',
    'sequence':-100,
    'website':'www.inducom-ec.com',
    'depends':[],
    'data':[
        "data/product_tag_data.xml",
        "security/ir.model.access.csv",
        "views/main_view.xml",
        "views/product_view.xml",
    ],
    'demo':[],
    'qweb':[],
    'installable':True,
    'application':True,
    'auto_install':False,


}