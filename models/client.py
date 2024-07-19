from datetime import date
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning


# we can create module with single line of cmd script
# step-1: "cd custom"
# step-2: "/home/keval/odoo_workspace/odoo-16.0/odoo-bin scaffold hello"

# (0,0): Create a record in comodel
# (1,ID): Update a record in comodel
# (2,ID): Delete a record and Remove a relation (must care about many2many field)
# (3,ID): Unlink or Remove relation  (must care about one2many field ex:ondelete)
# (4,ID): Crate a relation or link
# (5,ID): Remove all record from the relation with exixting record (unlink all record)
# (6,ID): Set: first unlink Than Link


class visatype(models.Model):
    _name = "visa.type"
    _description = "Type of visa"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    category = fields.Selection([('long term', 'Long Term'), ('short term', 'Short Term'), ('special', 'Special')],
                                default="short term", string="Terms")
    minimun_age = fields.Integer(string="Minimun Age", default="16")
    maximum_stay = fields.Integer(string="Maximum Stay")
    renewable = fields.Boolean(string="Renewable")
    fees = fields.Float(string="Application Fee")
    visa_onditions = fields.Text(string="Visa Conditions")
    bgimage = fields.Image()

    detail_ids = fields.One2many('visa.client', 'name_id', string="Details")
    tourist_count = fields.Integer(compute="_tourist_count")
    travel_count = fields.Integer(compute="_travel_count")
    business_count = fields.Integer(compute="_business_count")

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Visa type must be unique')
    ]

    @api.depends('name')
    def _tourist_count(self):
        self.tourist_count = self.env['visa.client'].search_count([('name_id', '=', 'Tourist')])

    @api.depends('name')
    def _travel_count(self):
        self.travel_count = self.env['visa.client'].search_count([('name_id', '=', 'Travel')])

    @api.depends('name')
    def _business_count(self):
        self.business_count = self.env['visa.client'].search_count([('name_id', '=', 'Business')])

    def get_tourist(self):
        pass
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tourist',
            'view_mode': 'tree',
            'res_model': 'visa.client',
            'domain': [('name_id', '=', 'Tourist')],
            'context': "{'create': False}"
        }

    def get_travel(self):
        pass
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Travel',
            'view_mode': 'tree',
            'res_model': 'visa.client',
            'domain': [('name_id', '=', 'Travel')],
            'context': "{'create': False}"
        }

    def get_business(self):
        pass
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Business',
            'view_mode': 'tree',
            'res_model': 'visa.client',
            'domain': [('name_id', '=', 'Business')],
            'context': "{'create': False}"
        }

    def create_action(self):

        record = self.env['visa.create'].search([('create_name', '=', self.name)])

        if record:
            l2 = []
            for rec in record:
                l2.append(rec.id)
            print(l2)
            self.env['visa.create'].browse(l2).unlink()

        # l = []
        # for rec in self:
        # 	for x in rec.detail_ids:
        # 		l.append((1, rec.id, {
        # 'fname': x.fname,
        # 			'lname': x.lname,
        # 			'dob': x.dob,
        # 			'age': x.age,
        # 			'email': x.email,
        # 			'country': x.country,
        # 		}))
        # print(l)

        l = []
        for rec in self:
            for x in rec.detail_ids:
                l.append((0, 0, {
                    'fname': x.fname,
                    'lname': x.lname,
                    'dob': x.dob,
                    'age': x.age,
                    'email': x.email,
                    'country': x.country,
                }))
        print(l)

        self.env['visa.create'].create({'create_name': self.name, 'o2m_ids': l})


class create(models.Model):
    _name = "visa.create"
    _description = "create"

    create_name = fields.Char(string="name")
    o2m_ids = fields.One2many('visa.client', 'mobile', string="new")


class visadocument(models.Model):
    _name = "visa.document"
    _rec_name = "document_name"
    _description = "Type of document"

    document_name = fields.Char(string="Document Name", required=True)
    verify = fields.Boolean(string="It's Verify")
    doc = fields.Binary(string="upload Document")


