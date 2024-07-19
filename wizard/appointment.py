from odoo import models, fields, api
import datetime
from datetime import date


class appointment(models.TransientModel):
	_name='appointment.wizard'
	_description="appointment wizard"

	f1=fields.Char(string="Name", required=True)
	f2=fields.Integer(string="Age" , required=True)
	f3=fields.Text(string="About")
	f4= fields.Datetime('Date current action', default=lambda self: fields.datetime.now())

	def action_done(self):

		self.ensure_one()
		record=self.env['visa.appointment'].create({'name':self.f1,'age':self.f2,'about':self.f3,'date':self.f4})
		return record