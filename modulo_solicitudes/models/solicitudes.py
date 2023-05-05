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
from odoo.exceptions import ValidationError
import requests
import re

permisos = ["Anthony Villacis", "Diana Abad"]
# numeros = ["593979101572", "593982749822", "593994111721"]
numeros = ["593979101572"]

class Solicitudes_inducom(models.Model):
    _name = "solicitudes.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "solicitud de trabajo"
    _rec_name = "sol_number"
    _order = 'sol_number desc'

    #######################################################################################################
    #                                   Campos del modulo Solicitudes                                     #
    #                                                                                                     #
    #######################################################################################################
    sol_number = fields.Char(string="Nº Solicitud", index=True, readonly=True,
                             default=lambda self: _("Nueva Solicitud"))
    fecha_incio = fields.Datetime(string="Fecha", readonly=True)
    client_name = fields.Many2one("clientes.inducom", string="Cliente", tracking=True, required=True)
    responsable = fields.Char(string="Funcionario Responsable (cliente)", tracking=True, required=True)
    informacion_adicional = fields.Text(string="Datos adicionales", tracking=True, required=True)
    area_sol = fields.Selection([
        ("ta", "Taller"),
        ("ve", "Ventas"),
        ("com", "Compras"),
    ], string="Area Solicitante", tracking=True, required=True)
    email_client = fields.Char(string="Correo de contacto", tracking=True, required=True)
    celular = fields.Char(string="Celular de contacto", tracking=True, required=True)
    telefono = fields.Char(string="Telefono")
    created_by = fields.Char(string="Vendedor", required=True, default=lambda self: self.env.user.name)
    email_user = fields.Char(string="Correo Vendedor", required=True, default=lambda self: self.env.user.email)
    factura = fields.Char(string="Factura", tracking=True, required=True)
    fecha_factura = fields.Date(string="Fecha Factura", tracking=True, required=True)
    equipo = fields.Char(string="Equipo", tracking=True, required=True)
    serie = fields.Char(string="Serie", tracking=True, required=True)
    modelo = fields.Char(string="modelo", tracking=True, required=True)
    trabajo = fields.Selection([
        ("RD", "Revisión y Diagnostico (Pagado)"),
        ("MR", "Mantenimiento de Rutina (Pagado)"),
        ("G", "Garantia"),
        ("ARI", "Arranque Inicial"),
        ("VD", "Visita por Diagnostico"),
        ("VG", "Visita por Garantia"),
        ("MS", "Mantenimiento en Sitio"),
        ("PG","Posible Garantia")
    ], string="Tipo de Trabajo", default="1", tracking=True, required=True)
    descripcion = fields.Text(string="Descripcion del Problema", tracking=True, required=True)
    evidencia1 = fields.Binary(string="Evidencia(Video)", attachment=True, tracking=True)
    evidencia2 = fields.Binary(string="Evidencia(imagen)", attachment=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get("sol_number", _("Nueva Solicitud")) == _("Nueva Solicitud"):
            vals["sol_number"] = self.env['ir.sequence'].next_by_code("sol_counter") or "/"
        vals["fecha_incio"] = datetime.now()
        res = super(Solicitudes_inducom, self).create(vals)
        for i in numeros:
            url_w = "https://graph.facebook.com/v15.0/114965038179176/messages"
            Headers = {"content-Type": "application/json",
                       "Authorization": "Bearer EAAHbZBXr5vnEBAJqb9MNLSTBZAFDZBQR8jjWjwlAYnwRxFslr8Ww5StYuOEbpnaRtpLBXcyUfWwCTF4cEEgFnEz4hs0RuAREhrMxgKzXHK7GOCwCZCnSaGo6qM1aLxzsh5L2jz9OMirMXvTIyPhuMbEfnQu3eM4ygW3zfFz4ASM6Hk11ZB7Lt"}
            data = {"messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": f"{i}",
                    "type": "text",
                    "text": {
                        "preview_url": False,
                        "body": f"""Solicitud de Trabajo Creada\n solicitud:{vals["sol_number"]} \n cliente:{res.client_name.client} \n vendedor:{vals["created_by"]}\nfecha de Generacion:{datetime.now()}"""
                    }
                    }
            response = requests.post(url=url_w, headers=Headers, json=data)
        # template_mail_id = self.env.ref("modulo_solicitudes.sol_mail_template").id
        # template = self.env["mail.template"].browse(template_mail_id)
        # template.send_mail(res.id, True)
        return res

    def create_ot(self):

        if self.env.user.name in permisos:
            if self.env["db.ots"].search_count([('sol_number', '=', self.sol_number)]) > 0:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'Esta Solicitud ya fue procesada',
                        'type': 'danger',
                        'sticky': True,
                    }
                }
            else:
                ot_values = {
                    'sol_number': self.sol_number,
                    'ot_number': self.env['ir.sequence'].next_by_code("ot_counter"),
                    'created_by': self.env.user.name,
                    'email': self.env.user.email,
                    'state_ot': "progreso",
                    'bill': self.factura,
                    'Orden_de_Compra': '-----',
                    'ot_progress': 0.00,
                    'ot_begin': datetime.now(),
                    'client_name': self.client_name.id,

                }
                self.env["db.ots"].create(ot_values)

                for i in numeros:
                    url_w = "https://graph.facebook.com/v15.0/114965038179176/messages"
                    Headers = {"content-Type": "application/json",
                               "Authorization": "Bearer EAAHbZBXr5vnEBAJqb9MNLSTBZAFDZBQR8jjWjwlAYnwRxFslr8Ww5StYuOEbpnaRtpLBXcyUfWwCTF4cEEgFnEz4hs0RuAREhrMxgKzXHK7GOCwCZCnSaGo6qM1aLxzsh5L2jz9OMirMXvTIyPhuMbEfnQu3eM4ygW3zfFz4ASM6Hk11ZB7Lt"}
                    data = {"messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": f"{i}",
                            "type": "text",
                            "text": {
                                "preview_url": False,
                                "body": f"""Orden de Trabajo Creada\n solicitud:{self.sol_number} \n cliente:{self.client_name.client} \n fecha de Generacion:{self.fecha_incio}"""
                            }
                            }
                    response = requests.post(url=url_w, headers=Headers, json=data)
                # id_ot = self.env["db.ots"].search([("sol_number", "=", self.sol_number)])
                # template_mail_id = self.env.ref("modulo_operaciones.ot_mail_template").id
                # template = self.env["mail.template"].browse(template_mail_id)
                # template.send_mail(id_ot.id, True)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'Orden de Trabajo Generada Correctamente ',
                        'type': 'success',
                        'sticky': True,
                    }
                }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'Usuario No Autorizado para Realizar esta Acción',
                    'type': 'danger',
                    'sticky': True,
                }
            }

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, "%s %s" % (field.sol_number, field.client_name.client)))
        return res

    @api.onchange("trabajo")
    def onchange_trabajo(self):
        option = self.trabajo
        if option == "VG":
            raise ValidationError(_("El equipo no debe ser manipulado ni desinstalado"))

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ["|", ("sol_number", operator, name), ("client_name.client", operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    @api.onchange('email_client')
    def validate_mail(self):
        if self.email_client:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_client)
            if match == None:
                raise ValidationError('Correo No Valido porfavor corregir')

    def get_area(self, selection):
        diccionario_area = {'ta': 'Taller', 've': 'Ventas', 'com': 'Compras'}
        return diccionario_area[selection]

    def get_type_of_problem(self, selection):
        diccionario_problem = {"RD": "Revisión y Diagnostico (Pagado)",
                               "MR": "Mantenimiento de Rutina (Pagado)",
                               "G": "Garantia",
                               "ARI": "Arranque Inicial",
                               "VD": "Visita por Diagnostico",
                               "VG": "Visita por Garantia",
                               "MS": "Mantenimiento en Sitio",
                               "PG":"Posible Garantia"}

        return diccionario_problem[selection]

    def download_pdf(self):
        return self.env.ref("modulo_solicitudes.sol_template_PDF").report_action(self.id)

    # def send_mail_temp(self):
    #     template_mail_id = self.env.ref("modulo_solicitudes.sol_mail_template").id
    #     template = self.env["mail.template"].browse(template_mail_id)
    #     template.send_mail(self.id, True)
