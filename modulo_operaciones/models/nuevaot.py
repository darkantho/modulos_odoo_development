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
    _name = "db.ots"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "database for new OT"
    _rec_name = "ot_number"
    _order = 'ot_number desc'

    # funciones por defecto en campos
    @api.model
    def default_mails(self):
        return self.env['personal.inducom'].search([('COD_IND', 'in', ['B0001',
                                                                       'B0003',
                                                                       'B0004',
                                                                       'B0005',
                                                                       'B0006',
                                                                       'B0007',
                                                                       'B0008',
                                                                       'B0009'])]).ids

    #######################################################################################################
    #                                   Campos del modulo operaciones                                     #
    #                                                                                                     #
    #######################################################################################################
    sol_number = fields.Char(string="Solicitud Nº", readonly=True)
    ot_number = fields.Char(string="OT", index=True, readonly=True, default=lambda self: _("Nueva orden de trabajo"))
    created_by = fields.Char(string="Elaborado Por", required=True, default=lambda self: self.env.user.name)
    email = fields.Char(string="Correo", required=True, default=lambda self: self.env.user.email)
    to = fields.Many2many("personal.inducom", "name", "email", "area", string="Responsables", default=default_mails)
    bill = fields.Char(string="Factura/Cotizacion", required=True)
    Orden_de_Compra = fields.Char(string="Orden de Compra", required=True)
    area = fields.Selection([
        ("bodega", "Bodega km 4.5"),
        ("taller", "Taller km 10.5"),
        ("externo","Externo")
    ], string="Area designada", tracking=True)

    state_ot = fields.Selection([
        ("cancelada", "Orden Anulada"),
        ("progreso", "Orden en Progreso"),
        ("revision", "Orden en Revision"),
        ("finalizada", "Orden Finalizada a Tiempo"),
        ("finalizada2", "Orden Finalizada fuera del plazo"),
        ("vencida", "Orden no completada")
    ], string="Estado de la OT", required=True, default="progreso", store=True, tracking=True)

    work_type = fields.Selection([
        ("armado", "Armado"),
        ("prueba", "Prueba de arranque"),
        ("visita", "visita Tecnica"),
        ("sci", "Sistema contra incendio"),
        ("cbc", "conjunto de bombeo completo"),
        ("otro", "otro")
    ], string="Servicio Requerido")

    type_work = fields.Selection([
        ("ens", "Ensamble"),
        ("serv", "Servicio Tecnico"),
        ("man", "Mantenimiento"),
    ], string="Tipo de Trabajo en Taller", tracking=True, readonly=True)

    ot_other_service = fields.Char(string="Otro Tipo de Servicio", default="", tracking=True)
    ot_progress = fields.Float(string="Estado Actual(%)", tracking=True)
    ot_progress_opt = fields.Float(string="Estado optimo(%)", default="0")
    ot_progress_cat = fields.Selection([
        ("1", "entre 0% del 24%"),
        ("2", "entre 25% y 49%"),
        ("3", "entre 50% y 74% "),
        ("4", "entre 75% y 100%"),
    ], string="Estado actual", default="1")
    ot_begin = fields.Datetime(string="Fecha inicio", store=True, readonly=True, default=date.today())
    ot_end = fields.Datetime(string="Fecha fin", store=True, tracking=True)
    ot_end_2 = fields.Datetime(string="OT entregada", readonly=True, trackin=True)
    datediff = fields.Integer(string="Duracion", compute="difference_date", store=True)
    bom_ids = fields.One2many("materiales.inducom", "order_id", string="Lista de material")
    other_requeriments = fields.Text(string="Descripcion del trabajo")
    cancelacion = fields.Text(string="Motivo de Cancelacion")
    # campos del cliente
    client_name = fields.Many2one("clientes.inducom", string="Cliente")
    id_client = fields.Char(string="Codigo Cliente", related="client_name.cod_client")
    client_type = fields.Selection(string="Tipo", related="client_name.client_type")
    vendor_name = fields.Char(string="Vendedor", related="client_name.vendor")
    vendor_email = fields.Char(string="Correo Vendedor", related="client_name.vendor_email")
    # campo de documentos
    adjunto_1 = fields.Binary(string="Nota de pedidos", attachment=True)
    adjunto_2 = fields.Binary(string="Aprobacion", attachment=True)
    adjunto_3 = fields.Binary(string="Cotizacion", attachment=True)
    adjunto_4 = fields.Binary(string="Orden de compra", attachment=True)
    adjunto_5 = fields.Binary(string="Otra Documentación", attachment=True)
    # campo de imagenes
    imagen_1 = fields.Binary(string="Foto Inicio ensamble", attachment=True)
    imagen_2 = fields.Binary(string="Foto Avance ensamble 1", attachment=True)
    imagen_3 = fields.Binary(string="Foto Avance ensamble 2", attachment=True)
    imagen_4 = fields.Binary(string="Foto Avance ensamble 3", attachment=True)
    imagen_5 = fields.Binary(string="Foto Final del ensamble", attachment=True)
    active = fields.Boolean(string="Active", default=True)

    #######################################################################################################
    #                                   Funciones del modulo operaciones                                  #
    #                                                                                                     #
    #######################################################################################################
    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, "%s %s" % (field.ot_number, field.client_name.client )))
        return res

    def get_client_name(self):
        return self.client_name.client

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ["|", ("ot_number", operator, name), ("client_name.client", operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    def get_status_ot(self, valor):
        if valor == "cancelada":
            return " Orden Anulada"
        elif valor == "progreso":
            return " Orden en Progreso"
        elif valor == "revision":
            return "Orden en Revision"
        elif valor == "finalizada":
            return "Orden Finalizada a Tiempo"
        elif valor == "finalizada2":
            return "Orden Finalizada Fuera del Plazo"
        else:
            return "Orden no Completada"

    @api.model
    def create(self, vals):
        if vals.get("ot_number", _("Nueva orden de trabajo")) == _("Nueva orden de trabajo"):
            vals["ot_number"] = self.env['ir.sequence'].next_by_code("ot_counter") or "/"
        res = super(dbots, self).create(vals)
        return res

    @api.depends("ot_begin", "ot_end")
    def difference_date(self):
        d1 = self.ot_begin
        d2 = self.ot_end
        if d1 and d2:
            if d2 > d1:
                self.datediff = (d2 - d1).days
            else:
                raise ValueError("la fecha de inicio debe ser menor que la fecha de finalizacion")

    @api.onchange("work_type")
    def onchange_work_type(self):
        option = self.work_type
        if option == "prueba":
            self.ot_end = datetime.now() + timedelta(days=10)
            self.bom_ids = [(5, 0, 0)]
        elif option == "sci":
            self.ot_end = datetime.now() + timedelta(days=20)
            self.bom_ids = [(5, 0, 0)]
            # lines = []
            # vals = {
            #     'material_id': self.env["productos.inducom"].search([("product_id", "=", "C0001")]),
            #     'cantidad': 1,
            #     'estado': 'verificacion',
            # }
            # lines.append((0, 0, vals))
            #
            # vals = {
            #     'material_id': self.env["productos.inducom"].search([("product_id", "=", "C0004")]),
            #     'cantidad': 1,
            #     'estado': 'verificacion',
            # }
            # lines.append((0, 0, vals))
            #
            # vals = {
            #     'material_id': self.env["productos.inducom"].search([("product_id", "=", "C0005")]),
            #     'cantidad': 1,
            #     'estado': 'verificacion',
            # }
            # lines.append((0, 0, vals))
            #
            # self.bom_ids = lines
        elif option == "visita":
            self.ot_end = datetime.now() + timedelta(days=2)
            self.bom_ids = [(5, 0, 0)]
        elif option == "armado":
            self.ot_end = datetime.now() + timedelta(days=15)
            self.bom_ids = [(5, 0, 0)]
            # lines = []
            # vals = {
            #     'material_id': self.env["productos.inducom"].search([("product_id", "=", "C0001")]),
            #     'cantidad': 1,
            #     'estado': 'verificacion',
            # }
            # lines.append((0, 0, vals))
            #
            # vals = {
            #     'material_id': self.env["productos.inducom"].search([("product_id", "=", "C0005")]),
            #     'cantidad': 1,
            #     'estado': 'verificacion',
            # }
            # lines.append((0, 0, vals))
            #
            # self.bom_ids = lines

    @api.onchange("bom_ids")
    def onchange_bom(self):
        lista_codigos = self.bom_ids.mapped("material_id.product_id")
        # lista_productos = self.bom_ids.mapped("material_id.product_name")
        lista_estados = self.bom_ids.mapped("estado")
        total_avance = 0
        avance = 0
        if len(lista_codigos) != 0:
            avance = 100 / len(lista_codigos)
            for record in range(len(lista_codigos)):
                if lista_estados[record] == "disponible" or lista_estados[record] == "Compra2":
                    total_avance += 1

        else:
            total_avance = 0
        self.ot_progress = round(avance * total_avance, 2)

    def action_send_ot(self):
        print("sending email")
        report_template_id = self.env.ref("modulo_operaciones.ot_order_template")._render_qweb_pdf(self.ids)
        data_record = base64.b64encode(report_template_id[0])
        ir_values = {
            'name': "%s.pdf" % self.ot_number,
            'type': 'binary',
            'datas': data_record,
            'store_fname': self.ot_number,
            'mimetype': 'application/x-pdf'
        }
        data_id = self.env["ir.attachment"].create(ir_values)
        template_mail_id = self.env.ref("modulo_operaciones.ot_mail_template").id
        template = self.env["mail.template"].browse(template_mail_id)
        template.attachment_ids = [(6, 0, [data_id.id])]
        template.send_mail(self.ids[0], True)
        template.attachment_ids = [(3, data_id.id)]
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Notificacion Enviada Correctamente',
                'type': 'success',
                'sticky': True,
            }
        }

    @api.onchange("state_ot")
    def send_status_changed(self):
        valor = self.state_ot
        valor2 = self.get_status_ot(valor)
        if self.ot_number != "Nueva orden de trabajo":
            mail_values = {
                'subject': 'Cambio del estado de la orden No %s' % self.ot_number,
                'body_html': 'La orden de trabajo asignada a %s ha cambiado de estado a : %s' % (self.area,
                                                                                                 valor2),
                'email_to': self._get_email_to(),
                'email_from': 'botinducom@gmail.com'
            }
            self.env["mail.mail"].create(mail_values).send(True)
            self.state_ot = valor

    def _get_email_to(self):
        correos = self.to.mapped("email")
        correos2 = ",".join(correos)
        correos_vendedor = self.vendor_email if type(self.vendor_email) == str else ""
        email_recipes = correos2 + "," + correos_vendedor
        return email_recipes

    def ot_end_button(self):
        hoy = datetime.now()

        check_5_images = not (self.imagen_1 == False or
                         self.imagen_2 == False or
                         self.imagen_3 == False or
                         self.imagen_4 == False or
                         self.imagen_5 == False)


        if self.ot_progress == 100:
            self.ot_progress_cat = "4"

            if hoy > self.ot_end and self.env.user.name in permisos:
                self.state_ot = "finalizada2"
                self.ot_end_2 = datetime.now()
                mail_values = {
                    'subject': 'Cambio del estado de la orden No %s' % self.ot_number,
                    'body_html': 'La orden de trabajo asignada a %s ha cambiado de estado a : %s' % (self.area,
                                                                                                     self.get_status_ot(
                                                                                                         self.state_ot)),
                    'email_to': self._get_email_to(),
                    'email_from': 'botinducom@gmail.com'
                }
                self.env["mail.mail"].create(mail_values).send(True)
            elif hoy <= self.ot_end and self.env.user.name in permisos:
                self.state_ot = "finalizada"
                self.ot_end_2 = datetime.now()
                mail_values = {
                    'subject': 'Cambio del estado de la orden No %s' % self.ot_number,
                    'body_html': 'La orden de trabajo asignada a %s ha cambiado de estado a : %s' % (self.area,
                                                                                                     self.get_status_ot(
                                                                                                         self.state_ot)),
                    'email_to': self._get_email_to(),
                    'email_from': 'botinducom@gmail.com'
                }
                self.env["mail.mail"].create(mail_values).send(True)
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'Usuario no autorizado o no registro las imagenes correctamente',
                        'type': 'danger',
                        'sticky': True,
                    }
                }


    def directorio_inducom(self):

        directorio = ['direccion1@inducom-ec.com',
                      'serviciocliente@inducom-ec.com',
                      'gcordova@inducom-ec.com',
                      'ventas1@inducom-ec.com',
                      'acompras@inducom-ec.com']

        return ",".join(directorio)

    def count_ot_progress_per_day(self, day):
        fecha_1 = date.today()
        fecha_2 = date.today() - timedelta(days=day)
        orders_P = self.env["db.ots"].search_count([('state_ot', '=', 'progreso'),
                                                    ('ot_begin', '<=', fecha_1),
                                                    ('ot_begin', '>=', fecha_2)])

        return f"Total de ordenes en progreso:{orders_P}"

    def count_ot_vencidas_per_day(self, day):
        fecha_1 = date.today()
        fecha_2 = date.today() - timedelta(days=day)

        orders_NC = self.env["db.ots"].search_count([('state_ot', '=', 'vencida'),
                                                     ('ot_begin', '<=', fecha_1),
                                                     ('ot_begin', '>=', fecha_2)])
        return f"Total de ordenes no completadas:{orders_NC}"

    def count_ot_final_per_day(self, day):
        fecha_1 = date.today()
        fecha_2 = date.today() - timedelta(days=day)
        orders_F = self.env["db.ots"].search_count([('state_ot', '=', 'finalizada'),
                                                    ('ot_begin', '<=', fecha_1),
                                                    ('ot_begin', '>=', fecha_2)])

        return f"Total de ordenes Finalizadas:{orders_F}"

    def count_ot_final2_per_day(self, day):
        fecha_1 = date.today()
        fecha_2 = date.today() - timedelta(days=day)
        orders_FFP = self.env["db.ots"].search_count([('state_ot', '=', 'finalizada2'),
                                                      ('ot_begin', '<=', fecha_1),
                                                      ('ot_begin', '>=', fecha_2)])
        return f"Total de ordenes Finalizadas Fuera del plazo:{orders_FFP}"

    def ensamble(self):
        print(self.env.user.name)
        if self.env.user.name in permisos:
            self.type_work = "ens"

    def mantenimiento(self):
        if self.env.user.name in permisos:
            self.type_work = "man"

    def postventa(self):
        if self.env.user.name in permisos:
            self.type_work = "serv"

    def report_excel(self):

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Resume_ordenes")

        bold = workbook.add_format({'bold': True,
                                    'align': 'center'})
        row = 0
        col = 0

        worksheet.write(row, col, "OT", bold)
        worksheet.write(row, col + 1, "Cliente", bold)
        worksheet.write(row, col + 2, "%", bold)
        worksheet.write(row, col + 3, "inicio", bold)
        worksheet.write(row, col + 4, "fin", bold)
        worksheet.write(row, col + 5, "Estado", bold)
        worksheet.write(row, col + 6, "vendedor", bold)
        worksheet.write(row, col + 7, "descripcion", bold)

        for rec in self:
            print(rec.client_name.client)
            row += 1
            worksheet.write(row, col, rec.ot_number)
            worksheet.write(row, col + 1, rec.client_name.client)
            worksheet.write(row, col + 2, rec.ot_progress)
            worksheet.write(row, col + 3, rec.ot_begin)
            worksheet.write(row, col + 4, rec.ot_end)
            worksheet.write(row, col + 5, self.get_status_ot(rec.state_ot))
            worksheet.write(row, col + 6, rec.client_name.vendor)
            worksheet.write(row, col + 7, rec.other_requeriments)

        workbook.close()

        data_record = base64.b64encode(output.getvalue())

        ir_values = {
            'name': 'resume_seleccionado_%s.xlsx' % date.today(),
            'type': 'binary',
            'datas': data_record,
            'store_fname': 'resume_seleccionado.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        data_id = self.env["ir.attachment"].create(ir_values)
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        download_url = '/web/content/' + str(data_id.id) + '?download=true'

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }




    #######################################################################################################
    #                                   Funciones que se ejecutan en el servidor                          #
    #                                                                                                     #
    #######################################################################################################

    # def generate_mail_orders(self):
    #
    #     orders_P = self.env["db.ots"].search_count([('state_ot', '=', 'progreso')])
    #     orders_NC = self.env["db.ots"].search_count([('state_ot', '=', 'vencida')])
    #     orders_F = self.env["db.ots"].search_count([('state_ot', '=', 'finalizada')])
    #     orders_FFP = self.env["db.ots"].search_count([('state_ot', '=', 'finalizada2')])
    #
    #     texto_mensaje = f"""
    #                         Total de ordenes en progreso:{orders_P} <br>
    #                         Total de ordenes Finalizadas:{orders_F} <br>
    #                         Total de ordenes Finalizadas Fuera del plazo:{orders_FFP} <br>
    #                         Total de ordenes no completadas:{orders_NC} <br>
    #
    #     """
    #     mail_values = {
    #         'subject': 'Estado diario de las OT',
    #         'body_html': texto_mensaje,
    #         'email_to': 'anthony1320081@gmail.com',
    #         'email_from': 'botinducom@gmail.com'
    #     }
    #     # directorio = ['direccion1@inducom-ec.com',
    #     #               'serviciocliente@inducom-ec.com',
    #     #               'gcordova@inducom-ec.com',
    #     #               'ventas1@inducom-ec.com',
    #     #               'acompras@inducom-ec.com']
    #     # mail_values = {
    #     #     'subject': 'ordenes de trabajo activas',
    #     #     'body_html': texto_mensaje,
    #     #     'email_to': ",".join(directorio),
    #     #     'email_from': 'botinducom@gmail.com'
    #     # }
    #     self.env["mail.mail"].create(mail_values).send()

    def update_status_orders_server(self):
        orders = self.env["db.ots"].search([])
        fecha_hoy = date.today()
        for order in orders:
            dias_transcurridos = (fecha_hoy - order.ot_begin).days
            dias_totales = order.datediff
            # print(order.ot_number, dias_transcurridos, dias_totales)
            if dias_transcurridos == 0:
                order.ot_progress_opt = 0
                order.ot_progress_cat = "1"
            elif dias_transcurridos == dias_totales:
                order.ot_progress_opt = 100
                order.ot_progress_cat = "4"
            else:
                calculo_progreso = (100 / dias_totales) * dias_transcurridos
                order.ot_progress_opt = 100 if calculo_progreso >= 100 else calculo_progreso
                if 0 <= calculo_progreso < 25:
                    order.ot_progress_cat = "1"
                elif 25 <= calculo_progreso < 50:
                    order.ot_progress_cat = "2"
                elif 50 <= calculo_progreso < 75:
                    order.ot_progress_cat = "3"
                else:
                    order.ot_progress_cat = "4"

    def change_status_orders_server(self):
        orders = self.env["db.ots"].search([('state_ot', '=', 'progreso')])
        day_com = date.today()
        contador = 0
        for order in orders:
            if day_com > order.ot_end:
                contador += 1
                order.state_ot = "vencida"

        directorio = ['direccion1@inducom-ec.com',
                      'serviciocliente@inducom-ec.com',
                      'gcordova@inducom-ec.com',
                      'ventas1@inducom-ec.com',
                      'acompras@inducom-ec.com']

        # mail_values = {
        #     'subject': 'Vencimiento de Ordenes de Trabajo ',
        #     'body_html': 'tiene %s ordenes que no cumplieron el intervalo planificado de finalización ' % contador,
        #     'email_to': ','.join(directorio),
        #     'email_from': 'botinducom@gmail.com'
        # }

        mail_values = {
            'subject': 'Vencimiento de Ordenes de Trabajo ',
            'body_html': 'tiene %s ordenes que no cumplieron el intervalo planificado de finalización ' % contador,
            'email_to': 'anthony1320081@gmail.com',
            'email_from': 'botinducom@gmail.com'
        }
        self.env["mail.mail"].create(mail_values).send()

    def report_resume_daily_xlsx(self):
        fecha_1 = date.today()
        fecha_2 = date.today() - timedelta(days=2)
        ordenes = self.env["db.ots"].search([('ot_begin', '<=', fecha_1),
                                             ('ot_begin', '>=', fecha_2)])

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("ordenes")

        bold = workbook.add_format({'bold': True,
                                    'align': 'center'})
        alertas = {
            "progreso": workbook.add_format({'bold': False, 'align': 'center'}),
            "vencida": workbook.add_format({'bg_color': 'red', 'align': 'center'}),
            "finalizada": workbook.add_format({'bg_color': 'green', 'align': 'center'}),
            "finalizada2": workbook.add_format({'bg_color': 'silver', 'align': 'center'})
        }
        row = 0
        col = 0

        worksheet.write(row, col, "Orden Nº", bold)
        worksheet.write(row, col + 1, "Cliente", bold)
        worksheet.write(row, col + 2, "Factura/Cotizacion", bold)
        worksheet.write(row, col + 3, "Orden de Compra", bold)
        worksheet.write(row, col + 4, "Area", bold)
        worksheet.write(row, col + 5, "Estado", bold)
        worksheet.write(row, col + 6, "Servicio", bold)
        worksheet.write(row, col + 7, "Progreso", bold)
        worksheet.write(row, col + 8, "Fecha Inicio", bold)
        worksheet.write(row, col + 9, "Fecha Fin", bold)
        worksheet.write(row, col + 10, "Dias", bold)

        for orden in ordenes:
            row += 1
            worksheet.write(row, col, orden.ot_number, alertas[orden.state_ot])
            worksheet.write(row, col + 1, orden.client_name.client, alertas[orden.state_ot])
            worksheet.write(row, col + 2, orden.bill, alertas[orden.state_ot])
            worksheet.write(row, col + 3, orden.Orden_de_Compra, alertas[orden.state_ot])
            worksheet.write(row, col + 4, orden.area, alertas[orden.state_ot])
            worksheet.write(row, col + 5, self.get_status_ot(orden.state_ot), alertas[orden.state_ot])
            worksheet.write(row, col + 6, orden.ot_other_service, alertas[orden.state_ot])
            worksheet.write(row, col + 7, orden.ot_progress, alertas[orden.state_ot])
            worksheet.write(row, col + 8, orden.ot_begin, alertas[orden.state_ot])
            worksheet.write(row, col + 9, orden.ot_end, alertas[orden.state_ot])
            worksheet.write(row, col + 10, orden.datediff, alertas[orden.state_ot])

        workbook.close()

        data_record = base64.b64encode(output.getvalue())

        ir_values = {
            'name': 'resume_diario_%s.xlsx' % date.today(),
            'type': 'binary',
            'datas': data_record,
            'store_fname': 'resume_diario.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        data_id = self.env["ir.attachment"].create(ir_values)
        template_mail_id = self.env.ref("modulo_operaciones.ot_resume_daily").id
        template = self.env["mail.template"].browse(template_mail_id)
        template.attachment_ids = [(6, 0, [data_id.id])]
        template.send_mail(self.id, True)
        template.attachment_ids = [(3, data_id.id)]


class product_index(models.Model):
    _name = "materiales.inducom"
    _description = "modelo para indexar los materiales ingresados"

    material_id = fields.Many2one("productos.inducom", string="Item")
    cantidad = fields.Integer(string="Cantidad", default=0)
    estado = fields.Selection([
        ("verificacion", "En verificacion"),
        ("disponible", "disponible"),
        ("compra", "Compra Pendiente"),
        ("Compra2", "Compra realizada")
    ], string="estado", default="verificacion")
    order_id = fields.Many2one("db.ots", string="lista")
