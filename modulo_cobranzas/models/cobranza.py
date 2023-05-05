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

permisos = ["Jorge Ibañez", "Jonathan Tejena", "Anthony Villacis"]

class dbots(models.Model):
    _name = "cobranza.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "cobranzas"
    # _rec_name = "ot_number"
    # _order = 'ot_number desc'


    #######################################################################################################
    #                                   Campos del modulo operaciones                                     #
    #                                                                                                     #
    #######################################################################################################

    cliente = fields.Many2one("clientes.inducom",string="Cliente")
    fecha_facturacion = fields.Date(string="Fecha de Facturacion")
    plazo = fields.Integer(string="Plazo")
    fecha_vencimiento = fields.Date(string="Fecha de Vencimiento")
    mora = fields.Integer(string="Dias de Mora")
    num_fact = fields.Integer(String='Numero de Factura')
    saldo = fields.Float(string="Saldo Pendiente")

    situacion = fields.Selection([("vencida", "VENCIDA"),
                                  ("vencepronto", "VENCE PRONTO"),
                                  ("novencida", "NO VENCIDA"),
                                  ("vencehoy","VENCE HOY")], string='Situación')

    estado = fields.Selection([("activo", "ACTIVO"),
                               ("anulado", "ANULADO")], string='Estado')

    pendiente = fields.Selection([("si","SI") ,("no","NO")],string='Pendiente')
    email = fields.Char(String='Email de cobro')

    #######################################################################################################
    #                                   Funciones del modulo operaciones                                  #
    #                                                                                                     #
    #######################################################################################################
    def action_send_cobro(self):

        template_mail_id = self.env.ref("modulo_cobranzas.cobranza_mail_template").id
        template = self.env["mail.template"].browse(template_mail_id)
        template.send_mail(self.id, True)

    def get_client_name(self):
        return self.cliente.client


    #######################################################################################################
    #                                   Funciones que se ejecutan en el servidor                          #
    #                                                                                                     #
    #######################################################################################################
