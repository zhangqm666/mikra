# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Module: mikra_co
#    Author: Davor Bojkić
#    mail:   bole@dajmi5.com
#    Copyright (C) 2012- Daj Mi 5, 
#                  http://www.dajmi5.com
#    Contributions: 
#                   
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


import time
from openerp.report import report_sxw

from netsvc import Service
#del Service._services['report.account.invoice']

class sale_order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'show_discount':self._show_discount,
            'sort_by_name':self._sort_by_name,
            'sortiraj':self._sortiraj
            
        })
        
    def _show_discount(self, uid, context=None):
        cr = self.cr
        try: 
            group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'group_discount_per_so_line')[1]
        except:
            return False
        return group_id in [x.id for x in self.pool.get('res.users').browse(cr, uid, uid, context=context).groups_id]
    
    def _sort_by_name(self, theList):
        theList.sort(key=lambda x: x.name, reverse=False)
        return theList
    
    def _sortiraj(self, theList, order_by=None):
        
        if not order_by or order_by == 'def':
            return theList
        
        if order_by == 'name_az':
            theList.sort(key=lambda x: x.name, reverse=False)
        elif order_by == "name_za":
            theList.sort(key=lambda x: x.name, reverse=True)
        elif order_by == 'seq':
            # TODO provjeri jel postoje seqvence.. kaj ako ih nema? 
            theList.sort(key=lambda x: x.sequence, reverse=True)
            pass
        
        return theList
        
    

report_sxw.report_sxw(
    'report.mikra.sale.order',
    'sale.order',
    'addons/mikra_co/report/sale_order.rml',
    parser=sale_order
)