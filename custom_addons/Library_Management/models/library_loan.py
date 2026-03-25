# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Préstamo de Libros'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    book_id = fields.Many2one(
        'library.book', string='Libro', required=True,
        domain=[('is_available', '=', True)], tracking=True,
    )
    member_id = fields.Many2one(
        'res.partner', string='Socio', required=True,
        domain=[('is_library_member', '=', True)], tracking=True,
    )
    loan_date = fields.Date(
        string='Fecha de Préstamo',
        default=fields.Date.today,
        readonly=True,
    )
    return_date = fields.Date(string='Fecha de Devolución', readonly=True)
    state = fields.Selection([
        ('active', 'Activo'),
        ('returned', 'Devuelto'),
        ('overdue', 'Vencido'),
    ], string='Estado', default='active', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            book = self.env['library.book'].browse(vals.get('book_id'))
            if not book.is_available:
                raise ValidationError(_(
                    "El libro '%s' no está disponible para préstamo."
                ) % book.name)
            active_loans = self.search_count([
                ('member_id', '=', vals.get('member_id')),
                ('state', 'in', ['active', 'overdue']),
            ])
            if active_loans >= 5:
                raise ValidationError(_(
                    "El socio ya tiene 5 préstamos activos. "
                    "Debe devolver un libro antes de realizar un nuevo préstamo."
                ))
            book.is_available = False
        return super().create(vals_list)

    def action_return_book(self):
        for record in self:
            record.book_id.is_available = True
            record.write({
                'state': 'returned',
                'return_date': fields.Date.today(),
            })

    def action_renew_loan(self):
        self.ensure_one()
        if self.state == 'overdue':
            raise ValidationError(_("No se puede renovar un préstamo vencido."))
        self.loan_date = fields.Date.today()

    @api.model
    def _cron_check_overdue_loans(self):
        limit_date = fields.Date.today() - timedelta(days=30)
        overdue_loans = self.search([
            ('state', '=', 'active'),
            ('loan_date', '<', limit_date),
        ])
        template = self.env.ref(
            'library_management.email_template_loan_overdue',
            raise_if_not_found=False,
        )
        for loan in overdue_loans:
            loan.state = 'overdue'
            if template:
                template.send_mail(loan.id, force_send=True)