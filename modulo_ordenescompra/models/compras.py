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



class ordenescompras(models.Model):
    _name = "ordenescompras.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "orden de compra"
    # _rec_name = "ot_number"
    # _order = 'ot_number desc'

    #######################################################################################################
    #                                   Campos del modulo ordenes de compra                               #
    #                                                                                                     #
    #######################################################################################################
    num_orden_compra = fields.Integer(string="Numero de Documento")
    codigo_proveedor = fields.Char(string="Codigo del Proveedor")
    orden_trabajo = fields.Many2one("db.ots",string="Orden Asociada")
    orden_texto = fields.Char(related="orden_trabajo.ot_number",string="Orden Numero")
    nombre_proveedor = fields.Char(string="Nombre del proveedor")
    fecha_ingreso = fields.Datetime(string="Fecha de Aprobacion")
    fecha_aprobacion = fields.Datetime(string="Fecha de Entrega")
    aprobacion = fields.Boolean(string="Orden Aprobada?")
    codigo_articulo = fields.Char(string="Articulo")

    #######################################################################################################
    #                                   Funciones del modulo operaciones                                  #
    #                                                                                                     #
    #######################################################################################################
    # def name_get(self):
    #     res = []
    #     for field in self:
    #         res.append((field.id, "%s %s" % (field.ot_number, field.client_name.client )))
    #     return res
    #
    # def get_client_name(self):
    #     return self.client_name.client
    #
    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     if args is None:
    #         args = []
    #     domain = args + ["|", ("ot_number", operator, name), ("client_name.client", operator, name)]
    #     return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

