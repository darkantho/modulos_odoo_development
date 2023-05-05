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


class rics(models.Model):
    _name = "rics.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Rics para el personal inducom"
    # _rec_name = "ot_number"
    # _order = 'ot_number desc'

    ric_number = fields.Char(string="Ric N°", readonly=True, default=lambda self: _("Nuevo Ric"))
    sol_attachment = fields.Many2one("solicitudes.inducom", string="solicitud adjunta")
    sol_attachment_selection = fields.Selection([("sol", "Solicitud"),
                                                 ("ot", "OT"),
                                                 ("ric", "Ric Normal")], string="Ric adjunto a ?", default='ric',
                                                tracking=True)
    description = fields.Text(string="Detalle del Ric", required=True, tracking=True)
    area = fields.Selection([("ad", "Administrativo"),
                             ("ta", "Taller"),
                             ("rh", "Recursos Humanos"),
                             ("ve", "Ventas")], string="Area Solicitante", required=True, tracking=True)
    ric_complete = fields.Boolean(string="Ric Completado?", default=False, tracking=True)
    date_sol_begin = fields.Datetime(string="Fecha de Generación", readonly=True, tracking=True)
    date_ric_end = fields.Datetime(string="Fecha de entrega para el dia", tracking=True, required=True)
    date_sol_end = fields.Datetime(string="Ric completado/entregado", readonly=True, tracking=True)
    client = fields.Many2one("clientes.inducom", string="Cliente", tracking=True)
    ot_attachment = fields.Many2one("db.ots", string="orden de trabajo", tracking=True)
    codigo_adjunto = fields.Char(string="Adjunto")
    created_by = fields.Char(string="Elaborado Por", required=True, default=lambda self: self.env.user.name)
    email = fields.Char(string="Correo", required=True, default=lambda self: self.env.user.email)
    list_of_materials = fields.One2many("listado.ric.inducom", "order_id", string="Lista de requerimientos")
    state_of_ric = fields.Selection([("NC", "No Completado"),
                                     ("C", "Completado")], string="estado", default="NC", readonly=True)


    @api.model
    def create(self, vals):
        if vals.get("ric_number", _("Nuevo Ric")) == _("Nuevo Ric"):
            vals["ric_number"] = self.env['ir.sequence'].next_by_code("RIC_counter") or "/"
        vals["date_sol_begin"] = datetime.now()

        if vals["sol_attachment"] > 0 and vals["client"] == False and vals["ot_attachment"] == False:
            vals["codigo_adjunto"] = self.env["solicitudes.inducom"].search([('id', '=', vals["sol_attachment"])]).sol_number

        elif vals["sol_attachment"] == False and vals["client"] > 0  and vals["ot_attachment"] == False:
            vals["codigo_adjunto"] = self.env["clientes.inducom"].search([('id', '=', vals["client"])]).cod_client

        else:
            vals["codigo_adjunto"] = self.env["db.ots"].search([('id', '=', vals["ot_attachment"])]).ot_number

        res = super(rics, self).create(vals)

        report_template_id = self.env.ref("modulo_rics.RIC_template_PDF")._render_qweb_pdf(res.id)
        data_record = base64.b64encode(report_template_id[0])
        ir_values = {
            'name': "%s.pdf" % res.ric_number,
            'type': 'binary',
            'datas': data_record,
            'store_fname': res.ric_number,
            'mimetype': 'application/x-pdf'
        }
        data_id = self.env["ir.attachment"].create(ir_values)
        template_mail_id = self.env.ref("modulo_rics.ric_mail_template").id
        template = self.env["mail.template"].browse(template_mail_id)
        template.attachment_ids = [(6, 0, [data_id.id])]
        template.send_mail(res.id, True)
        template.attachment_ids = [(3, data_id.id)]

        return res



    def action_download_ric(self):
        return self.env.ref("modulo_rics.RIC_template_PDF").report_action(self.id)

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, "%s %s" % (field.ric_number, field.created_by)))
        return res

    @api.onchange("ric_complete")
    def onchange_state_ric(self):
        if self.ric_complete and not self.date_sol_end:
            self.state_of_ric = "C"
            self.date_sol_end = datetime.now()


class product_list(models.Model):
    _name = "listado.ric.inducom"
    _description = "modelo para indexar los materiales de los rics"

    cantidad = fields.Float(string="Cantidad", default=0.0)
    descripcion = fields.Char(string="descripcion")
    observacion = fields.Char(string="Observacion")
    order_id = fields.Many2one("rics.inducom", string="listado")
