# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AffiliationConfiguration(models.Model):
    _name = 'affiliation.affiliation_configuration'
    _description = 'Configuration of Affiliaton module'

    name = fields.Char(string='Name', compute='_compute_name')
    affiliation_number_edition = fields.Boolean(string='Allow editing affiliation number on start affiliation view.', default=False)
    next_affiliation_number = fields.Integer(string='Next affiliation number on sequence')
    enable_affiliation_number_sequence = fields.Boolean(string='Enable affiliation number sequence', default=True)
    affiliation_start = fields.Selection(
        selection=[
            ('on_affiliate', 'On affiliate'),
            ('on_confirm', 'On confirm affiliation'),
        ],
        string='Set init of affiliation',
        default='on_confirm'
    )
    set_disaffiliation_date = fields.Selection(
        selection=[
            ('on_disaffiliate', 'On disaffiliate'),
            ('on_confirm', 'On confirm disaffiliation'),
        ],
        string='Set end of affiliation',
        default='on_confirm'
    )

    def write(self, vals):
        if 'next_affiliation_number' in vals:
            _seq = self.env['ir.sequence'].search(
                [('code', '=', 'next_affiliation_number_seq')])
            _seq.number_next_actual = vals['next_affiliation_number']
        res = super(AffiliationConfiguration, self).write(vals)
        return res

# This method was added so that the breadcrumb does not appear as "affiliation.affiliation_configuration,1"
# and is translated according to the user's language
    @api.depends_context('lang')
    def _compute_name(self):
        for record in self:
            if self.env.user.lang and self.env.user.lang.startswith('es'):
                record.name = 'Configuración'
            else:
                record.name = 'Configuration'
