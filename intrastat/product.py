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
        'intrastat_id': fields.many2one('intrastat.code', 'Intrastat code'),
        'country_origin':fields.many2one('res.country','Country origin', help="Country where product is produced"),
        'is_accessory_cost': fields.boolean('Is accessory cost', help='Activate this option for shipping costs, packaging costs and all services related to the sale of products. This option is used for Intrastat reports.'),
                }
    
    def _check_accessory_cost(self, cr, uid, ids):
        for product in self.browse(cr, uid, ids):
            if product.is_accessory_cost and product.type != 'service':
                raise osv.except_osv(_('Error :'), _("The option 'Is accessory cost?' should only be activated on 'Service' products. You have activated this option for the product '%s' which is of type '%s'" % (product.name, product.type)))
        return True

    _constraints = [
        (_check_accessory_cost, "Error msg is in raise", ['is_accessory_cost', 'type'])
        ]

class product_product(osv.Model):
    _inherit = 'product.product'
    
    _columns = {
                'invoice_ids':fields.many2many('account.invoice','product_invoice_rel','invoice_ids','dep_cost','For invoices')
                }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
