import base64
import io
from odoo import models

class resumenotXlsx(models.AbstractModel):
    _name = 'report.modulo_operaciones.resume_ot_template_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data):
        sheet = workbook.add_worksheet("Resumen")
        bold = workbook.add_format({'bold': True,
                                    'align': 'center'})
        row = 3
        col = 3
        sheet.write(row, col, "reference", bold)
        sheet.write(row, col + 1, "reference", bold)

