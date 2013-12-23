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
    'name': 'Intrastat Codes & Reporting',
    'version': '1.0',
    "category": 'Accounting & Finance',
    'description': """
A module that adds:
    - intrastat codes
    - intrastat transaction types
    - intrastat reports
    
This module gives the details of the goods traded between the countries of European Union. 
Taken from MENTIS d.o.o.(http://www.mentis.si)
rewrite for HR localization by Bole
    """,
    'author': 'DAJ MI 5',
    'website': 'http://www.dajmi5.com',
    'depends': ['base', 
                'product', 
                'stock', 
                'sale', 
                'purchase'],
    'data': [
        'data/intrastat_countries_data.xml',
        'data/stock_incoterms.xml',  #nijre nuzno, samo je dodan xxx, mislio da cu uspjeti prevesti
        'intrastat_transaction_type_view.xml',
        'intrastat_view.xml',
        'report/intrastat_report.xml',
        'security/ir.model.access.csv',
        'data/intrastat.code.csv',
        'data/intrastat.transaction.type.csv'
            ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
