# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AffiliateChild(models.Model):
    _name = 'affiliation.affiliate_child'
    _description = 'Union affiliate\'s child entity'

    name = fields.Char(string='Name', required=True)
    personal_id_type = fields.Selection([
        ('dni', 'DNI'), 
        ('lc', 'LC'), 
        ('le', 'LE'),
        ('pasaporte', 'PASAPORTE'), 
        ('ci', 'CI')],
        string='Personal ID type', default='dni', required=True)
    personal_id = fields.Char(string='Personal ID', required=True)
    birth_date = fields.Date(string='Birth date')
    handicapped = fields.Boolean(string='Handicapped', default=False)
    verified = fields.Boolean(string='Verified', default=False)
    observation = fields.Char(string='Observations')
    affiliate_ids = fields.Many2many(
        comodel_name='affiliation.affiliate',
        relation='affiliate_affiliate_child',
        column1='affiliate_child_id',
        column2='affiliate_id',
        string='Parents'
    )

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = ['|',('personal_id', operator, name),('name', operator, name)]
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()
