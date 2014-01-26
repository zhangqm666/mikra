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

class account_dep_cost(osv.TransientModel):
    _name = "account.dep.cost"
    _description = "Calculate dependency cost"
    
    _columns = {
                'invoice_id':fields.many2one('account.invoice','Invoice'),
                'cost_type':fields.selection([('manual','Manual distribute'),
                                              ('qty','By quantity'),
                                              ('price','By price'),
                                              ('weight','By weight')],'Dep.cost calculation'),
                #This goes for EUR as base currency, so i take rate for HRK id=30
                'currency_rate':fields.many2one('res.currency.rate','Currency rate',),
                'curr_rate_amount':fields.related('currency_rate','rate',type="float", digits=(16,6), string='Rate factor', readonly=True),
                'cost_lines':fields.one2many('account.dep.cost.cost','dep_cost_id','Costs'),
                'prod_lines':fields.one2many('account.dep.cost.prod','dep_cost_id','Products'),
                'total_cost':fields.float('Cost total', digits=(16,2)),
                'total_price':fields.float('Price total', digits=(16,2)),
                'total_depc':fields.float('Dep.cost total', digits=(16,2)),
                'total_weight':fields.float('Total product weight', digits=(16,3)),
                'total_pcs':fields.float('Total quantity', digits=(16,2)),
                'show_curr':fields.boolean('Show currency rate'),
                }

    _defaults = {
                 'cost_type':'manual',
                 'invoice_id':lambda self, cr, uid, c: c.get('active_id',False),
                 'currency_rate': lambda self, cr, uid, c: self.pool.get('res.currency.rate').search(cr, uid, [('currency_id','=',30)])[0]
                 }
    
    def write_changes(self, cr, uid , ids, context=None):
        calculator = self.browse(cr, uid, ids[0])
        for p in calculator.prod_lines:
            p.prod_line.write({'dep_cost_amount':p.cost_amount})
        calculator.invoice_id.write({'dep_cost_type':calculator.cost_type})
        return True
    
    def onchange_calculate(self, cr, uid, ids, cost_type=None, context=None):
        calculator = self.browse(cr, uid, ids[0])
        if cost_type == None or cost_type == 'manual' or len(calculator.prod_lines)==0:
            return False
        prod_list = []
        if cost_type == 'qty':    
            for p in calculator.prod_lines:
                prod_list.append((1,p.id,{'cost_amount':calculator.total_cost / calculator.total_pcs}))
        elif cost_type == 'price':
            for p in calculator.prod_lines:
                prod_list.append((1,p.id,{'cost_amount':calculator.total_cost * p.prod_hrk / calculator.total_price}))
        elif cost_type == 'weight':
            if calculator.total_weight==0:self.raise_zero_division()
            for p in calculator.prod_lines:
                if p.weight_net == 0:self.raise_zero_division()
                prod_list.append((1,p.id,{'cost_amount':calculator.total_cost * p.weight_net / calculator.total_weight}))
        return {'value':{'prod_lines':prod_list}}
           
    def raise_zero_division(self):
        raise osv.except_osv('Error!','Dividing with zero value not possible!\n At least one of products has zero net_weight')
    
    def populate_lines(self, cr, uid, ids, context=None):
        calculator = self.browse(cr, uid, ids[0])
        invoice = calculator.invoice_id
        #prep
        show_curr = True
        tot_cost = tot_weight = tot_pcs = tot_price = 0
        cur_rate = calculator.currency_rate.rate
        #1. get costs
        cost_list = []
        if len(calculator.cost_lines) !=0:
            for line in calculator.cost_lines:
                cost_list.append((2,line.id))
        for c in invoice.dep_cost:
            if c.invoice_id.currency_id.id == 30:
                show_curr = False
                cur_rate = 1.00
            cost_vals = {
                         'cost_line':c.id,
                         'cost_name':c.product_id.name,
                         'cost_qty':c.quantity,
                         'cost_subtotal':c.price_subtotal,
                         'cost_currency':c.invoice_id.currency_id.id,
                         'cost_hrk':c.price_subtotal * cur_rate
                         }
            tot_cost += c.price_subtotal * cur_rate
            cost_list.append((0,0,cost_vals))
        #2. get product data
        prod_list = []
        if len(calculator.prod_lines) !=0:
            for line in calculator.prod_lines:
                prod_list.append((2,line.id))
        for p in invoice.invoice_line:
            if p.invoice_id.currency_id.id == 30:
                show_curr = False
                cur_rate = 1.00
            prod_vals = {
                         'prod_line':p.id,
                         'prod_name':p.product_id.name,
                         'prod_weight':p.product_id.weight_net,
                         'prod_qty':p.quantity,
                         'prod_subtotal':p.price_subtotal,
                         'prod_currency':p.invoice_id.currency_id.id,
                         'prod_hrk': p.price_subtotal * cur_rate,
                         'prod_hrk_kom': p.price_subtotal * cur_rate / p.quantity
                         }
            if not p.product_id.is_accessory_cost:
                tot_price += p.price_subtotal * cur_rate
                tot_pcs += p.quantity
                tot_weight += p.product_id.weight_net
                prod_list.append((0,0,prod_vals))
        
        self.write(cr, uid, ids[0], {'cost_lines':cost_list,
                                     'prod_lines':prod_list,
                                     'total_cost':tot_cost,
                                     'total_weight':tot_weight,
                                     'total_price':tot_price,
                                     'total_pcs':tot_pcs,
                                     'show_curr':show_curr})
        
        return self.refresh_current_view(cr, uid, ids, context)
    
   
    
    def refresh_current_view(self, cr, uid, ids, context=None):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_dependant_cost', 'account_invoice_dep_cost_calculation')
        view_id = view_ref and view_ref[1] or False,
        return {
                'type': 'ir.actions.act_window',
                'name': 'Zavisni troškovi',
                'res_model': 'account.dep.cost',
                'res_id':ids[0],
                'view_type': 'form',
                'view_mode': 'form',
                'auto_refresh':1,
                'view_id': view_id,
                'target': 'new',
                'nodestroy': True,
                }
    
class account_dep_cost_cost(osv.TransientModel):
    _name = 'account.dep.cost.cost'
    _description = 'Costs for calculation'
    _columns = {
                'dep_cost_id':fields.many2one('account.dep.cost','Cost'),
                'cost_line':fields.integer('Line ID'),#fields.many2one('account.invoice.line','Cost'),
                'cost_name':fields.char('Cost product',size=256),
                'cost_qty':fields.float('Qty'),
                'cost_subtotal':fields.float('Price'),
                'cost_currency':fields.many2one('res.currency','Currency'),
                'cost_hrk':fields.float('Price HRK', digits=(16,2))           
                }
    
class account_dep_cost_prod(osv.TransientModel):
    _name = 'account.dep.cost.prod'
    _description = 'Products for calculation'
    _columns = {
                'dep_cost_id':fields.many2one('account.dep.cost','Product'),
                'prod_line':fields.many2one('account.invoice.line','Product'),
                'prod_name':fields.char('Cost product',size=256),
                'prod_qty':fields.float('Qty'),
                'prod_weight':fields.float('Weight/Pc'),
                'prod_subtotal':fields.float('Price line',help="Subtotal of invoice line"),
                'prod_currency':fields.many2one('res.currency','Currency'),
                'prod_hrk':fields.float('Price HRK', digits=(16,2)),
                'prod_hrk_kom':fields.float('Price HRK/pc', digits=(16,2)),
                'cost_amount':fields.float('Dependant cost', digits=(16,2))
                
                }