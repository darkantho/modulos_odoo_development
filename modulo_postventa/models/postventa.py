from copy import copy
from datetime import datetime, date, timedelta
from email.policy import default
from pyexpat import model
import string
from xml.dom import ValidationErr
from odoo import api, models, fields
from odoo import _
from odoo import modules, tools
import base64
import xlsxwriter
from io import BytesIO
import json
from odoo.tools import date_utils



class postventa(models.Model):
    _name = "postventa.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "postventa"
    # _rec_name = "ot_number"
    # _order = 'ot_number desc'

    #######################################################################################################
    #                                   Campos del modulo operaciones                                     #
    #                                                                                                     #
    #######################################################################################################
    num_fact = fields.Integer(string="Numero de Documento")
    cliente = fields.Many2one("clientes.inducom")
    ruc = fields.Char(string="RUC")
    fecha_emision = fields.Datetime(string="Fecha de Emision")
    codigo = fields.Char(string="Codigo Principal")
    descripcion = fields.Char(string="Detalle del codigo")

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

    def campains_send_server(self):
        print("funcion")

    def action_send_postventa(self):

        template_mail_id = self.env.ref("modulo_postventa.postventa_mail_template").id
        template = self.env["mail.template"].browse(template_mail_id)
        template.send_mail(self.id, True)

    def get_client_name(self):
        return self.cliente.client

    def get_base64_file(self):
        pathfile = modules.module.get_resource_path("modulo_postventa","static","src","img","Inducom_Ecuador_2.png")
        with open(pathfile, "rb") as inducom_img:
            image_content = inducom_img.read()
            datos = base64.b64encode(image_content).decode('utf-8')
            return f'data:image/png;base64,{datos}'

    def get_base64_file_2(self):
        pathfile = modules.module.get_resource_path("modulo_postventa","static","src","img","mantenimiento_mecanico.jpg")
        with open(pathfile, "rb") as inducom_img:
            image_content = inducom_img.read()
            datos = base64.b64encode(image_content).decode('utf-8')
            return f'data:image/jpg;base64,{datos}'

    def get_base64_file_3(self):
        pathfile = modules.module.get_resource_path("modulo_postventa","static","src","img","mantenimiento1.jpg")
        with open(pathfile, "rb") as inducom_img:
            image_content = inducom_img.read()
            datos = base64.b64encode(image_content).decode('utf-8')
            return f'data:image/jpg;base64,{datos}'

    def get_base64_file_4(self):
        pathfile = modules.module.get_resource_path("modulo_postventa","static","src","img","trabajando_2.jpg")
        with open(pathfile, "rb") as inducom_img:
            image_content = inducom_img.read()
            datos = base64.b64encode(image_content).decode('utf-8')
            return f'data:image/png;base64,{datos}'

    def get_base64_file_5(self):
        pathfile = modules.module.get_resource_path("modulo_postventa","static","src","img","bomba_de_agua.jpg")
        with open(pathfile, "rb") as inducom_img:
            image_content = inducom_img.read()
            datos = base64.b64encode(image_content).decode('utf-8')
            return f'data:image/jpg;base64,{datos}'