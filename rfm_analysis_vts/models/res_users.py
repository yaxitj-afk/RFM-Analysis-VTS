import logging
from odoo import models, fields, api

_logger = logging.getLogger("RFM")
class ResUsers(models.Model):
    _inherit = 'res.users'

    # def write(self, vals):
    #     res = super().write(vals)
    #     if 'company_id' in vals:
    #         # Company changed, trigger RFM for that company
    #         _logger.info('Writing to company %s', vals['company_id'])
    #         self.env['res.partner']._trigger_rfm_for_current_company()
    #     return res

    # def write(self, vals):
    #     run_cron = False
    #     print("Write method called")
    #     if 'company_id' in vals or 'company_ids' in vals:
    #         run_cron = True
    #
    #     res = super(ResUsers,self).write(vals)
    #
    #     if run_cron:
    #         print("Write method called and come inside run cron condition")
    #         self._run_company_switch_cron()
    #
    #     return res

    # def _run_company_switch_cron(self):
    #     print("_run_company_switch_cron called")
    #     cron = self.env.ref(
    #         'rfm_analysis_vts.ir_cron_rfm_compute',
    #         raise_if_not_found=False
    #     )
    #     if cron:
    #         cron.sudo().method_direct_trigger()

