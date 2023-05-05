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

class visitas(models.Model):
    _name = "visitas.inducom"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "registro de visita"
    # _rec_name = "ot_number"
    # _order = 'ot_number desc'

    # funciones por defecto en campos

    #######################################################################################################
    #                                   Campos del modulo operaciones                                     #
    #                                                                                                     #
    #######################################################################################################

    fecha = fields.Datetime(string="Fecha", tracking=True)
    created_by = fields.Char(string="Elaborado Por", required=True, default=lambda self: self.env.user.name)
    email = fields.Char(string="Correo", required=True, default=lambda self: self.env.user.email)
    cliente = fields.Many2one("clientes.inducom",string="Cliente", tracking=True)
    contacto_tipo = fields.Selection([
        ("visita", "Visita"), ("llamada", "Llamada Recibida"),
        ("email", "Email recibido"), ("whatsapp", "Whatsapp"),
        ("acercamiento", "Acercamiento"), ("otros", "Otros")
    ], string="Contacto", tracking=True)
    provincia = fields.Selection([
        ("azuay","Azuay"), ("bolivar","Bolivar"), ("cañar","Cañar"), ("carchi","Carchi"),
        ("chimborazo","Chimborazo"), ("cotopaxi","Cotopaxi"),
        ("oro","El Oro"), ("esmeraldas","Esmeraldas"), ("galapagos","Galapagos"), ("guayas","Guayas"),
        ("imbabura","Imbabura"), ("loja","Loja"),
        ("Rios","Los Rios"), ("manabi","Manabi"), ("moronasantiago","Morona Santiago"), ("napo","Napo"),
        ("orellana","Orellana"), ("pastaza","Pastaza"),
        ("pichincha", "Pichincha"), ("santaelena", "Santa Elena"),
        ("santodomingodelostsachilas", "Santo Domingo de los Tsachilas"),
        ("sucumbios", "Sucumbios"), ("tungurahua", "Tungurahua"), ("zamorahinchipe", "Zamora Chinchipe")
    ], string="Provincia", tracking=True)
    marca = fields.Selection([
        ("ebara","EBARA"), ("hidromac","HIDROMAC"), ("debem","DEBEM"), ("apv","APV"), ("spx","SPX"),
        ("durcomex","DURCOMEX"), ("ruhrpumpen","RUHRPUMPEN"), ("corvex","CORVEX"), ("CRIPUMPS","C.R.I PUMPS"),
        ("warsonpump","WARSON PUMP"),("atlascopco","ATLAS COPCO"), ("trisun","TRISUN"),
        ("yamada","YAMADA"), ("iwakiamerica","IWAKI AMERICA"), ("seepex","SEEPEX"), ("netzsch","NETZSCH"),
        ("vikingpump","VIKING PUMP"), ("gardnedenverr","GARDNER DENVER"), ("giant","GIANT"), ("ligao","LIGAO"),
        ("albinpump","ALBIN PUMP"), ("robuschi","ROBUSCHI"), ("cycloblower","CYCLOBLOWER"),
        ("sutorbilt","SUTORBILT"), ("elmorietschle","ELMO RIETSCHLE"), ("dekker","DEKKER"), ("thompson","THOMPSON"),
        ("schurcoslurry","SCHURCO SLURRY"), ("abb","ABB"), ("baldor","BALDOR"),
        ("lovol","LOVOL"), ("oli","OLI"), ("bonfiglioli","BONFIGLIOLI"), ("dodge","DODGE"),
        ("everlast","EVERLAST"), ("gemotron","GEMOTRON"), ("gpi","GPI"), ("imduelectric","INDUELECTRIC"),
        ("walchem","WALCHEM"), ("donaldson","DONALDSON"),
        ("wam","WAM"), ("compair","COMPAIR"), ("bellissmorcom","BELLISSMORCOM"),
        ("mako","MAKO"), ("champion","CHAMPION"), ("shimge","SHIMGE"),
        ("shaki","SHAKI"), ("roper","ROPER"), ("siemens","SIEMENS"), ("emotron","EMOTRON"),
        ("weg","WEG"), ("sydex","SYDEX"), ("ihm","IHM"), ("weima","WEIMA"),
        ("varios","VARIOS"), ("api","API"), ("eifel","EIFEL"), ("varem","VAREM"), ("ampco","AMPCO"),
        ("tsurumi","TSURUMI"), ("gea","GEA")
    ], string="Marca", tracking=True)
    descripcion = fields.Text(string="descripcion", tracking=True)
    observaciones = fields.Selection([
        ("clientedecepcionado", "Cliente decepcionado de la empresa"), ("ocupado", "Cliente ocupado, no atendio"),
        ("norequerimientos", "El cliente no tiene requerimientos al momento"), ("demostracion", "Demostracion de productos"),
        ("recoleccion", "Recoleccion de datos para cotizaciones"),
        ("revision", "El cliente se encuentra revisando cotizaciones"),
        ("equipos", "Revision de equipos"), ("oferta", "Seguimiento de oferta"),
        ("entrega", "Entrega de equipos"), ("programacion", "Programacion de equipo"),
        ("orden", "Orden de compras"), ("cobranza", "Cobranza")
    ],string="observaciones", tracking=True)

    contacto = fields.Char(string="Contacto(Cliente)")
    telefono = fields.Char(string="Telefono(Cliente)")
    correo = fields.Char(string="Correo(Cliente)")
    departamento = fields.Char(string="Departamento(Cliente)")

    #######################################################################################################
    #                                   Funciones del modulo operaciones                                  #
    #                                                                                                     #
    #######################################################################################################



    #######################################################################################################
    #                                   Funciones que se ejecutan en el servidor                          #
    #                                                                                                     #
    #######################################################################################################

