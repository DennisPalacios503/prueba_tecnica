# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Libro de Biblioteca'

    name = fields.Char(string='Título', required=True)
    author = fields.Char(string='Autor', required=True)
    isbn = fields.Char(string='ISBN')
    publication_date = fields.Date(string='Fecha de Publicación')
    years_since_publication = fields.Integer(
        string='Años desde Publicación',
        compute='_compute_years_since_publication',
        store=False,
    )
    is_available = fields.Boolean(string='Disponible', default=True)
    loan_ids = fields.One2many('library.loan', 'book_id', string='Préstamos')
    loan_count = fields.Integer(
        string='Total Préstamos',
        compute='_compute_loan_count',
    )
    # Producto opcional para POS
    product_id = fields.Many2one(
        'product.product',
        string='Producto POS',
        help='Producto asociado para operar desde el Punto de Venta.',
    )

    @api.depends('publication_date')
    def _compute_years_since_publication(self):
        today = date.today()
        for record in self:
            if record.publication_date:
                record.years_since_publication = today.year - record.publication_date.year
            else:
                record.years_since_publication = 0

    @api.depends('loan_ids')
    def _compute_loan_count(self):
        for record in self:
            record.loan_count = len(record.loan_ids)

    def action_create_loan(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nuevo Préstamo',
            'res_model': 'library.loan',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_book_id': self.id},
        }

    def write(self, vals):
        res = super().write(vals)
        if 'product_id' in vals:
            for record in self:
                if record.product_id:
                    record.product_id.available_in_pos = True
        return res
    
    def action_view_loans(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Préstamos',
            'res_model': 'library.loan',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
        }