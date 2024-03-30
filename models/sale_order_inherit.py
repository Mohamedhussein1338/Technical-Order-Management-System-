from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    technical_order_id = fields.Many2one('technical.order',
                                         string='Technical Order',)
