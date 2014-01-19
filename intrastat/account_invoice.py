# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 DAJ MI 5 (<http://www.dajmi5.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
from tools.sql import drop_view_if_exists
from decimal_precision import decimal_precision as dp
import time

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    
    _columns = {
                'incoterm':fields.many2one('stock.incoterms','Incoterm'),
                'dep_cost':fields.many2many('product.product','product_invoice_rel','dep_cost','invoice_ids','Dependant cost')
                }