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
import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class stock_picking(osv.Model):
    
    _inherit = "stock.picking"
    
    SORT_VRSTE = (('name_az','Po nazivu (A->Z)'),
                  ('name_za','Po nazivu (Z->A)'),
                  ('seq','Ručno postavljeni redosljed (snimiti prije ispisa)'),
                  ('def','Redosljed upisivanja stavaka'))
    
    _columns = {
                'sort_print':fields.selection(SORT_VRSTE,'Redosljed stavaka pri ispisu',
                                              help="Ostaviti prazno za ispis po redosljedu upisa stavaka ili izabrati željeni redosljed")
                }
    
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        """
        if uid != 1:
            frozen_fields = set(['product_qty', 'product_uom', 'product_uos_qty', 'product_uos', 'location_id', 'location_dest_id', 'product_id'])
            for move in self.browse(cr, uid, ids, context=context):
                if move.state == 'done':
                    if frozen_fields.intersection(vals):
                        raise osv.except_osv(_('Operation Forbidden!'),
                                             _('Quantities, Units of Measure, Products and Locations cannot be modified on stock moves that have already been processed (except by the Administrator).'))
        
        Izbacio da ne jebe mirkeca.. inače ne dirati!
        """
        
        
        return  super(stock_move, self).write(cr, uid, ids, vals, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
