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
from intrastat import default_transaction_type 


        

class purchase_order(osv.Model):
    
    _inherit = "purchase.order"
    _columns = {
        'transaction_type_id': fields.many2one('intrastat.transaction.type', 'Transaction type'),
        'incoterm':fields.many2one('stock.incoterms','Incoterm'),
                }
    
    _defaults = {
        'transaction_type_id': default_transaction_type,
                }            
    
    
        
    def _prepare_order_picking(self, cr, uid, order, context=None):
        res = super(purchase_order,self)._prepare_order_picking( cr, uid, order, context)
        res['transaction_type_id'] = order.transaction_type_id.id
        return res
    """
    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, context=None):
        res = super(purchase_order, self)._prepare_order_line_move(cr, uid, order, order_line, picking_id)
        res['country_origin_id'] = order_line.country_origin_id.id
        #res['customer_id'] = order_line.customer_id.id
        return res
    """


"""
class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _columns = {
        'country_origin_id': fields.many2one('res.country','Country of origin'),
        #'customer_id':fields.many2one('res.partner','Partner')
    }
    
    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, context=None):
        
        res = super(purchase_order_line, self).onchange_product_id(cr, uid, ids, 
                    pricelist_id, product_id, qty, uom_id, partner_id, date_order, 
                    fiscal_position_id, date_planned,
                    name, price_unit, context)
        country_origin = self.pool.get('res.partner').browse(cr, uid, partner_id).country_id.id
        res['value'].update({'country_origin_id': country_origin })
                             
        return res
        
purchase_order_line()
"""