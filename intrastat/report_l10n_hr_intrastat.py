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
from tools.sql import drop_view_if_exists
from decimal_precision import decimal_precision as dp
import time




class intrastat(osv.AbstractModel):
    _name='intrastat'
    _description = "Intrastat report"
    _auto = False
    _columns = {
        'id':fields.many2one('stock.picking','Skladiste', readonly=True),
        'picking_name':fields.char('Dokument', size=64,readonly=True),
        
        'intrastat_id': fields.many2one('intrastat.code', 'Intrastat code', readonly=True),
        #'intrastat_name': fields.related('intrastat_id', 'description', type='char', string='Intrastat name'),
        
        'product_id':fields.many2one('product.product','Product'),
        
        'partner_id':fields.many2one('res.partner','Partner', readonly=True),
        'partner':fields.char('Partner', size=128),
        
        'country_code': fields.char('Country code', size=2, readonly=True),
        'country_intrastat': fields.boolean('In Intrastat', readonly=True),
        
        'transaction_type_id': fields.many2one('intrastat.transaction.type', 'Transaction type', readonly=True),
        #'transaction_type_code': fields.related('transaction_type_id', 'code', type='char', string='Trans. type'),
        
        
        #'country_origin': fields.many2one('res.country', 'Country of origin', readonly=True),
        #'country_origin_code': fields.related('country_origin', 'code', type='char', string='Country of origin'),
        
        #'weight_net': fields.float('Weight', readonly=True),
        #'value': fields.float('Value', readonly=True, digits_compute=dp.get_precision('Account')),
        'date': fields.char('Date done',size=64,required=False, readonly=True),
        'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'),
            ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],'Month',readonly=True),
        'year': fields.char('Year',size=64,required=False, readonly=True),
    }
    def init(self, cr):
        drop_view_if_exists(cr, 'intrastat')
        drop_view_if_exists(cr, 'l10n_hr_intrastat')
        cr.execute("""
            create or replace view intrastat as (
                SELECT 
                    SP.id ,
                    SP.name as picking_name,
                    to_char(SP.date_done, 'YYYY') || '-' || to_char(SP.date_done, 'MM') as date,
                    to_char(SP.date_done, 'MM') as month,
                    to_char(SP.date_done, 'YYYY') as year,
                    SP.partner_id as partner_id,
                    PA.name as partner,
                    C.code as country_code,
                    C.intrastat as country_intrastat,
                    SP.transaction_type_id as transaction_type_id,
                    SP.invoice_state as invoice_state,
                    URA.number as ura,
                    PTEM.intrastat_id as intrastat_id,
                    PPROD.id as product_id
                    
                FROM stock_picking as SP
                    LEFT JOIN res_partner PA on (PA.id = SP.partner_id)
                    LEFT JOIN res_country C on C.id = PA.country_id
                    LEFT JOIN account_invoice URA on URA.id = SP.purchase_id
                    LEFT JOIN stock_move SM on SM.picking_id=SP.id
                    left join (product_template PTEM
                        left join product_product PPROD on (PPROD.product_tmpl_id = PTEM.id))
                        on (SM.product_id = PPROD.id)
                    
                    /*croatia_id=98*   and c.id <>'98' */
                WHERE SP.state='done' 
                    )""")

