from odoo import api,fields,models
class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    product_uom_qty=fields.Float(string='Sqmt',default=0.0)
    quantity_line=fields.Float(string="Quantity",default=0)
    seq_number=fields.Char('No.',store=True)
    area_field = fields.Float( string='Area',store=True)
    colour=fields.Many2one('sales_task.color',string='Colour',store=True)
    line_no = fields.Integer(string="SNo:" , readonly=True, compute = '_get_line_numbers' )
    ref_id = fields.Many2one('sales_task.job.order', string='Reference')
    estimation_line_ids=fields.One2many('sales_task.estimation' ,'order_line_ref_id' ,string='Estimation Lines')


    #serial number for orderlines
    @api.depends('order_id.order_line')
    def _get_line_numbers(self):
        for line in self:
            no=0
            line.line_no=no
            for ln in line.order_id.order_line:
                no += 1
                ln.line_no = no

    #for sqmt getting zero value
    @api.onchange('product_id')
    def product_sqmt_changing(self):
        self.product_uom_qty = 0

    @api.depends('price_unit', 'product_uom_qty', 'quantity_line', 'tax_id')
    def _compute_amount(self):
        for order_line in self:
                # Calculate taxes for quantity_line
                quantity_taxes = order_line.tax_id.compute_all(
                    order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0),
                    order_line.order_id.currency_id,
                    order_line.quantity_line,
                    order_line.product_id,
                    order_line.order_id.partner_shipping_id
                )
                # Calculate taxes for product_uom_qty
                uom_quantity_taxes = order_line.tax_id.compute_all(
                    order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0),
                    order_line.order_id.currency_id,
                    order_line.product_uom_qty,
                    order_line.product_id,
                    order_line.order_id.partner_shipping_id
                )

                # Calculate the total amount including taxes for both quantity and product_uom_qty
                total_with_quantity_and_tax = (
                    quantity_taxes['total_included'] if order_line.product_uom_qty == 0.0 else uom_quantity_taxes[
                        'total_included'])

                # Update price_total with tax included
                order_line.price_total = total_with_quantity_and_tax

