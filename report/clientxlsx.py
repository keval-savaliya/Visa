from odoo import models, fields, api
import io
import xlsxwriter

class ClientXlsx(models.AbstractModel):
    _name = 'report.visa.type_xlsx_report_start'
    _description = 'Visa Type XLSX Report'

    def generate_xlsx_report(self, workbook, data, records):
        sheet = workbook.add_worksheet('Clients')

        # Define cell formats
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

        # Merge and write header
        sheet.merge_range('A1:F2', 'First Excel', head_format)
        sheet.write(3, 0, 'Type', att_format)
        sheet.write(3, 1, 'First Name', att_format)
        sheet.write(3, 2, 'Date Of Birth', att_format)
        sheet.write(3, 3, 'Email', att_format)
        sheet.write(3, 4, 'Phone', att_format)

        # Write data rows
        row = 4
        for rec in records:
            for d in rec.detail_ids:
                sheet.write(row, 0, rec.name or '', xatt_format)
                sheet.write(row, 1, d.fname or '', xatt_format)
                sheet.write(row, 2, d.dob or '', xatt_format)
                sheet.write(row, 3, d.email or '', xatt_format)
                sheet.write(row, 4, d.mobile or '', xatt_format)
                row += 1

    @api.model
    def get_report(self):
        # Example method to trigger report generation
        records = self.env['your.model'].search([])

        # Create Excel file in memory
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        self.generate_xlsx_report(workbook, {}, records)
        workbook.close()
        output.seek(0)

        # Return the Excel file as byte stream
        return {
            'file': output.getvalue(),
            'filename': 'visa_type_report.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
