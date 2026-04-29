from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class CompanySwitchHookController(http.Controller):

    @http.route('/company_switch/hook', type='json', auth='user')
    def company_switch_hook(self, company_ids):
        request.env['res.partner'].sudo().with_context(
            allowed_company_ids=company_ids,
            force_company=company_ids,
        )._cron_compute_rfm()
        return {'status': 'ok'}


