from odoo import models, fields, api
import datetime
from datetime import date


class createexcel(models.TransientModel):
	_name='excel.wizard'
	_description="excel wizard"

	title = fields.Char(string="Title",required=True)
	detail_ids=fields.One2many('visa.client','mobile',string="Details")
	f2=fields.Integer(string="Age" , required=True)
	document_id=fields.Many2one('visa.document',string="Documents")

	def create_excel(self):
		# print(self.read()[0])
		data=self.read()[0]
		detail_data = self.detail_ids.read(['fname', 'married_status', 'country'])
		data['detail_ids'] = detail_data
		data['document_name'] = self.document_id.document_name if self.document_id else '' 
		return self.env.ref('Visa.wizard_xlsx_report_1').report_action(self, data=data)
