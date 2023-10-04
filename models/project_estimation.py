from odoo import  models,api,fields,_
class ProjectEstimation(models.Model):
    _name = 'sales_task.project.estimation'
    _description = 'Project Estimations'

    sequence_number=fields.Char(string="Sequence Number",readonly=True)
    customer_name_id=fields.Many2one('res.partner',string="Customer Name",required=True)
    creation_date = fields.Datetime(string="Creation Date",required=True)
    estimation_ids = fields.One2many('sales_task.estimation', 'project_est_id',
                                     string="Estimation" )


    def sl_number(self):
        sl_no=0
        for rec in self.estimation_ids:
            sl_no+=1
            rec.serial_no=sl_no

    def name_get(self):
        return [(record.id,' %s' % (record.sequence_number)) for record in self]

    @api.model
    def create(self, vals):
        vals['sequence_number'] = self.env['ir.sequence'].next_by_code('sales_task.project.estimation')
        res = super(ProjectEstimation, self).create(vals)
        res.sl_number()
        return res

    def write(self, vals):
        if not self.sequence_number and not vals.get('sequence_number'):
            vals['sequence_number']=self.env['ir.sequence'].next_by_code('sales_task.project.estimation')
        res = super(ProjectEstimation, self).write(vals)
        self.sl_number()
        return res

    def action_convert_quotation(self):
        vals={
            'related_estimation': self.sequence_number,
            'partner_id': self.customer_name_id.id,
            'state':'draft',
            'date_order':self.creation_date,
            'estimation_lines_ids':self.estimation_ids,
            }
        self.env['sale.order'].create(vals)

        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Successfully Created a Quotation!!',
                'type': 'rainbow_man'
            }
        }


class Estimation(models.Model):
    _name = 'sales_task.estimation'
    _description = 'Estimations'

    serial_no=fields.Integer(string="SL No.",readonly=True,)
    description=fields.Many2one('sales_task.description',string="Description")
    width=fields.Float(string="Width")
    length=fields.Float(string="Length")
    area=fields.Float(string="Area", compute=('_compute_area') ,store=True)
    quantity=fields.Float(string="Quantity")
    total=fields.Float(string="Total",compute=('_compute_total') ,store=True)
    project_est_id=fields.Many2one('sales_task.project.estimation' ,string='Project Est.',ondelete='cascade')
    ref_id = fields.Many2one('sale.order', string='Reference',ondelete='cascade')
    est_ref_id=fields.Many2one('sales_task.job.order',string="Estimation Lines")
    customer_ref = fields.Many2one('res.partner', string="Cust.Ref")
    job_no = fields.Integer(string='Jo No')
    colour_field = fields.Many2one('sales_task.color', string="Colour")
    order_line_ref_id = fields.Many2one('sale.order.line', string="Order Line Ref")

    @api.onchange('job_no')
    def job_no_auto_colour(self):
        for line in self:
            record = self.env['sales_task.color'].browse(line.job_no).exists()
            if record:
                line.colour_field = record
            else:
                line.colour_field = ''

    @api.depends('width','length')
    def _compute_area(self):
        for rec in self:
            rec.area = rec.width * rec.length

    @api.depends('area', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.area * rec.quantity


class Description(models.Model):
    _name = 'sales_task.description'
    _description = 'Description '

    name=fields.Char(string="Name")

