from odoo import models
from io import BytesIO
import xlsxwriter

class WizardXlsxReport(models.AbstractModel):
    _name = 'report.report.excel.wizard_xlsx_report_start'

    def generate_xlsx_report(self, workbook, data, records):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Clients')

        # Formats for cell styles
        head_format = workbook.add_format({
            'align': 'center',
            'font_size': 20,
            'bold': True,
            'border': 2,
            'bg_color': '#FFFF00'
        })
        att_format = workbook.add_format({
            'align': 'center',
            'font_size': 16,
            'bold': True
        })
        xatt_format = workbook.add_format({
            'align': 'center',
            'font_size': 12,
            'bold': True
        })

        # Merge cells and write header
        sheet.merge_range('A1:H2', 'Wizard Excel', head_format)
        sheet.write(3, 0, 'Title', att_format)
        sheet.write(3, 1, 'First name', att_format)
        sheet.write(3, 3, 'Age', att_format)
        sheet.write(3, 4, 'Married Status', att_format)
        sheet.write(3, 5, 'Country', att_format)
        sheet.write(3, 6, 'Document', att_format)

        # Write data
        row = 4
        for detail in data['detail_ids']:
            sheet.write(row, 0, data['title'] or '', xatt_format)
            sheet.write(row, 1, detail.get('fname', '') or '', xatt_format)
            sheet.write(row, 3, data['f2'] or '', xatt_format)
            sheet.write(row, 4, detail.get('married_status', '') or '', xatt_format)
            sheet.write(row, 5, detail.get('country', '') or '', xatt_format)
            sheet.write(row, 6, data['document_name'] or '', xatt_format)
            row += 1

        workbook.close()
        output.seek(0)
        xlsreport = output.read()
        output.close()

        # Return the XLSX report content
        return xlsreport
