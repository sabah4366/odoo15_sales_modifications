from odoo import  models,api,fields,_
class JobOrder(models.Model):
    _name = 'sales_task.job.order'
    _description = 'Job Order'
    date_field=fields.Date(string="Date ?")
    date_confirmation=fields.Date(string="Date(Confirmation)")
    reference=fields.Char(string="Reference")
    project_field=fields.Char(string="Project")
    sequence_number=fields.Char(string="Sequence Number",readonly=True)
    customer_name_id=fields.Many2one('res.partner',string="Customer ?",required=True)
    related_sale_order=fields.Many2one('sale.order',string="Related Sale Order")
    sale_order_lines_ids = fields.One2many('sale.order.line', 'ref_id', string='Job Order Lines ')
    estimated_line_ids=fields.One2many('sales_task.estimation','est_ref_id',string='Estimated Lines')
    full_total_area = fields.Float(string="Total Area" ,compute='_calculate_total_area',readonly=True)
    full_total_qty = fields.Float(string="Total Quantity",readonly=True)


    @api.depends('sale_order_lines_ids')
    def _calculate_total_area(self):
        self.full_total_area = sum(self.sale_order_lines_ids.mapped('area_field'))
        self.full_total_qty = sum(self.sale_order_lines_ids.mapped('quantity_line'))

    def action_pdf_job_order(self):

        return self.env.ref('sales_task.report_sales_task_job_order_pdf').report_action(self)




