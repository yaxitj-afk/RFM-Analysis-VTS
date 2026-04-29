from odoo import models, fields

class RFMRule(models.Model):
    _name = 'rfm.rule'
    _description = 'RFM Scoring Rule'
    _order = 'metric, sequence'

    name = fields.Char(required=True)
    metric = fields.Selection([
        ('recency', 'Recency'),
        ('frequency', 'Frequency'),
        ('monetary', 'Monetary'),
    ], required=True)

    value_from = fields.Float(required=True)
    value_to = fields.Float(required=True)
    score = fields.Integer(required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    partner_category_ids = fields.Many2many(
        'res.partner.category',
        string="Customer Tags",
        help="Define rules based on customer tags"
    )


