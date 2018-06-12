# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class SaleReport(models.Model):
    _inherit = "sale.report"

    due_date = fields.Date('Due Date')
    product_desc = fields.Char('Product Desc')

    def _select(self):
        return super(SaleReport, self)._select() + ", l.due_date as due_date, l.name as product_desc"

    def _group_by(self):
        return super(SaleReport, self)._group_by() + ", l.due_date, l.name"

