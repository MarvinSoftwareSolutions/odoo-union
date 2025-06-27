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
        if self.affiliation_number == 0:
                raise ValidationError(_("Affiliation number cannot be 0."))

        # write affiliation data
        _to_write = {'affiliation_number': self.affiliation_number }
        fields = ['state', 'quote', 'affiliation_date', 'disaffiliation_date']
        for field in fields:
            if self.env.context.get(field):
                _to_write.update({field:self.env.context.get(field)})
        if self.affiliate_id.disaffiliation_date:
            _to_write.update({'disaffiliation_date': None})
        self.affiliate_id.write(_to_write)

        # increment next affiliation number sequence if it was used
        if self.enable_affiliation_number_sequence:
            _seq = self.env['ir.sequence'].search(
                    [('code', '=', 'next_affiliation_number_seq')])
            if self.affiliation_number == _seq.number_next_actual:
                next_affiliaton_number = int(self.env['ir.sequence'].next_by_code('next_affiliation_number_seq'))
                next_affiliaton_number = next_affiliaton_number + 1
                # update next affiliation number on configuration
                _to_write = {'next_affiliation_number': str(next_affiliaton_number)}
                _config = self.env['affiliation.affiliation_configuration'].browse(1)
                _config.write(_to_write)

        self.unlink()