class visaclient(models.Model):
    _name = "visa.client"
    _rec_name = "client_seq"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Visa Client"

    id_user = fields.Many2one('res.partner', string='User', tracking=True)

    client_seq = fields.Char(string="client sequence", required=True, invisible=True, readonly=True,
                             default=lambda self: _('New'))
    fname = fields.Char(string="First name", required=True)
    lname = fields.Char(string="last name")
    name_id = fields.Many2one('visa.type', string="Name", default="Tourist")  # domain=[('name','!=','Travel')]
    dob = fields.Date(string="Date of birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    height = fields.Float(string="Height", digits=(16, 4))
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender',
                              default='male')
    mobile = fields.Char(string="Mobile")
    add1 = fields.Char(string="Address 1")
    add2 = fields.Char(string="Address 2")
    email = fields.Char(string="E-mail")
    date_action = fields.Datetime('Application Date', default=lambda self: fields.datetime.now())
    image = fields.Image(string="Photo")
    married_status = fields.Selection([('married', 'Married'), ('single', 'Single'), ['unmarried', 'Unmarried']],
                                      string='Married_status', default="married")
    country = fields.Selection(
        [('united kingdome', 'United kingdome'), ('canada', 'Canada'), ('austrelia', 'Austrelia'), ('china', 'China')],
        string='Country', default="canada")
    state = fields.Selection([('draft', 'Draft'), ('cancel', 'Cancel'), ('done', 'Done'), ('confirm', 'Confirm')],
                             tracking=True, string='Status', default="cancel")
    family = fields.One2many('visa.family', 'x')
    document_ids = fields.Many2many('visa.document', string="Documents")
    html = fields.Html(string="HTML")
    reason = fields.Text(string="Reason")

    company_id = fields.Many2one('res.company')
    address_id = fields.Many2one('res.partner', string="Address")
    email_from = fields.Char(string="From")
    confirm = fields.Boolean(string='Confirm', default=True)
    reference_appiontment = fields.Reference(selection=[('visa.appointment', 'appointment')], string="Record")
    ID = fields.Integer(string="ID")
    start = fields.Char()
    start_date = fields.Date(string="Start Date")
    stop_date = fields.Date(string="End Date")

    @api.autovacuum
    def _autovacuum(self):
        records_to_delete = self.search([('dob', '=', False)])
        records_to_delete.unlink()

    @api.model
    def create(self, vals):

        if vals.get('client_seq', _('New')) == _('New'):
            vals['client_seq'] = self.env['ir.sequence'].next_by_code('visa.client') or _('New')

        # if vals['height'] == 0.0000:
        # 	raise UserError("Enter Your Height")
        # 	# return {'value':{},'warning':{'title':'warning','message':'Your message'}}

        # rec=self.env['visa.client'].search([('email','=',vals['email'])])
        # if rec:
        # 	raise ValidationError('Another user is already created using this email')

        res = super(visaclient, self).create(vals)
        return res

    # def write(self,vals):
    # 	vals['lname']=vals['lname'].capitalize()
    # 	print('write')
    # 	return super(visaclient,self).write(vals)

    # # @api.returns('self',lambda val:val.id)
    # def copy(self,default_list=None):
    # 	print('read')
    # 	if default_list is None:
    # 		default_list={}
    # 	default_list['lname']=f'copy {self.lname}'
    # 	return super(visaclient,self).copy(default=default_list)

    # def unlink(self):
    # 	print('unlink')
    # 	for rec in self:
    # 		if rec.age > 20:
    # 			raise UserError(f"You can not delete this record")
    # 	return super(visaclient,self).unlink()

    # @api.model
    # def name_create(self, name):
    # 	print("name_create")
    # 	return super(visaclient, self).name_create(name)

    # @api.model
    # def default_get(self,field_list=[]):
    # 	rtn=super(visaclient,self).default_get([])
    # 	print(f'befor : {rtn}')
    # 	rtn['name_id']="Travel"
    # 	return rtn

    # @api.model
    # def sort(self):
    # 	self.age=self.age.sorted(key=lambda self:self.age)
    # 	rtn=super(visaclient,self).sort()
    # 	return rtn

    # @api.depends('dob')
    # def _compute_age(self):
    # 	for rec in self:
    # 		if rec.dob:
    # 			today=date.today()
    # 			rec.age=today.year-rec.dob.year
    # 		else:
    # 			rec.age=1

    @api.depends(lambda self: self.my_function())
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 1

    def my_function(self):
        return ['dob']

    @api.constrains('lname')
    def _constrains_reconcile(self):
        for record in self:
            if record.lname is False:
                raise UserError(('Enter last name'))

    @api.onchange("fname")
    def _onchange_fname(self):
        self.start = "hello! %s" % (self.fname)

    def confirm_action(self):

        # pass

        # try:
        # 	rec=self.env['visa.client'].browse(155)
        # 	if rec.exists():
        # 		print(rec)
        # 	else:
        # 		raise MissingError('Record is Missing')
        # except:
        # 	raise MissingError('Record is Missing')

        action = self.env.ref('Visa.visa_type_action')
        msg = _('Redirect into visa type.')
        raise RedirectWarning(msg, action.id, _('Go to type'))

    # 	# create
    # rec=self.env['visa.client'].create({'married_status':'unmarried'})
    # print(rec)
    # return rec

    # 	# write
    # self.write({'lname': 'default'})

    # 	# flush
    # rec=self.env['visa.client'].flush(['fname','lname'])
    # print(rec)
    # return rec

    # browse
    # rec=self.env['visa.client'].browse([18,30])
    # print(rec)
    # return rec

    # 	# read
    # l=[]
    # record=self.env['visa.client'].search([])
    # for rec in record:
    # 	if rec.fname=="xyz":
    # 		l.append(rec.id)
    # self.env['visa.client'].browse(l).read()
    # print("read is done")

    # 	# unlink
    # l=[]
    # record=self.env['visa.client'].search([])
    # for rec in record:
    # 	if rec.fname=="xyz":
    # 		l.append(rec.id)
    # self.env['visa.client'].browse(l).unlink()

    # 	# sorted
    # record=self.env['visa.client'].search([])
    # sorted_record = sorted(record, key=lambda r: r.fname)
    # print(sorted_record)

    # 	# search
    # rec=self.env['visa.client'].search(['|',('gender','=','female'),('country','=','canada')])
    # print(rec)
    # return rec

    # 	# search_count
    # rec=self.env['visa.client'].search_count(['|',('gender','=','female'),('country','=','canada')])
    # print(rec)
    # return rec

    # task

    # record=self.env['visa.type'].search([('name','=','Travel')])
    # rec=self.env['visa.client'].create({'married_status':'unmarried','name_id':record.id})
    # print(rec)
    # return rec

    def action_confirm(self):
        # x=1
        for record in self:
            record.state = 'confirm'

        # record.write({'ID':x})
        # x+=1

    # def birthday_reminder(self):
    # 	record=self.env['visa.client'].search([])
    # 	for rec in record:
    # 		if self.dob:
    # 			mail_val={
    # 				'email_to':rec.email,
    # 				'subject':"Birthday Reminder",
    # 				'body_html':"One Day Remian to Your Birthday"
    # 			}
    # 			mail=self.env['mail.mail'].sudo().create(mail_val)
    # 			mail.send()

    @api.onchange("state")
    def _onchange_state(self):
        if self.state == 'confirm':
            # using _message_log() method

            body = f'hello {self.fname}, Your Application is Confirm'
            self._message_log(body=body)

        # # using message.post() method // "You need to take a object of record then you use it"
        # s = self.env['visa.client'].search([('client_seq','=',self.client_seq)])
        # body = f'hello {self.fname}, Your Application is Confirm'
        # s.message_post(body=body)

    def action_send_email(self):
        send_email = self.env['ir.config_parameter'].sudo().get_param('Visa.send_email')
        print(send_email)
        if send_email:
            t_id = self.env.ref('Visa.email_template_visa').id
            self.env['mail.template'].browse(t_id).send_mail(self.id, force_send=True)
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Record state is confirm',
                    'type': 'rainbow_man'
                }
            }
        else:
            raise UserError('You can not send an Email to client. First you need to set Config Parameter')


class visafamily(models.Model):
    _name = "visa.family"
    _description = "detail about family"

    fm_name = fields.Char(string="Member Name", required=True)
    fage = fields.Integer(string="Age")
    relation = fields.Selection(
        [('father', 'Father'), ('mother', 'Mother'), ('son', 'Son'), ('daughter', 'Daughter'), ('brother', 'Brother'),
         ('sister', 'Sister')], default='father', string="relation")
    occupation = fields.Selection(
        [('business', 'Business'), ('farmer', 'Farmer'), ('house wife', 'House wife'), ('student', 'Student'),
         ('other', 'Other')], default='business', string="Occupation")
    x = fields.Many2one('visa.client', invisible=1)
    currency_id = fields.Many2one('res.currency', string='Currency')
    income = fields.Float(string="Income")


class visaservant(models.Model):
    _name = 'visa.servant'
    _inherits = {'visa.client': 'client_name'}
    _description = 'visa servant'

    servant = fields.Char(string="Servant Name")
    client_name = fields.Many2one('visa.client', string="Client Name", ondelete="cascade", required=True)
