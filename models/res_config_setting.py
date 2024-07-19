from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    send_email = fields.Boolean(string="Send Email", config_parameter='Visa.send_email')
