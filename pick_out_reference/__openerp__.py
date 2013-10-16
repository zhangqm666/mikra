# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Module: pick_out_reference
#    Author: Davor Bojkić
#    mail:   bole@dajmi5.com
#    Copyright (C) 2012- Daj Mi 5, 
#                  http://www.dajmi5.com
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

{
    "name" : "Picking out - customer reference",
    "description" : """
Customer reference on picking out documents
===========================================

Author: Davor Bojkić - Bole @ DAJ MI 5     www.dajmi5.com

               
Gets the customer reference from sales order while creating picking out and delivery order 
""",
    "version" : "1.07",
    "author" : "DAJ MI 5",
    "category" : "Stock",
    "website": "http://www.dajmi5.com",

    'depends': [
                
                'sale_stock'
                ],
    'update_xml': [
                   'stock_view.xml'
                   ],
    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
