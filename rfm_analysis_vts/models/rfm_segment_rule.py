from odoo import models, fields


class RFMSegmentRule(models.Model):
    _name = 'rfm.segment.rule'
    _description = 'RFM Segment Rule'
    _order = 'sequence,id'

    name = fields.Char(required=True)

    recency_min = fields.Integer(string="Recency Min", required=True)
    frequency_min = fields.Integer(string="Frequency Min", required=True)
    monetary_min = fields.Integer(string="Monetary Min", required=True)
    segment_id = fields.Many2one(string="Segment", comodel_name='rfm.segments', copy=False)
    sequence = fields.Integer(string="Sequence", default=10,index=True)
    active = fields.Boolean(string="Active", default=True)

