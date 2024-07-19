from odoo import models, fields, api

class TaskWizard(models.TransientModel):
    _name = 'task.wizard'
    _description = "task wizard"

    name_id = fields.Many2one('visa.type', string="Visa Type")    
    detail_ids = fields.One2many('task2.wizard', 'type_id', string="details")

    @api.onchange("name_id")
    def _onchange_fname(self):

        details = []
        self.write({'detail_ids': [(5, 0, details)]})
        record = self.env['visa.client'].search([('name_id', '=', self.name_id.id)])
        details.clear()
        for rec in record:
            details.append((0, 0, {
                'fname': rec.fname,
                'lname': rec.lname,
                'dob': rec.dob,
                'age': rec.age,
                'email': rec.email,
                'country': rec.country,
            }))
        self.detail_ids = details

class Task2Wizard(models.TransientModel):
    _name = "task2.wizard"
    _description = "task2"

    type_id = fields.Many2one('task.wizard', string="Task Wizard")    
    fname = fields.Char(string="First name")
    lname = fields.Char(string="Last name")
    dob = fields.Date(string="Date of birth")
    age = fields.Integer(string="Age", compute="_compute_age")
    email = fields.Char(string="E-mail")
    country = fields.Selection([
        ('united_kingdom', 'United Kingdom'),
        ('canada', 'Canada'),
        ('australia', 'Australia'),
        ('china', 'China')
    ], string='Country', default="canada")

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = fields.Date.today()
                delta = today - record.dob
                record.age = delta.days // 365
            else:
                record.age = 0
