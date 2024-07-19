from odoo import models, fields, api
import datetime
from datetime import date
from odoo.exceptions import UserError


class selected_project(models.TransientModel):
	_name='selected.report.project'
	_description="selected.report.project"

	
	partner_id = fields.Many2one('res.partner', string='Partner', required=True)
	partner_name = fields.Char(string='Partner Name')
	project_ids = fields.Many2many('project.project', string='Projects')

	# @api.model
	# def default_get(self, fields):
	# 	res = super(selected_project, self).default_get(fields)
	# 	partner_id = self.env.context.get('active_id')
	# 	partner_name=self.env['visa.client'].browse(partner_id).id_user.name
	# 	print(partner_name)
	# 	if partner_id:
	# 		res['partner_id'] = partner_id
	# 		rec=self.env['project.project'].search([('partner_id', '=', partner_name)]).ids
	# 		if rec:
	# 			res['project_ids'] = [(6, 0, rec)]
	# 			print(res)
	# 			return res
	# 		else:
	# 			raise UserError("This User Does Not Hold Any Project Yet..!")


	@api.model
	def default_get(self, fields):
		res = super(selected_project, self).default_get(fields)
		partner_ids = self.env.context.get('active_ids',[])
		print(partner_ids)
		recs=[]
		for partner_id in partner_ids:

			partner_name=self.env['visa.client'].browse(partner_id).id_user.name
			print(partner_name)

			res['partner_id'] = partner_id
			rec=self.env['project.project'].search([('partner_id', '=', partner_name)]).ids

			if rec:
				recs.extend(rec)
		if recs:
			res['project_ids'] = [(6, 0, recs)]
			return res;
		else:
			raise UserError("This User Does Not Hold Any Project Yet..!")

		
	# @api.model
	# def default_get(self, fields):
	# 	res = super(SelectedProject, self).default_get(fields)
	# 	partner_ids = self.env.context.get('active_ids', [])

	# 	print(partner_ids)

	# 	if partner_ids:
	# 		project_ids = []

	# 		for partner_id in partner_ids:
	# 			partner = self.env['visa.client'].browse(partner_id)
	# 			partner_name = partner.id_user.name
	# 			print(partner_name)

	# 			res['partner_id'] = partner_id
	# 			recs = self.env['project.project'].search([('partner_id', '=', partner.id)])
				
	# 			if recs:
	# 				project_ids.extend(recs.ids)
	# 				print(res)
	# 			else:
	# 				raise UserError("User with ID %s does not hold any projects yet!" % partner_id)

	# 			res['project_ids'] = [(6, 0, project_ids)]
	# 		return res