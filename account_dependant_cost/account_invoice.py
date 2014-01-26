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

class product_template(osv.osv):
    _name = "product.template"
    _inherit = "product.template"
    _columns = {
        'is_accessory_cost': fields.boolean('Is accessory cost', help='Activate this option for shipping costs, packaging costs and all services related to the sale of products. This option is used for Intrastat reports.'),
                }
    
    def _check_accessory_cost(self, cr, uid, ids):
        for product in self.browse(cr, uid, ids):
            if product.is_accessory_cost and product.type != 'service':
                raise osv.except_osv(_('Error :'), _("The option 'Is accessory cost?' should only be activated on 'Service' products. You have activated this option for the product '%s' which is of type '%s'" % (product.name, product.type)))
        return True

    _constraints = [
        (_check_accessory_cost, "Error !", ['is_accessory_cost', 'type'])
        ]

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    
    _columns = {
                
                'dep_cost':fields.many2many('account.invoice.line','invoice_dep_cost_rel','dep_cost','invoice_dep_ids','Dependant cost',
                                            help="Dependant cost lines in this or other invoice"),
                'dep_cost_type':fields.selection([('manual','Manual dist'),
                                                  ('qty','By quantity'),
                                                  ('price','By price'),
                                                  ('weight','By weight')],'Dep.cost calculation')
                }
    
    def dependant_cost_calculation(self, cr, uid, ids, context=None):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_dependant_cost', 'account_invoice_dep_cost_calculation')
        view_id = view_ref and view_ref[1] or False,
        return {
                'type': 'ir.actions.act_window',
                'name': 'Zavisni troškovi',
                'res_model': 'account.dep.cost',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'new',
                'nodestroy': True,
                }
    
class account_invoice_line(osv.Model):
    _inherit = 'account.invoice.line'
    
    _columns = {
                'invoice_dep_ids':fields.many2many('account.invoice','invoice_dep_cost_rel','invoice_dep_ids','dep_cost','For invoices',
                                                   help="Is depentant cost for these invoices"),
                'dep_cost_amount':fields.float('Amount of dep.cost',digits=(16,2), ),
                'is_accessory_cost':fields.related('product_id','is_accessory_cost',type="boolean", string="Is cost"),
                'weight_net':fields.related('product_id','weight_net', type="float", string="Weight netto"),
                'currency':fields.related('invoice_id','currency_id',type="many2one", relation="res.currency", string="Currency", readonly=True),
                
                }
    
