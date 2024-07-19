from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError, MissingError, AccessError,RedirectWarning


class menufactureTask(models.Model):
	_inherit=['stock.move']

	remark=fields.Char(string="Remark")



class saleprice(models.Model):
	_inherit=['sale.order.line']

	price=fields.Float(string="price")

	@api.depends('product_uom_qty','price')
	def _compute_price_unit(self):
		for line in self:
			if line.qty_invoiced > 0 or (line.product_id.expense_policy == 'cost' and line.is_expense):
				continue
			if not line.product_uom or not line.product_id:
				line.price_unit = 0.0
			else:
				line = line.with_company(line.company_id)
				price = line._get_display_price()
				line.price_unit =line.price/line.product_uom_qty

	def _prepare_invoice_line(self, **optional_values):
		res= super(saleprice,self)._prepare_invoice_line()         # Second Method
		self.ensure_one()
		res['price2']=self.price
		return res

class InvoiceInherit(models.Model):
	_inherit=['account.move.line']

	price2=fields.Float(string="Invoice Price" ,compute='_compute_price2', store=True)

	# @api.depends('sale_line_ids')
	# def _compute_price2(self):
		# self.price2=self.sale_line_ids.price           #First Method
            