from odoo import models, fields, api


class LibraryMember(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean(
        string='Es Socio de Biblioteca',
        default=False,
    )

    library_member_code = fields.Char(
        string='Código de Socio',
        readonly=True,
        copy=False,
        index=True,
    )

    library_membership_date = fields.Date(
        string='Fecha de Alta',
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_library_member'):
                vals['library_member_code'] = self.env['ir.sequence'].next_by_code(
                    'library.member.sequence'
                ) or '/'
                vals['library_membership_date'] = fields.Date.today()
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('is_library_member'):
            for record in self:
                if not record.library_member_code:
                    vals['library_member_code'] = self.env['ir.sequence'].next_by_code(
                        'library.member.sequence'
                    ) or '/'
                    vals['library_membership_date'] = fields.Date.today()
        return super().write(vals)