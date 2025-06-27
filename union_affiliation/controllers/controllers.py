# -*- coding: utf-8 -*-
# from odoo import http


# class Afiliados(http.Controller):
#     @http.route('/afiliados/afiliados/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/afiliados/afiliados/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('afiliados.listing', {
#             'root': '/afiliados/afiliados',
#             'objects': http.request.env['afiliados.afiliados'].search([]),
#         })

#     @http.route('/afiliados/afiliados/objects/<model("afiliados.afiliados"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('afiliados.object', {
#             'object': obj
#         })
