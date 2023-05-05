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



class proveedores(models.Model):
    _name = "proveedores.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Proveedor asociado a inducom"
    _rec_name = "nombre"
    # _order = 'ot_number desc'

    # funciones por defecto en campos

    #######################################################################################################
    #                                   Campos del modulo operaciones                                     #
    #                                                                                                     #
    #######################################################################################################

    codigo = fields.Char(string="Codigo", tracking=True)
    nombre = fields.Char(string="Nombre del proveedor", tracking=True)
    telefono = fields.Char(string="Telefono", tracking=True)
    ci_ruc = fields.Char(string="CI/RUC", tracking=True)
    correo = fields.Char(string="Correo", tracking=True)

    #######################################################################################################
    #                                   Funciones del modulo operaciones                                  #
    #                                                                                                     #
    #######################################################################################################
    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, "%s %s" % (field.codigo, field.nombre)))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ["|", ("codigo", operator, name), ("nombre", operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)





    #######################################################################################################
    #                                   Funciones que se ejecutan en el servidor                          #
    #                                                                                                     #
    #######################################################################################################

