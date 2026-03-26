# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, exceptions

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _process_order(self, *args, **kwargs):
        # Al usar *args y **kwargs, aceptamos 3, 4 o 10 argumentos sin fallar
        res = super(PosOrder, self)._process_order(*args, **kwargs)
        
        order_id = res[0] if isinstance(res, (list, tuple)) else res
        order_obj = self.browse(order_id)

        for line in order_obj.lines:
            book = self.env['library.book'].sudo().search(
                [('product_id', '=', line.product_id.id)], limit=1
            )
            if book:
                if not book.is_available:
                    raise exceptions.ValidationError(_("El libro '%s' no está disponible.") % book.name)
                
                if order_obj.partner_id:
                    self.env['library.loan'].sudo().create({
                        'book_id': book.id,
                        'member_id': order_obj.partner_id.id,
                        'loan_date': fields.Date.today(),
                        'state': 'active',
                    })
                    book.sudo().write({'is_available': False})
        return res