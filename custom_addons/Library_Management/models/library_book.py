
from odoo import models, fields, api
from datetime import date


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Libro de Biblioteca'

    name = fields.Char(
        string='Título',
        required=True,
    )
    author = fields.Char(
        string='Autor',
        required=True,
    )
    isbn = fields.Char(
        string='ISBN',
    )
    publication_date = fields.Date(
        string='Fecha de Publicación',
    )
    years_since_publication = fields.Integer(
        string='Años desde Publicación',
        compute='_compute_years_since_publication',
        store=False,
    )
    is_available = fields.Boolean(
        string='Disponible',
        default=True,
    )

    @api.depends('publication_date')
    def _compute_years_since_publication(self):
        today = date.today()
        for record in self:
            if record.publication_date:
                record.years_since_publication = today.year - record.publication_date.year
            else:
                record.years_since_publication = 0

    product_id = fields.Many2one('product.product', string='Producto Relacionado', required=True)
    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Solo intentamos modificar el producto si realmente se envió un ID
            if vals.get('product_id'):
                product = self.env['product.product'].browse(vals['product_id'])
                if product.exists():
                    product.available_in_pos = True
        return super().create(vals_list)