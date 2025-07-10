# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AffiliationNumber(models.TransientModel):
    _name = 'affiliation.affiliation_number'
    _description = 'Model for Affiliation Number wizard'

    affiliate_id = fields.Many2one(
        comodel_name='affiliation.affiliate',
        string='Affiliate',
        required=True
    )
    affiliation_number = fields.Integer(string='Affiliation number')
    enable_affiliation_number_sequence = fields.Boolean(string='Enable affiliation number sequence', required=True)
    affiliation_number_edition = fields.Boolean(string='Allow editing affiliation number', required=True)

    def confirm(self):
        self.ensure_one()

        if self.affiliation_number == 0:
            raise ValidationError(_("Affiliation number cannot be 0."))

        # Actualizar datos del afiliado a través de método del modelo
        self.affiliate_id.confirm_affiliation_with_number(
            affiliation_number=self.affiliation_number,
            context_updates=self.env.context
        )

        # Incrementar la secuencia si fue usada
        if self.enable_affiliation_number_sequence:
            seq = self.env['ir.sequence'].search([('code', '=', 'next_affiliation_number_seq')], limit=1)
            if self.affiliation_number == seq.number_next_actual:
                # Incrementar dos veces porque la siguiente llamada a `next_by_code()` ya lo hace una vez
                self.env['ir.sequence'].next_by_code('next_affiliation_number_seq')
                seq.sudo().write({'number_next_actual': seq.number_next_actual + 1})

        self.unlink()
