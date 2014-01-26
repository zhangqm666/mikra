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
from jinja2.testsuite import res
from datetime import datetime, time

_VRSTE_PROMETA=[('1','Pomorski promet'),
                ('2','Željeznički promet'),
                ('3','Cestovni promet'),
                ('4','Zračni promet'),
                ('5','Poštanska pošiljka'),
                ('6','Fiksne prometne instalacije'),
                ('7','Promet kopnenim plovnim putevima'),
                ('8','Vlastiti pogon')]

class stock_picking(osv.osv):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
   
    
    _columns = {
        'transaction_type_id': fields.many2one('intrastat.transaction.type', 'Transaction type'),
        'incoterm':fields.many2one('stock.incoterms','Incoterm'),
        'intrastat_exclude':fields.boolean('Exclude', help="Isključeno iz Intrastat izvještaja, ostavite isključeno unoliko niste sigurni što radite!"),
        'vrsta_prometa':fields.selection(_VRSTE_PROMETA,'Vrsta prometa',help="Potrebno radi intrastat izvještaja"),
               
    }
    _defaults = {
        'transaction_type_id': default_transaction_type
    }
    
class stock_picking_in(osv.osv):
    _inherit = 'stock.picking.in'
    _columns = {
        'transaction_type_id': fields.many2one('intrastat.transaction.type', 'Transaction type'),
        'incoterm':fields.many2one('stock.incoterms','Incoterm'),
        'intrastat_exclude':fields.boolean('Exclude', help="Isključeno iz Intrastat izvještaja, ostavite isključeno unoliko niste sigurni što radite!"),
        'vrsta_prometa':fields.selection(_VRSTE_PROMETA,'Vrsta prometa',help="Potrebno radi intrastat izvještaja"),

    }
    _defaults = {
        'transaction_type_id': default_transaction_type
    }
    
class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'
    _columns = {
        'transaction_type_id': fields.many2one('intrastat.transaction.type', 'Transaction type'),
        'incoterm':fields.many2one('stock.incoterms','Incoterm'),
        'intrastat_exclude':fields.boolean('Exclude', help="Isključeno iz Intrastat izvještaja, ostavite isključeno unoliko niste sigurni što radite!"),
        'vrsta_prometa':fields.selection(_VRSTE_PROMETA,'Vrsta prometa',help="Potrebno radi intrastat izvještaja"),
    }
    _defaults = {
        'transaction_type_id': default_transaction_type
    }

