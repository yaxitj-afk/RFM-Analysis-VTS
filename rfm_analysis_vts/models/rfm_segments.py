from odoo import models, fields, api


class RFMSegments(models.Model):
    _name = 'rfm.segments'
    _description = 'RFM Segment'
    _order = 'sequence, id'

    name = fields.Char(string="RFM Segment Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    active = fields.Boolean(string="Active", default=True)

    @api.model
    def create(self, vals):
        segment = super().create(vals)
        # Create dashboard record automatically
        self.env['rfm.segment.dashboard'].create({
            'segment_id': segment.id
        })
        return segment
