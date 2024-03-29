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
from openerp import netsvc

class sale_order(osv.Model):
    _inherit = "sale.order"
    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cr)
        datas = {
                 'ids': ids,
                 'model': 'sale.order',
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 
                'report_name': 'mikra.sale.order', 
                'datas': datas, 'nodestroy': True}
        
    def action_button_confirm(self, cr, uid, ids, context=None):
        tomo = self.pool.get('res.users').search(cr, uid,[('login','=','tbozicevic')])[0]
        ivanal = self.pool.get('res.partner').search(cr, uid,[('name','=','IVANAL d.o.o.')])[0]
        partner = self.browse(cr, uid, ids[0]).partner_id.id #pool.get('sale.order')
        if uid == tomo and partner == ivanal:
            if not self.browse(cr, uid, ids[0]).origin:
                #self.pool.get('sale.order').write(cr, uid, ids[0],{'origin':'WARNED'})
                raise osv.except_osv(('TOMO PAZI!'),('Ako roba ide sa skladista IVANAL odaberi Prodavaonica IVANAL\n'\
                                                    'Ako prodaješ direktno, onda je prodavaonica MIKRA VP.\n\n'\
                                                    'Upiši OK u polje Izvorni dokument da potvrdiš ovu ponudu!'))
            
        return super(sale_order, self).action_button_confirm(cr, uid, ids, context=None)
        
    SORT_VRSTE = (('name_az','Po nazivu (A->Z)'),
                  ('name_za','Po nazivu (Z->A)'),
                  ('seq','Ručno postavljeni redosljed (snimiti prije ispisa)'),
                  ('def','Redosljed upisivanja stavaka'))
                     
    _columns = {
                'sort_print':fields.selection(SORT_VRSTE,'Redosljed stavaka pri ispisu',
                                              help="Ostaviti prazno za ispis po redosljedu upisa stavaka ili izabrati željeni redosljed")
                }
    
    _defaults = {
                 'order_policy':'picking'
                 }