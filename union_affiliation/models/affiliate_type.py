# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
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
        other = self.search(filter)
        if len(other.ids):
            raise ValidationError(_('There is already exist a type with the same name!'))

    @api.model
    def load(self, fields, data):
        """Override para hacer upsert por la clave natural ``name``.

        Si una fila importada tiene un ``name`` que coincide con un registro
        existente, se inyecta el External ID del existente para que Odoo
        actualice (en vez de fallar contra el constraint de unicidad).
        Las filas se reportan como warnings en el preview de "Probar".
        """
        if 'name' not in fields or 'id' in fields:
            return super().load(fields, data)

        name_idx = fields.index('name')
        IMD = self.env['ir.model.data']
        new_fields = ['id'] + list(fields)
        new_data = []
        warnings_msgs = []

        for row_idx, row in enumerate(data, start=2):  # fila 1 = header
            name = row[name_idx]
            if not name:
                new_data.append(['', *row])
                continue

            existing = self.search([('name', '=', name)], limit=1)
            if not existing:
                new_data.append(['', *row])
                continue

            imd = IMD.search([
                ('model', '=', self._name),
                ('res_id', '=', existing.id),
            ], limit=1)
            if imd:
                xml_id = f"{imd.module}.{imd.name}"
            else:
                ext_name = f'affiliate_type_{existing.id}'
                IMD.create({
                    'module': '__import__',
                    'name': ext_name,
                    'model': self._name,
                    'res_id': existing.id,
                })
                xml_id = f"__import__.{ext_name}"

            new_data.append([xml_id, *row])
            warnings_msgs.append({
                'type': 'warning',
                'message': _('Fila %(row)s: el tipo "%(name)s" ya existe — se actualizará en vez de crear uno nuevo.') % {
                    'row': row_idx,
                    'name': name,
                },
                'rows': {'from': row_idx - 1, 'to': row_idx - 1},
            })

        result = super().load(new_fields, new_data)
        if warnings_msgs:
            result.setdefault('messages', []).extend(warnings_msgs)
        return result
