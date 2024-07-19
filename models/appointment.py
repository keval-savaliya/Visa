import datetime
from datetime import date
from odoo import api, fields, models, SUPERUSER_ID



class visaappointment(models.Model):
	_name="visa.appointment"

	_description="appointment"

	name=fields.Char(string="Name")
	age=fields.Integer(string="Age")
	date=fields.Datetime('Date current action', default=lambda self: fields.datetime.now())
	about=fields.Text(string="About")

	def action_url(self):
		self.ensure_one()
		return{
			"type": "ir.actions.act_url",
			"url": "https://google.com",
			"target": "new",
		}
