from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TechnicalOrderLine(models.Model):
    _name = 'technical.order.line'
    _description = 'Technical Order Line'

    product_id = fields.Many2one('product.product',
                                 string='Product',
                                 required=True)

    description = fields.Char(string='Description',
                              related='product_id.name',
                              store=True)

    quantity = fields.Float(string='Quantity',
                            default=1)

    cost_price = fields.Float(string='Cost Price',
                              related='product_id.standard_price',
                              readonly=True)

    total = fields.Float(string='Total',
                         compute='_compute_total',
                         store=True)

    remaining_quantity= fields.Float(string='Remaining Quantity',
                                     compute='_compute_quantity')

    sale_order_lines_id = fields.One2many('sale.order.line',
                                          'technical_order_line_id')

    technical_order_id = fields.Many2one('technical.order',
                                         string='Technical Order')

    sale_order_id = fields.Many2one('sale.order')

    @api.depends('quantity', 'cost_price')
    def _compute_total(self):
        for line in self:
            line.total = line.quantity * line.cost_price


    @api.depends('quantity', 'sale_order_lines_id.product_uom_qty')
    def _compute_quantity(self):
        for record in self:
            total_sold_quantity = sum(
                line.product_uom_qty for line in record.sale_order_lines_id if line.state == 'sale')
            record.remaining_quantity = record.quantity - total_sold_quantity
            if record.quantity == 0:
              raise ValidationError("The original quantity cannot be zero.")
