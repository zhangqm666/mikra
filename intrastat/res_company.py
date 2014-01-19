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


class res_company(osv.Model):
    _inherit = 'res.company'
    _columns = {
                'def_transaction_type':fields.many2one('intrastat.transaction.type','Transaction type', 
                        help='Default transaction type for purchase and sales order, Important if you need intrastat reports')
                }
    
    def ajde_popravi(self, cr, uid, ids, context=None):
        #ovo samo da popravim krive unose i mičem odavde... ne koristiti 
        po_obj = self.pool.get('purchase.order')
        
        po_ids = po_obj.search(cr, uid, [])
        for po in po_obj.browse(cr, uid, po_ids):
            amount = 0
            if po.partner_id.country_id.code != 'HR':
                if po.pricelist_id.id != 12 or po.amount_total ==0:
                    for pol in po.order_line:
                        pol.write({'price_unit':pol.product_id.nabavna_eur})
                    po_vals = {'pricelist_id':12}
                    po.write(po_vals)
        
        acc = self.pool.get('account.invoice')
        acc_ids = acc.search(cr, uid, [('type','=','in_invoice')])
        for ac in acc.browse(cr, uid, acc_ids):
            amount = 0
            if ac.partner_id.country_id.code != 'HR':
                if ac.currency_id != 1 or ac.amount_total == 0:
                    for line in ac.invoice_line:
                        line.write({'price_unit':line.product_id.nabavna_eur})
                    ac.write({'currency_id':1})
        return True