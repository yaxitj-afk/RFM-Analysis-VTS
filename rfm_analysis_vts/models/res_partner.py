import logging
from odoo import models, fields, api

_logger = logging.getLogger("RFM")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_orders = fields.Integer(
        string="Total Orders",
        compute="_compute_partner_order_summary",
        store=True
    )
    average_total_amount = fields.Float(
        string="Avg Order Amount",
        compute="_compute_partner_order_summary",
        store=True
    )
    life_time_order_value = fields.Float(
        string="Lifetime Order Value",
        compute="_compute_partner_order_summary",
        store=True
    )
    last_order_date = fields.Datetime(
        string="Last Order Date",
        compute="_compute_partner_order_summary",
        store=True
    )
    average_days_between_orders = fields.Float(
        string="Average Days Between Orders",
        compute="_compute_partner_order_summary",
        store=True
    )
    average_order_frequency = fields.Float(
        string="Average Order Frequency / Month",
        compute="_compute_partner_order_summary",
        store=True
    )

    rfm_recency_score = fields.Integer()
    rfm_frequency_score = fields.Integer()
    rfm_monetary_score = fields.Integer()

    rfm_score = fields.Char(string="RFM Score")
    rfm_segment_id = fields.Many2one(comodel_name="rfm.segments", copy=False)

    rfm_last_computed = fields.Datetime()
    rfm_recency = fields.Integer(
        string="Recency (days)",
        compute="_compute_rfm_recency",
        store=True
    )
    total_orders_by_date_range = fields.Integer(string="Total Order By Date Range",
                                                compute="_compute_partner_order_summary_by_date_range", store=True)
    total_orders_amount_by_date_range = fields.Float(string="Total Order Amount By Date Range",
                                                     compute="_compute_partner_order_summary_by_date_range", store=True)
    rfm_log_ids = fields.One2many('rfm.log','partner_id',string="Logs Details")

    def calculate_total_order_amount_and_total_order_by_date_range(self, partner):
        company = self.env.company
        orders = partner.sale_order_ids.filtered(
            lambda o:
            o.state in ('sale', 'done')
            and o.date_order
            and (not company.rfm_date_from or o.date_order.date() >= company.rfm_date_from)
            and (not company.rfm_date_to or o.date_order.date() <= company.rfm_date_to)
            and o.company_id == company
        ).sorted('date_order')

        count = len(orders)
        amount = sum(orders.mapped('amount_total'))

        partner.total_orders_by_date_range = count
        partner.total_orders_amount_by_date_range = amount

    @api.depends('sale_order_ids.state', 'sale_order_ids.amount_total', 'sale_order_ids.date_order')
    def _compute_partner_order_summary_by_date_range(self):
        for partner in self:
            self.calculate_total_order_amount_and_total_order_by_date_range(partner)

    @api.depends('last_order_date')
    def _compute_rfm_recency(self):
        for partner in self:
            if partner.last_order_date:
                delta = fields.Date.today() - partner.last_order_date.date()
                partner.rfm_recency = delta.days
            else:
                partner.rfm_recency = 0

    def _get_rfm_score(self, metric, value,partner_tags):
        """This method call for search the rfm rule based on metric and value"""
        base_domain = [
            ('metric', '=', metric),
            ('value_from', '<=', value),
            ('value_to', '>=', value),
            ('active', '=', True),
        ]

        rule=False
        partner_category_ids = partner_tags.ids
        if partner_category_ids:
            rules = self.env['rfm.rule'].sudo().search(base_domain + [('partner_category_ids', 'in', partner_tags.ids)],order='sequence')
            for rl in rules:
                if (rl.partner_category_ids.ids) == partner_category_ids:
                    rule = rl
                    break
        if not rule:
            rule = self.env['rfm.rule'].search(base_domain + [('partner_category_ids', '=', False)],order='sequence',limit=1)

        return rule.score if rule else 0

    def compute_rfm(self):
        """This method use for compute the partner's RFM score and assign segment based on RFM score"""
        segment_rules = self.env['rfm.segment.rule'].search(
            [('active', '=', True)],
            order='sequence'
        )

        for partner in self:
            old_segment = partner.rfm_segment_id
            # Defensive: skip non-customers if you want
            # if not partner.customer_rank:
            #     continue
            self.calculate_total_order_amount_and_total_order_by_date_range(partner)
            partner.rfm_recency_score = self._get_rfm_score(
                'recency', partner.rfm_recency or 0, partner.category_id
            )
            partner.rfm_frequency_score = self._get_rfm_score(
                'frequency', partner.total_orders_by_date_range or 0, partner.category_id
            )
            partner.rfm_monetary_score = self._get_rfm_score(
                'monetary', partner.total_orders_amount_by_date_range or 0, partner.category_id
            )

            partner.rfm_score = "%s%s%s" % (
                partner.rfm_recency_score,
                partner.rfm_frequency_score,
                partner.rfm_monetary_score,
            )

            # Segment assignment
            partner.rfm_segment_id = False
            new_segment = False
            for rule in segment_rules:
                if (
                        partner.rfm_recency_score >= rule.recency_min and
                        partner.rfm_frequency_score >= rule.frequency_min and
                        partner.rfm_monetary_score >= rule.monetary_min
                ):
                    partner.rfm_segment_id = rule.segment_id
                    new_segment = partner.rfm_segment_id
                    break

            if old_segment != new_segment:
                self.env['rfm.log'].sudo().create({
                    'order_date': fields.Datetime.now(),
                    'partner_id': partner.id,
                    'old_segment_id':old_segment.id,
                    'new_segment_id':partner.rfm_segment_id.id
                })
            partner.rfm_last_computed = fields.Datetime.now()

    def action_compute_rfm(self):
        """This method use for compute the partner's RFM score and assign segment based on RFM score manually"""
        self.compute_rfm()
        return True

    @api.depends('sale_order_ids.state', 'sale_order_ids.amount_total', 'sale_order_ids.date_order')
    def _compute_partner_order_summary(self):
        """This method use for count order and total amount of order and average days of order and average amount of order"""
        for partner in self:
            orders = partner.sale_order_ids.filtered(lambda o: o.state in ('sale', 'done') and o.date_order).sorted(
                'date_order')

            count = len(orders)
            amount = sum(orders.mapped('amount_total'))

            partner.total_orders = count
            partner.life_time_order_value = amount
            partner.average_total_amount = amount / count if count else 0.0

            if not count:
                partner.last_order_date = False
                partner.average_days_between_orders = 0.0
                partner.average_order_frequency = 0.0
                continue

            first, last = orders[0].date_order, orders[-1].date_order
            partner.last_order_date = last

            if count == 1:
                partner.average_days_between_orders = 0.0
                partner.average_order_frequency = 1.0
                continue

            days = max((last - first).days, 1)

            partner.average_days_between_orders = days / (count - 1)
            partner.average_order_frequency = count / (days / 30.0)
            partner.compute_rfm()

    @api.model
    def _cron_compute_rfm(self):
        """Cron entry point for RFM computation"""
        current_company = self.env.company
        # partners = self.search([('customer_rank', '>', 0),
        #                         ('company_id', '=', current_company.id)])
        partners = self.search([
            '&',
            ('customer_rank', '>', 0),
            '|',
            ('company_id', '=', current_company.id),
            ('company_id', '=', False)
        ])

        _logger.info(
            "RFM Cron started: %s partners found for company %s", len(partners), current_company.name
        )

        if not partners:
            return
        partners.compute_rfm()
        _logger.info("RFM Cron completed successfully")
