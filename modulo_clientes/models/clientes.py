from copy import copy
from datetime import datetime
from email.policy import default
from pyexpat import model
import string
from xml.dom import ValidationErr
from odoo import api, models, fields


class clientes(models.Model):
    _name = "clientes.inducom"
    _description = "database for new clients"
    _rec_name = "client"

    cod_client = fields.Char(string="Codigo", required=True)
    client = fields.Char(string="nombre", required=True)
    client_type = fields.Selection([
        ('empresa', 'Empresa'),
        ("persona", "Persona")
    ], string='Tipo de Cliente')
    vendor = fields.Char(string="Vendedor", required=True)
    vendor_email = fields.Char(string="email")
    contact = fields.Char(string="contacto", required=True)

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, "%s %s" % (field.cod_client, field.client)))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ["|", ("cod_client", operator, name), ("client", operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
