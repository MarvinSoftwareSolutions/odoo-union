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

    # ---------- CONSTRAINTS ----------
    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for rec in self:
            if rec.from_date and rec.to_date and rec.from_date > rec.to_date:
                raise ValidationError(_("The 'From date' is after the 'To date'."))

    @api.constrains('affiliation_number')
    def _check_affiliation_number(self):
        for rec in self:
            others = rec.search([
                ('affiliation_number', '=', rec.affiliation_number),
                ('id', '!=', rec.id),
            ])
            if others:
                raise ValidationError(_('There is already a period with the same affiliation number!'))

    @api.constrains('from_date')
    def _check_from_date_overlap(self):
        for rec in self:
            if not rec.from_date or not rec.affiliate_id:
                continue
            overlaps = rec.affiliate_id.affiliation_period_ids.filtered(
                lambda p: p.id != rec.id and
                          p.from_date <= rec.from_date <= (p.to_date or rec.from_date)
            )
            if overlaps:
                raise ValidationError(_("Period's start date overlaps with another period."))

    @api.constrains('to_date')
    def _check_to_date_overlap(self):
        for rec in self:
            if not rec.to_date or not rec.affiliate_id:
                continue
            overlaps = rec.affiliate_id.affiliation_period_ids.filtered(
                lambda p: p.id != rec.id and
                          p.from_date <= rec.to_date <= (p.to_date or rec.to_date)
            )
            if overlaps:
                raise ValidationError(_("Period's end date overlaps with another period."))

    # ---------- HELPERS ----------
    def _are_any_open(self, affiliate_id):
        affiliate = self.env['affiliation.affiliate'].browse(affiliate_id)
        return any(not period.closed for period in affiliate.affiliation_period_ids)

    # ---------- OVERRIDES ----------
    @api.model
    def create(self, vals):
        affiliate_id = vals.get('affiliate_id') or self.env.context.get('default_affiliate_id')
        if not affiliate_id:
            raise ValidationError(_('Affiliate ID is required'))

        if self._are_any_open(affiliate_id):
            raise ValidationError(_('There is already an open period!'))

        return super().create(vals)

    def write(self, vals):
        for rec in self:
            if rec.closed:
                raise ValidationError(_("You can't edit a closed period!"))
        return super().write(vals)

    # ---------- BUSINESS ----------
    def close(self, date):
        self.write({'to_date': date, 'closed': True})