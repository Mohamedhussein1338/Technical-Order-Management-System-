from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_tech_offer = fields.Boolean(default=True)
