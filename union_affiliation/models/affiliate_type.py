# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AffiliateType(models.Model):
    _name = 'affiliation.affiliate_type'
    _description = 'Union affiliate\'s type entity'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True)
    enabled = fields.Boolean(string='Enabled', default=True)

    @api.constrains('name')
    def _check_name(self):
        filter = [('name','=',self.name)]
        if self.id:
            filter.append(('id','!=', self.id))
        other = self.env['affiliation.affiliate_type'].search(filter)
        if len(other.ids):
            raise ValidationError(_('There is already exist a type with the same name!'))
