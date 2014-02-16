# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp.osv import osv
from openerp import pooler

class request_quotation(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(request_quotation, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'user': self.pool.get('res.users').browse(cr, uid, uid, context),
            'sort_by_name':self._sort_by_name,
            'sortiraj':self._sortiraj
        })
        
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
        
report_sxw.report_sxw('report.mikra.request.quotation',
                      'purchase.order',
                      'addons/mikra_co/report/request_quotation.rml',
                      parser=request_quotation)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

