from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class LibraryPortal(CustomerPortal):

    @http.route(
        ['/my/library/loans', '/my/library/loans/'],
        type='http',
        auth='user',
        website=True,
        sitemap=False,
    )
    def portal_my_loans(self, **kw):
        partner = request.env.user.partner_id
        loans = request.env['library.loan'].sudo().search([
            ('member_id', '=', partner.id),
        ])
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
        if loan.member_id == request.env.user.partner_id and loan.state == 'active':
            loan.sudo().action_renew_loan()
        return request.redirect('/my/library/loans')