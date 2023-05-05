from copy import copy
from datetime import datetime
from email.policy import default
from pyexpat import model
import string
from xml.dom import ValidationErr
from odoo import api,models,fields

class productos(models.Model):
    _name = "productos.inducom"
    _description = "database for new products"
    _rec_name = "product_id"

    product_id = fields.Char(string="codigo",required=True)
    product_name = fields.Char(string="nombre",required=True)
    qty = fields.Integer(string="cantidad",default=0)
    status = fields.Selection([
        ("a",""),
        ("verificacion","En verificacion"),
        ("disponible","disponible"),
        ("compra","Compra Pendiente"),
        ("Compra2","Compra realizada")
    ],string="estado",default="verificacion")


    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, "%s %s" % (field.product_id, field.product_name)))
        return res
    
