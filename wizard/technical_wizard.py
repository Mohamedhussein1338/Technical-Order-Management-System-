from odoo import models, api, fields
from datetime import date, datetime, time


class TechnicalWizard(models.TransientModel):
    _name = "technical.wizard"
    _description = "technical wizard"

    rejection_reasone= fields.Text("Rejection Reason", required=True)

    def action_add_rejection(self):
        active_id = self.env.context.get('active_id')
        current_request = self.env['technical.order'].search([('id', '=', active_id)])
        current_request.rejection_reason = self.rejection_reasone
        current_request.status = 'reject'
