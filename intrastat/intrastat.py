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
from decimal_precision import decimal_precision as dp
import time


def default_transaction_type(self, cr, uid, context=None):
    """used in: purchase_order, stock_picking
    """
    #TODO : Multicompany! BB
    comp_default=self.pool.get('res.company').browse(cr, uid, 1).def_transaction_type.id
    tt_ids = self.pool.get('intrastat.transaction.type').search(cr, uid, [('code', '=', '11')])
    return comp_default and comp_default or tt_ids and tt_ids[0] or False    


class res_country(osv.osv):
    _name = 'res.country'
    _inherit = 'res.country'
    _columns = {
        'intrastat': fields.boolean('Intrastat member'),
    }
    


class intrastat_transaction_type(osv.osv):
    _name = "intrastat.transaction.type"
    _description = "Intrastat transaction types"
    
    def _concat_code_name(self, cr, uid, ids, fields, arg, context=None):
        res={}
        for codes in self.browse(cr,uid,ids,context=context):
            res[codes.id] = codes.code + ' ' + codes.short_name
        return res
        
    _columns = {
        'code': fields.char('Transaction Type Code', size=2, required=True),
        'short_name': fields.char('Short description', size=36, required=True),
        'name': fields.function(_concat_code_name, type='char', method=True, string='Description', store=True),
        'full_description': fields.text('Full Description'),
    }
    _order = "code"




class intrastat_code(osv.osv):
    _name = "intrastat.code"
    _description = "Intrastat code"
    _columns = {
        'name': fields.char('Intrastat Code', size=16),
        'description': fields.text('Description'),
    }
 
class delivery_carrier(osv.Model):
    _inherit  = "delivery.carrier"
    
    _VRSTE_PROMETA=[('1','Pomorski promet'),
                    ('2','Željeznički promet'),
                    ('3','Cestovni promet'),
                    ('4','Zračni promet'),
                    ('5','Poštanska pošiljka'),
                    ('6','Fiksne prometne instalacije'),
                    ('7','Promet kopnenim plovnim putevima'),
                    ('8','Vlastiti pogon')]
    
    _columns = {
                'vrsta':fields.selection(_VRSTE_PROMETA,'Vrsta prometa',help="Potrebno radi intrastat izvještaja", required="True")
                }
class product_template(osv.osv):
    _name = "product.template"
    _inherit = "product.template"
    _columns = {
        'intrastat_id': fields.many2one('intrastat.code', 'Intrastat code'),
        'country_origin':fields.many2one('res.country','Country origin', help="Country where product is produced"),
               }
 
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



class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    
    _columns = {
                'incoterm':fields.many2one('stock.incoterms','Incoterm'),            
                }
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
