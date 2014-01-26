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

from osv import osv, fields
from openerp.tools.translate import _
import decimal_precision as dp
import psycopg2


class account_invoice(osv.Model):
    _inherit = "account.invoice"
    
    SORT_VRSTE = (('name_az','Po nazivu (A->Z)'),
                  ('name_za','Po nazivu (Z->A)'),
                  ('seq','Ručno postavljeni redosljed (snimiti prije ispisa)'),
                  ('def','Redosljed upisivanja stavaka'))
    
    _columns = {
                'narudzba':fields.char('Narudžba br', size=64),
                'sort_print':fields.selection(SORT_VRSTE,'Redosljed stavaka pri ispisu',
                                              help="Ostaviti prazno za ispis po redosljedu upisa stavaka ili izabrati željeni redosljed")
                }
    
    def invoice_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'mikra.account.invoice',
            'datas': datas, 'nodestroy' : True }