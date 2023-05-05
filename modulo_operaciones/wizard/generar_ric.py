from odoo import api, fields, models, _
from datetime import date
import base64


def date_gen():
    return date.today()


class generarRICwizard(models.TransientModel):
    _name = "ric.inducom.wizard"
    _description = "modelo para generar el Ric"

    ric_number = fields.Char(string="RIC", index=True, readonly=True, default=lambda self: _("Nuevo RIC"))
    orden = fields.Many2one("db.ots", string="Orden de trabajo")
    cliente = fields.Char(string="Cliente", related="orden.client_name.client", required=True)
    fecha1 = fields.Date(string="Fecha de Solicitud", required=True, default=date.today(), readonly=True)
    solicitante = fields.Char(string="Solicitante", required=True, default=lambda self: self.env.user.name)
    fecha2 = fields.Date(string="Fecha de Entrega", required=True)
    area = fields.Selection([
        ("mec", "Area Mecanica"),
        ("elec", "Area Electrica"),
        ("tec", "Servicio Tecnico"),
        ("pro", "Proyectos"),
    ], string="Area", required=True)
    materiales = fields.One2many("materiales.ric.inducom.wizard", "order_id", string="Lista de Requerimientos")

    def get_ot_number(self):
        return self.orden.ot_number

    def action_send_ot(self):
        print("sending email")
        report_template_id = self.env.ref("modulo_operaciones.RIC_template_PDF")._render_qweb_pdf(self.ids)
        data_record = base64.b64encode(report_template_id[0])
        ir_values = {
            'name': "%s-%s-%s.pdf" % (self.ric_number, self.get_ot_number(), self.cliente),
            'type': 'binary',
            'datas': data_record,
            'store_fname': "RIC"+self.cliente,
            'mimetype': 'application/x-pdf'
        }
        data_id = self.env["ir.attachment"].create(ir_values)
        template_mail_id = self.env.ref("modulo_operaciones.RIC_mail_template").id
        template = self.env["mail.template"].browse(template_mail_id)
        template.attachment_ids = [(6, 0, [data_id.id])]
        template.send_mail(self.ids[0], True)
        template.attachment_ids = [(3, data_id.id)]

    @api.model
    def create(self, vals):
        if vals.get("ric_number", _("Nuevo RIC")) == _("Nuevo RIC"):
            vals["ric_number"] = self.env['ir.sequence'].next_by_code("ric_counter") or "/"
        res = super(generarRICwizard, self).create(vals)
        return res

    def action_download(self):
        return self.env.ref("modulo_operaciones.RIC_template_PDF").report_action(self.id)



class product_index_wizard(models.TransientModel):
    _name = "materiales.ric.inducom.wizard"
    _description = "modelo para indexar los materiales de los requerimientos"

    cantidad = fields.Float(string="Cantidad", default=0)
    descripcion = fields.Char(string="Descripcion")
    observacion = fields.Char(string="Observacion")
    order_id = fields.Many2one("ric.inducom.wizard", string="lista")




