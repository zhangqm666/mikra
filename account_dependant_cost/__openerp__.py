# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Mentis d.o.o. (<http://www.mentis.si/openerp>).
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
    'name': 'Dependant cost calculation',
    'version': '1.0',
    "category": 'Accounting & Finance',
    'description': """
A module that adds:
    
    - dependant cost calculation for invoice lines
cost can be distributed :
-manualy
-by units
-by price
-by weight
    
Dependant cost calculation
    """,
    'author': 'DAJ MI 5',
    'website': 'http://www.dajmi5.com',
    'depends': [
        'base', 
        'product',
        'account', 
        'purchase',
                ],
    'data': [
        'account_invoice_view.xml',
        'wizard/account_dependant_cost_view.xml'
            ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
