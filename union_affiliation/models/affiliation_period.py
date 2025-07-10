# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AffiliationPeriod(models.Model):
    _name = 'affiliation.affiliation_period'
    _description = 'Affiliation period entity'
    _order = 'from_date desc'

    affiliation_number = fields.Integer(string='Affiliation number', required=True)
    from_date = fields.Datetime(string='From', required=True)
    to_date = fields.Datetime(string='To')
    closed = fields.Boolean(string='Closed', default=False)
    affiliate_id = fields.Many2one(
        comodel_name='affiliation.affiliate',
        string='Affiliate',
        required=True,
        ondelete='cascade'
    )
    affiliate_state = fields.Selection(related='affiliate_id.state', store=False)
    disaffiliation_reason = fields.Char(string="Motivo de desafiliación")

    @api.constrains('from_date','to_date')
    def _check_dates(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError(_('\'From date\' is major to \'to date\'!'))

    @api.constrains('affiliation_number')
    def _check_affiliation_number(self):
        other = self.env['affiliation.affiliation_period'].search([('affiliation_number','=',self.affiliation_number)])
        if len(other.ids) > 1 or (other[0].id != self.id):
            raise ValidationError(_('There is already exist a period with the same affiliation number!'))

    @api.constrains('from_date')
    def _check_from_date(self):
        for record in self:
            if not record.from_date or not record.affiliate_id:
                continue
            overlaps = self.env['affiliation.affiliation_period'].search([
                ('affiliate_id', '=', record.affiliate_id.id),
                ('id', '!=', record.id),
                ('from_date', '<=', record.from_date),
                ('to_date', '>=', record.from_date),
            ])
            if overlaps:
                raise ValidationError(_('Period\'s start date overlaps with another period.'))


    @api.constrains('to_date')
    def _check_to_date(self):
        for record in self:
            if not record.to_date or not record.affiliate_id:
                continue
            overlaps = self.env['affiliation.affiliation_period'].search([
                ('affiliate_id', '=', record.affiliate_id.id), 
                ('id', '!=', record.id),
                ('from_date', '<=', record.to_date),
                ('to_date', '>=', record.to_date),
            ])
            if overlaps:
                raise ValidationError(_('Period\'s end date overlaps with another period.'))


    # @api.depends('to_date')
    # def _compute_closed(self):
    #     for record in self:
    #         if record.to_date:
    #             record.closed = True
    #             return
    #         record.closed = False

    def _are_any_open(self, affiliate_id):
        period = self.env['affiliation.affiliation_period'].search([('affiliate_id','=',affiliate_id),('closed','=',False)])
        if len(period.ids):
            return True
        return False

    @api.model
    def create(self, vals):
        _affiliate_id = vals.get('affiliate_id') or self.env.context.get('default_affiliate_id')
        if not _affiliate_id:
            raise ValidationError(_('Affiliate ID is required'))
        if self._are_any_open(_affiliate_id):
            raise ValidationError(_('There is already an open period!'))
        res = super(AffiliationPeriod, self).create(vals)
        # affiliate = res.affiliate_id
        # affiliate.affiliate_()
        return res

    def write(self, vals) :
        if self.closed:
            raise ValidationError(_('You can\'t edit a closed period!'))
        res = super(AffiliationPeriod, self).write(vals)
        return res

    def close(self, date):
        self.write({'to_date': date, 'closed': True})
