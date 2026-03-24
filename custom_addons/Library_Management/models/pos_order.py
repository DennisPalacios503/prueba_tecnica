from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _process_order(self, order, draft, existing_order):
        res = super()._process_order(order, draft, existing_order)
        order_obj = self.browse(res)
        
        for line in order_obj.lines:
            # Buscar si el producto vendido es un libro
            book = self.env['library.book'].search([('product_id', '=', line.product_id.id)], limit=1)
            if book:
                # Crear el préstamo automáticamente
                self.env['library.loan'].create({
                    'book_id': book.id,
                    'member_id': order_obj.partner_id.id,
                    'loan_date': fields.Date.today(),
                    'state': 'active',
                })
        return res