from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    technical_order_line_id = fields.Many2one('technical.order.line',
                                              string='Technical Order Line')

    @api.constrains('product_uom_qty')
    def _check_technical_order_quantity(self):
        for rec in self:
            if rec.product_uom_qty > rec.technical_order_line_id.quantity:
              raise ValidationError( f"The quantity in sale order line '{rec.product_id.name}' cannot exceed the quantity in the related technical order line.")