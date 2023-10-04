from odoo import api,fields,models
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    related_estimation=fields.Many2one('sales_task.project.estimation' ,string='Related Estimation')
    estimation_lines_ids=fields.One2many('sales_task.estimation' ,'ref_id' ,string='Estimation Lines')
    ref_id=fields.Many2one('sales_task.job.order',string='Reference')






    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        #serial number for job order
        serial_number = self.env['ir.sequence'].next_by_code('sales_task.job.order')
        for rec in self.order_line:
            #colour fetching from color model
            record = self.env['sales_task.color'].browse(rec.line_no).exists()
            if record:
                rec.colour = record
            #area based on qty and sqmt
            if rec.product_uom_qty > 0:
                rec.area_field = rec.product_uom_qty
            elif rec.quantity_line > 0:
                rec.area_field = rec.quantity_line
            else:
                rec.area_field = 0

        vals={
            'related_sale_order': self.id,
            'customer_name_id': self.partner_id.id,
            'sequence_number': serial_number,
            'sale_order_lines_ids': self.order_line,
            'estimated_line_ids':self.estimation_lines_ids

        }
        action = self.env['sales_task.job.order'].create(vals)

        return {'name': 'job order',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sales_task.job.order',
                'res_id':action.id,
                'type': 'ir.actions.act_window',
                'target': 'self'
                }
