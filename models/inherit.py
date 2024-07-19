from odoo import fields, models, api


class parent(models.Model):
	_name="parent.model"
	_description="parent model"

	parent=fields.Char(string="Parent")
	is_rich=fields.Boolean(string="Is Rich")

	# def test(self):
	# 	return self.test_check("parent model")

	# def test_check(self,s):
	# 	return f'this is {s}'

class child(models.Model):
	# _name="child.model"
	_inherit="parent.model"

	# _description="child model"
	child=fields.Char(string="Child")
	child_intro=fields.Html(string="Child Introduction")
	ty=fields.Many2one('visa.type',string="type")
	# cust_mess=fields.Char()


	# def test(self):
	# 	return self.test_check("child model")

	# @api.model
	# def create(self,vals):
	# 	vals={'parent':"MNO",'child':'mno'}
	# 	print("create")
	# 	rec=super(parent,self).create(vals)
	# 	print(rec.test())
	# 	return rec

	# def inherit_action(self):
	# 	pass
	# 	rec=self.env['parent.model'].create({'parent':"MNO"})
	# 	print(rec.test())
	# 	return rec



class task(models.Model):
	_inherit="sale.order"

	task=fields.Many2one('visa.type',string="task")




