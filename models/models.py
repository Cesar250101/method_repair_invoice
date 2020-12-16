# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class NewModule(models.Model):
    _inherit = 'mrp.repair'


    def action_repair_invoice_create(self):
        for repair in self:
            repair.action_invoice_create()
            repair.write({'state': 'done'})
        return True

    @api.multi
    def action_invoice_create(self, group=False):
        """ Creates invoice(s) for repair order.
        @param group: It is set to true when group invoice is to be generated.
        @return: Invoice Ids.
        """
        res = dict.fromkeys(self.ids, False)
        invoices_group = {}
        InvoiceLine = self.env['account.invoice.line']
        Invoice = self.env['account.invoice']
        for repair in self.filtered(lambda repair: repair.state not in ('draft', 'cancel') and not repair.invoice_id):
            if not repair.partner_id.id and not repair.partner_invoice_id.id:
                raise UserError(_('You have to select a Partner Invoice Address in the repair form!'))
            comment = repair.quotation_notes
            if repair.invoice_method != 'none':
                if group and repair.partner_invoice_id.id in invoices_group:
                    invoice = invoices_group[repair.partner_invoice_id.id]
                    invoice.write({
                        'name': invoice.name + ', ' + repair.name,
                        'origin': invoice.origin + ', ' + repair.name,
                        'comment': (comment and (invoice.comment and invoice.comment + "\n" + comment or comment)) or (invoice.comment and invoice.comment or ''),
                    })
                else:
                    if not repair.partner_id.property_account_receivable_id:
                        raise UserError(_('No account defined for partner "%s".') % repair.partner_id.name)
                    invoice = Invoice.create({
                        'name': repair.name,
                        'origin': repair.name,
                        'type': 'out_invoice',
                        'account_id': repair.partner_id.property_account_receivable_id.id,
                        'partner_id': repair.partner_invoice_id.id or repair.partner_id.id,
                        'currency_id': repair.pricelist_id.currency_id.id,
                        'comment': repair.quotation_notes,
                        'fiscal_position_id': repair.partner_id.property_account_position_id.id
                    })
                    invoices_group[repair.partner_invoice_id.id] = invoice
                repair.write({'invoiced': True, 'invoice_id': invoice.id})

                for operation in repair.operations:
                    if operation.type == 'add':
                        if group:
                            name = repair.name + '-' + operation.name
                        else:
                            name = operation.name

                        if operation.product_id.property_account_income_id:
                            account_id = operation.product_id.property_account_income_id.id
                        elif operation.product_id.categ_id.property_account_income_categ_id:
                            account_id = operation.product_id.categ_id.property_account_income_categ_id.id
                        else:
                            raise UserError(_('No account defined for product "%s".') % operation.product_id.name)

                        invoice_line = InvoiceLine.create({
                            'invoice_id': invoice.id,
                            'name': name,
                            'origin': repair.name,
                            'account_id': account_id,
                            'quantity': operation.product_uom_qty,
                            'invoice_line_tax_ids': [(6, 0, [x.id for x in operation.tax_id])],
                            'uom_id': operation.product_uom.id,
                            'price_unit': operation.price_unit,
                            'price_subtotal': operation.product_uom_qty * operation.price_unit,
                            'product_id': operation.product_id and operation.product_id.id or False
                        })
                        operation.write({'invoiced': True, 'invoice_line_id': invoice_line.id})
                for fee in repair.fees_lines:
                    if group:
                        name = repair.name + '-' + fee.name
                    else:
                        name = fee.name
                    if not fee.product_id:
                        raise UserError(_('No product defined on Fees!'))

                    if fee.product_id.property_account_income_id:
                        account_id = fee.product_id.property_account_income_id.id
                    elif fee.product_id.categ_id.property_account_income_categ_id:
                        account_id = fee.product_id.categ_id.property_account_income_categ_id.id
                    else:
                        raise UserError(_('No account defined for product "%s".') % fee.product_id.name)

                    invoice_line = InvoiceLine.create({
                        'invoice_id': invoice.id,
                        'name': name,
                        'origin': repair.name,
                        'account_id': account_id,
                        'quantity': fee.product_uom_qty,
                        'invoice_line_tax_ids': [(6, 0, [x.id for x in fee.tax_id])],
                        'uom_id': fee.product_uom.id,
                        'product_id': fee.product_id and fee.product_id.id or False,
                        'price_unit': fee.price_unit,
                        'price_subtotal': fee.product_uom_qty * fee.price_unit
                    })
                    fee.write({'invoiced': True, 'invoice_line_id': invoice_line.id})
                invoice.compute_taxes()
                res[repair.id] = invoice.id
        return res
