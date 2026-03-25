# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager



class LibraryPortal(CustomerPortal):

    import logging
    _logger = logging.getLogger(__name__)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        values['loan_count'] = request.env['library.loan'].sudo().search_count([
            ('member_id', '=', partner.id),
            ('state', '=', 'active'),
        ])
        return values

    @http.route(
        ['/my/library/loans'],
        type='http',
        auth='user',
        website=True,
        sitemap=False,
    )
    def portal_my_loans(self, **kw):
        partner = request.env.user.partner_id
        loans = request.env['library.loan'].sudo().search(
            [('member_id', '=', partner.id)]
        )
        return request.render(
            'library_management.portal_my_library_loans',
            {'loans': loans, 'page_name': 'my_loans'},
        )

    @http.route(
        ['/my/library/renew/<model("library.loan"):loan>'],
        type='http',
        auth='user',
        website=True,
        sitemap=False,
    )
    def portal_renew_loan(self, loan, **kw):
        if loan.member_id == request.env.user.partner_id and loan.state != 'overdue':
            loan.sudo().action_renew_loan()
        return request.redirect('/my/library/loans')