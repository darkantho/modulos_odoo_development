from copy import copy
from datetime import datetime, date, timedelta
from email.policy import default
from pyexpat import model
import string
from xml.dom import ValidationErr
from odoo import api, models, fields
from odoo import _
import base64
import xlsxwriter
from io import BytesIO
import json
from odoo.tools import date_utils



class rentabilidad(models.Model):
    _name = "rentabilidades.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Rentabilidad"
    # _rec_name = "ot_number"
    # _order = 'ot_number desc'


    #######################################################################################################
    #                                   Campos del modulo operaciones                                     #
    #                                                                                                     #
    #######################################################################################################
    cuadro_rentabilidad_num = fields.Char(string="Cuadro de Rentabilidad #", traking=True, required=True)
    fecha_requision = fields.Datetime(string="Requision de compra", tracking=True, required=True)
    solicitante = fields.Char(string="Solicitante", tracking=True, required=True)
    cliente = fields.Many2one("clientes.inducom", string="Cliente", tracking=True, required=True)
    pvp = fields.Float(string="PVP", default=0, tracking=True)
    Rentabilidad = fields.Float(string="Rentabilidad", default=0, tracking=True)
    Rentabilidad_percent = fields.Float(string="Rentabilidad(%)", default=0, tracking=True)
    listado = fields.One2many("productos.rentabilidades.inducom", "order_id", string="Lista de material")
    #######################################################################################################
    #                                   Funciones del modulo operaciones                                  #
    #                                                                                                     #
    #######################################################################################################
    # def name_get(self):
    #     res = []
    #     for field in self:
    #         res.append((field.id, "%s %s" % (field.ot_number, field.client_name.client )))
    #     return res


    def calculo_rent(self):
        rentabilidad_lista = []
        for record in self.listado:
            record.costo = record.cantidad * record.precio_unitario
            rentabilidad_lista.append(record.costo)

        self.Rentabilidad = sum(rentabilidad_lista)
        self.Rentabilidad_percent = ((self.pvp-sum(rentabilidad_lista))/self.pvp)*100



    #######################################################################################################
    #                                   Funciones que se ejecutan en el servidor                          #
    #                                                                                                     #
    #######################################################################################################




#######################################################################################################
#                                   Modelo de datos internos al modelo principal                      #
#                                                                                                     #
#######################################################################################################
class productos_rentabilidad(models.Model):
    _name = "productos.rentabilidades.inducom"
    _description = "modelo para indexar los productos de las rentabilidades"

    material_id = fields.Many2one("productos.inducom", string="Codigo")
    cantidad = fields.Float(string="Cantidad", default=1)
    producto = fields.Char(related="material_id.product_name",string="Producto")
    proveedor = fields.Many2one("proveedores.inducom", string="proveedor")
    orden_compra = fields.Char(string="O/C")
    precio_unitario = fields.Float(string="Precio Unitario")
    costo = fields.Float(string="Costo")
    estado = fields.Selection([
        ("stock", "STOCK"),
        ("realizado", "REALIZADO")
    ], string="Status", default="")
    order_id = fields.Many2one("rentabilidades.inducom", string="lista")



