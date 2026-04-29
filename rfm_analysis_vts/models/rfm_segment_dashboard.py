from odoo import models, fields, api
from datetime import datetime, time


class RfmSegmentDashboard(models.Model):
    _name = 'rfm.segment.dashboard'
    _description = 'RFM Segment Dashboard'
    _rec_name = 'segment_id'

    segment_id = fields.Many2one(comodel_name='rfm.segments', string='Segment')

    customer_count = fields.Integer(
        string='Customers',
        compute='_compute_counts',
        store=False,
        group_operator="sum"
    )

    order_count = fields.Integer(
        string='Orders',
        compute='_compute_counts',
        store=False,
        group_operator="sum"
    )
    order_percentage = fields.Float(
        string='Order %',
        compute='_compute_counts',
        digits=(16, 2),
        group_operator="avg"
    )
    customer_percentage = fields.Float(
        string='Customer %',
        compute='_compute_counts',
        digits=(16, 2),
        group_operator="avg"
    )

    def _compute_counts(self):
        # Partner = self.env['res.partner']
        SaleOrder = self.env['sale.order']
        company = self.env.company

        # BASE ORDER DOMAIN (DATE + STATE)
        base_order_domain = [
            ('state', 'in', ('sale', 'done')),
            ('partner_id.rfm_segment_id', '!=', False),
        ]

        if company.rfm_date_from:
            base_order_domain.append(('date_order', '>=', company.rfm_date_from))

        if company.rfm_date_to:
            date_to = datetime.combine(company.rfm_date_to, time.max)
            base_order_domain.append(('date_order', '<=', date_to))

        # TOTAL ORDERS (ALL SEGMENTS)
        total_orders = SaleOrder.search_count(base_order_domain)

        # TOTAL CUSTOMERS (WITH AT LEAST 1 ORDER)
        all_orders = SaleOrder.search(base_order_domain)
        total_customers = len(all_orders.mapped('partner_id'))

        for rec in self:
            # ORDERS FOR THIS SEGMENT
            segment_orders = all_orders.filtered(
                lambda o: o.partner_id.rfm_segment_id == rec.segment_id
            )

            rec.order_count = len(segment_orders)

            # CUSTOMERS FOR THIS SEGMENT
            # (ONLY CUSTOMERS WITH ORDERS)
            segment_customers = segment_orders.mapped('partner_id')
            rec.customer_count = len(segment_customers)

            # PERCENTAGES
            rec.customer_percentage = (
                round((rec.customer_count / total_customers) * 100, 2)
                if total_customers else 0.0
            )

            rec.order_percentage = (
                round((rec.order_count / total_orders) * 100, 2)
                if total_orders else 0.0
            )

    def action_open_customers(self):
        self.ensure_one()
        company = self.env.company

        order_domain = [
            ('partner_id.rfm_segment_id', '=', self.segment_id.id),
            ('state', 'in', ('sale', 'done')),
        ]

        if company.rfm_date_from:
            order_domain.append(('date_order', '>=', company.rfm_date_from))

        if company.rfm_date_to:
            date_to = datetime.combine(company.rfm_date_to, time.max)
            order_domain.append(('date_order', '<=', date_to))

        orders = self.env['sale.order'].search(order_domain)
        partner_ids = orders.mapped('partner_id').ids

        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.segment_id.name} Customers',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('id', 'in', partner_ids)],
        }

    def action_open_orders(self):
        self.ensure_one()
        company = self.env.company

        domain = [
            ('partner_id.rfm_segment_id', '=', self.segment_id.id),
            ('state', 'in', ('sale', 'done')),
        ]

        # Apply date range ONLY if configured
        if company.rfm_date_from:
            domain.append(('date_order', '>=', company.rfm_date_from))

        if company.rfm_date_to:
            date_to = datetime.combine(company.rfm_date_to, time.max)
            domain.append(('date_order', '<=', date_to))

        return {
            'type': 'ir.actions.act_window',
            'name': f'{self.segment_id.name} Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'search_default_groupby_partner': 1,
            },
        }
