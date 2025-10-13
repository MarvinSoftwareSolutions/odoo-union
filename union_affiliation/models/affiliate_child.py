# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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
    affiliate_names = fields.Char(
        string="Parents",
        compute="_compute_affiliate_names",
        store=False
    )
    educational_level = fields.Selection(
        selection=[
            ('none', 'Ninguno'),
            ('jardin', 'Jardín (4 y 5 años)'),
            ('primaria_1_3', '1º a 3º grado'),
            ('primaria_4_6', '4º a 6º grado'),
            ('secundaria', 'Secundaria'),
            ('mayor', 'Mayor (finalizado o no aplica)')
        ],
        string='Nivel educativo',
        tracking=True
    )


    @api.constrains('affiliate_ids')
    def _check_has_affiliate(self):
        for child in self:
            if not child.affiliate_ids:
                raise ValidationError(('Each child must be linked to at least one affiliate.'))


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = ['|',('personal_id', operator, name),('name', operator, name)]
        recs = self.search(domain + args, limit=limit)
        return recs.name_get()


    @api.depends('affiliate_ids.name')
    def _compute_affiliate_names(self):
        for record in self:
            record.affiliate_names = ', '.join(record.affiliate_ids.mapped('name'))