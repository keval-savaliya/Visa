from odoo import models, fields, api
import datetime
from datetime import date


class selected_record(models.TransientModel):
	_name='selected.report.view'
	_description="selected.report.view"

	
	selected_record_ids = fields.Many2many('visa.client', string="Selected Record")

	@api.model
	def default_get(self, fields):
		res = super(selected_record, self).default_get(fields)
		active_ids = self.env.context.get('active_ids', [])
		if active_ids:
			res['selected_record_ids'] = [(6, 0, active_ids)]
		print(res)
		return res