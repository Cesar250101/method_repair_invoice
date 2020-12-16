# -*- coding: utf-8 -*-
from odoo import http

# class MethodRepairInvoice(http.Controller):
#     @http.route('/method_repair_invoice/method_repair_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_repair_invoice/method_repair_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_repair_invoice.listing', {
#             'root': '/method_repair_invoice/method_repair_invoice',
#             'objects': http.request.env['method_repair_invoice.method_repair_invoice'].search([]),
#         })

#     @http.route('/method_repair_invoice/method_repair_invoice/objects/<model("method_repair_invoice.method_repair_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_repair_invoice.object', {
#             'object': obj
#         })