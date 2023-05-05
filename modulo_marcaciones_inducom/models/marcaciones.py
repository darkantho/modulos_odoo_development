from copy import copy
from datetime import datetime, date, timedelta
from email.policy import default
from pyexpat import model
import string
from xml.dom import ValidationErr
from odoo import api, models, fields
from odoo import _
import base64


class marcaciones(models.Model):
    _name = "marcaciones.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "marcaciones para inducom"
    _rec_name = "type_tag"

    name = fields.Char(string="nombre", required=True, default=lambda self: self.env.user.name,readonly=True)
    email = fields.Char(string="Correo", required=True, default=lambda self: self.env.user.email,readonly=True)
    date_hour_tag = fields.Datetime(string="Fecha y hora",readonly=True,required=True,store=True,default=lambda self: datetime.today())
    type_tag = fields.Selection([
        ("entrada", "Entrada"),
        ("salidaal", "Salida Almuerzo"),
        ("entradaal", "Entrada Almuerzo"),
        ("salida", "Salida"),
        ("atrasoen","Entrada Atrasada"),
        ("rango","fuera de rango laboral")
    ], string="motivo", required=True, readonly=True, compute="autofill_tag", store=True)

    @api.depends("date_hour_tag")
    def autofill_tag(self):
        marcacion=datetime.today()-timedelta(hours=+5)
        mar_ent_ini=marcacion.replace(hour=6, minute=30, second=0, microsecond=0)
        mar_ent_fin=marcacion.replace(hour=8, minute=30, second=0, microsecond=0)
        mar_salidaal_ini =marcacion.replace(hour=12, minute=0, second=0, microsecond=0)
        mar_salidaal_fin =marcacion.replace(hour=14, minute=0, second=0, microsecond=0)
        mar_entradaal_ini = marcacion.replace(hour=15, minute=30, second=0, microsecond=0)
        mar_entradaal_fin = marcacion.replace(hour=16, minute=30, second=0, microsecond=0)
        mar_salida_ini = marcacion.replace(hour=18, minute=0, second=0, microsecond=0)
        mar_salida_fin = marcacion.replace(hour=19, minute=0, second=0, microsecond=0)
        mar_salida_ini_fds = marcacion.replace(hour=13, minute=0, second=0, microsecond=0)
        mar_salida_fin_fds = marcacion.replace(hour=13, minute=30, second=0, microsecond=0)
        print(marcacion)
        weekday_list=["Lunes", "Martes", "Miercoles", "jueves", "Viernes", "Sabado", "Domingo"]
        if(weekday_list[marcacion.weekday()]!="Sabado" and mar_ent_ini<marcacion<mar_ent_fin):
            self.type_tag="entrada"
            print("entrada")
        elif(weekday_list[marcacion.weekday()]!="Sabado" and mar_ent_fin<marcacion<mar_salidaal_ini):
            self.type_tag="atrasoen"
            print("atraso")
        elif (weekday_list[marcacion.weekday()]!="Sabado" and mar_salidaal_ini < marcacion < mar_salidaal_fin):
            self.type_tag = "salidaal"
            print("salida almuerzo")
        elif (weekday_list[marcacion.weekday()]!="Sabado" and mar_entradaal_ini < marcacion < mar_entradaal_fin):
            self.type_tag = "entradaal"
            print("entrada almerzo")
        elif (weekday_list[marcacion.weekday()]!="Sabado" and mar_salida_ini < marcacion < mar_salida_fin):
            self.type_tag = "salida"
            print("salida")
        elif (weekday_list[marcacion.weekday()]=="Sabado" and mar_ent_ini < marcacion < mar_ent_fin):
            self.type_tag = "entrada"
            print("entrada finde")
        elif (weekday_list[marcacion.weekday()]=="Sabado" and mar_salida_ini_fds < marcacion < mar_salida_fin_fds):
            self.type_tag = "salida"
            print("salida finde")
        else:
            self.type_tag = "rango"
            print("fuera rango")
        print(self.type_tag)

    def send_email_notification(self):
        template_mail_id = self.env.ref("modulo_marcaciones_inducom.marcaciones_mail_template").id
        template = self.env["mail.template"].browse(template_mail_id)
        template.send_mail(self.ids[0], True)

    def _get_date(self):
        return self.date_hour_tag-timedelta(hours=+5)

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, "%s %s" % (field.date_hour_tag-timedelta(hours=+5), field.name)))
        return res

    def _get_values_tags(self):
        if self.type_tag=="entrada":
            return "entrada"
        if self.type_tag=="salidaal":
            return "Salida del Almuerzo"
        if self.type_tag=="entradaal":
            return "entrada del Almuerzo"
        if self.type_tag=="salida":
            return "Salida"
        if self.type_tag=="rango":
            return "Fuera de rango"
        if self.type_tag=="atrasoen":
            return "entrada atrasada"