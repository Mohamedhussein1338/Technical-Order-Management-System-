from odoo import models, fields, api, _


class TechnicalOrder(models.Model):
    _name = 'technical.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Technical Order'

    sequence = fields.Char(string='Request Name')

    name = fields.Char(string='Request Name',
                       required=True)

    customer = fields.Many2one('res.partner',
                               domain=[('is_tech_offer', '=', True)],
                               required=True,
                               string='Customer')

    requested_by = fields.Many2one('res.users',
                                   string='Requested By',
                                   default=lambda self: self.env.user,
                                   required=True)

    start_date = fields.Date(string='Start Date',
                             default=fields.Date.today())

    end_date = fields.Date(string='End Date')

    rejection_reason = fields.Text(string='Rejection Reason',
                                   invisible=True,
                                   readonly=True)

    order_lines_ids = fields.One2many('technical.order.line',
                                      'technical_order_id',
                                      string=' Technical Order Lines')

    total_price = fields.Float(string='Total Price',
                               compute='_compute_total_price',
                               store=True)

    status = fields.Selection([('draft', 'Draft'), ('to_be_approved', 'To be Approved'),
                               ('approve', 'Approve'), ('reject', 'Reject'),
                               ('cancel', 'Cancel'), ], string='Status', default='draft')

    sale_order_ids = fields.One2many('sale.order',
                                     'technical_order_id',
                                     string='Sale Orders',
                                     readonly=True)

    sales_order_count = fields.Integer(string='Sale Order Count',
                                       compute='_compute_sale_order_count')

    zero_remaining_quantity = fields.Boolean(compute='_compute_zero_remaining_quantity')

    def _compute_sale_order_count(self):
        count = self.env['sale.order'].search_count([('technical_order_id', '=', self.id)])
        self.sales_order_count = count


    @api.depends('order_lines_ids.remaining_quantity')
    def _compute_zero_remaining_quantity(self):
        for record in self:
            zero_remaining = any(line.remaining_quantity == 0 for line in record.order_lines_ids)
            record.zero_remaining_quantity = zero_remaining


    def view_sale_order(self):
        return {
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('technical_order_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window'
        }

    # create new sale order lines
    def create_sale_list(self):
        sale_list = []
        for sale in self.order_lines_ids:
            remaining_quantity = sale.remaining_quantity
            if remaining_quantity >= 0:
                sale_list.append(
                    (0, 0, {
                        'product_id': sale.product_id.id,
                        'product_uom_qty': remaining_quantity,
                        'price_unit': sale.cost_price,
                        'name': sale.description,
                        'price_total': sale.total,
                        'technical_order_line_id': sale.id

                    })
                )
        return sale_list

    # create new sale order with so lines
    def create_sale_order(self):
        sale_list = self.create_sale_list()
        sale_order_vals = {
            'partner_id': self.customer.id,
            'order_line': sale_list,
        }
        sale_order = self.env['sale.order'].create(sale_order_vals)
        self.sale_order_ids = [(4, sale_order.id)]

    def action_submit_for_approval(self):
        self.status = 'to_be_approved'

    def action_cancel(self):
        self.status = 'cancel'

    def action_approve(self):
        group_technical_manager = self.env.ref('technical_order_module.group_manager_technical_id')
        manager_users = group_technical_manager.users
        template = self.env.ref('technical_order_module.email_template_technical_approved')
        for user in manager_users:
            template.send_mail(self.id, force_send=True, email_values={'email_to': user.email})
            print(f'Email sent for approval to : {user.name} - Your Email is: {user.email}')
        self.status = "approve"

    def action_reset_to_draft(self):
        self.status = 'draft'

    def action_reject(self):
        return {
            'name': _('Rejection Reason'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'technical.wizard',
            'target': 'new',
        }

    @api.depends('order_lines_ids.total')
    def _compute_total_price(self):
        for req in self:
            req.total_price = sum(req.order_lines_ids.mapped('total'))

    @api.model
    def create(self, values):
        values['sequence'] = self.env["ir.sequence"].next_by_code("technical_order_code")
        return super(TechnicalOrder, self).create(values)

