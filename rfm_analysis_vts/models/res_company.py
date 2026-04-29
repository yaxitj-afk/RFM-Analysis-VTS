import logging
from odoo import models, fields, api
from contextlib import contextmanager


_logger = logging.getLogger("RFM")


class ResCompany(models.Model):
    _inherit = 'res.company'

    rfm_date_from = fields.Date(string="RFM Date From")
    rfm_date_to = fields.Date(string="RFM Date To")

    def write(self, vals):
        res = super().write(vals)
        if 'rfm_date_from' in vals or 'rfm_date_to' in vals:
            _logger.info("RFM date range changed triggering RFM cron for company %s", self.name)
            self.env['res.partner']._cron_compute_rfm()
        return res

    # @contextmanager
    # def switch_company(self, new_company_id):
    #     _logger.info("action switch company %s", new_company_id)
    #     result = super(ResCompany,self).switch_company(new_company_id)
    #     self.env['res.partner']._trigger_rfm_for_current_company()
    #     return result
