from odoo import models, fields

class RFMLog(models.Model):
    _name = 'rfm.log'
    _description = 'RFM Log'

    order_date = fields.Datetime("Created On")
    partner_id = fields.Many2one('res.partner', string='Customer Name')
    old_segment_id = fields.Many2one('rfm.segments' ,string= "Old Segment", help="Customer segment before last order")
    new_segment_id = fields.Many2one('rfm.segments' ,string= "New Segment", help="Customer segment after last order")
