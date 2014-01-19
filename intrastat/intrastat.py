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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
