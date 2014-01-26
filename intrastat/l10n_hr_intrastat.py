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




class l10n_hr_intrastat(osv.Model):
    _name='l10n.hr.intrastat'
    _description = "Croatian intrastat reports"
   
    
     
    _columns = {
                'state':fields.selection([('draft','Draft'),
                                          ('sent','Sent'),
                                          ('done','Done'),
                                          ('cancel','Cancel')],'State'),
                'name':fields.char('Name', size=64),
                'year':fields.char('Year', size=4),
                'period_id':fields.many2one('account.period','Period'),
                'month':fields.selection([('01','January'), ('02','February'),('03','March'), 
                                          ('04','April'), ('05','May'), ('06','June'),
                                          ('07','July'), ('08','August'),('09','September'), 
                                          ('10','October'), ('11','November'), ('12','December')],'Month',),
                
                'vrsta':fields.selection([('I','Izvorni obrazac'),
                                          ('N','Nadomjesni obrazac'),
                                          ('B','Brisanje prethodno dostavljenog obrasca'),
                                          ('0','Prazan obrazac')], 'Vrsta obrasca'),
                'evid_broj':fields.char('Evidencijski broj', size=10, help="Broj koji se dobije kad je obrazac prihvaćem i uveden u sustav"),
                'date':fields.date('Datum izvještaja'),
                'lines_in':fields.integer('Broj stavaka primitaka'),
                'lines_out':fields.integer('Broj stavaka otpreme'),
                'line_ids':fields.one2many('l10n.hr.intrastat.line','report_id','Stavke')
                }
    
    _defaults = {
                 'state':'draft',
                 'vrsta':'I',
                 }
    
    def fill_data_wiz(self, cr, uid, ids, context=None):
        #pretpostavljam da je single id
        izv = self.browse(cr, uid, ids[0])
        if not izv.period_id:
            raise osv.except_osv('Greška','Morate odabrati period')
        p_start = izv.period_id.date_start
        p_stop = izv.period_id.date_stop
        type='in'
        
        return res

class l10n_hr_intrastat_line(osv.Model):
    _name='l10n.hr.intrastat.line'
    _description = "Croatian intrastat report lines"
   
    _columns = {
                'report_id':fields.many2one('l10n.hr.intrastat','Izvještaj'),
                'type':fields.selection([('1','Primitak'),('2','otprema')],'Tok robe'),
                'redni_br':fields.integer('Redni broj'),
                'product_id':fields.many2one('product.product','Proizvod'),
                'sifra_robe':fields.char("Intrastat code", size=8),
                'opis_robe':fields.char('Opis robe', size=256),
                'porijeklo_robe':fields.char("Zemlja porijekla robe", size=2),
                'neto_masa':fields.float("Netto masa", digits=(16,3)),
                'kolicina':fields.float('Količina u jedinici mjere', digits=(12,3)),
                'zemlja':fields.char('Zemlja', size=2),
                'incoterm_id':fields.many2one('stock.incoterms','Incoterm'),
                'vrsta_posla':fields.many2one('intrastat.transaction.type','Vrsta posla'),
                'fak_vrijedi':fields.float('Fakturna vrijednost', digits=(16,2)),
                'stat_vrijedi':fields.float('Statistička vrijednost', digits=(16,2))
                }


class intrastat_preview(osv.AbstractModel):
    _name="intrastat.preview"
    _description=" Intrastat data prewiew"
    
    _columns= {
               'id':fields.integer('ID'),
               'picking_id':fields.many2one('stock.picking','Zaliha'),
               'picking_name':fields.char('Dokument', size=64),
               'month':fields.char('Month',size=2),
               'year':fields.char('Year', size=4),
               'partner_id':fields.many2one('res.partner','Partner'),
               'country_code':fields.char('Zemlja', size=2),
               'country_intrastat':fields.boolean('Country intrastat'),
               'transaction_type_id':fields.many2one('intrastat.transaction.type','Transaction type'),
               'invoiced_state':fields.char('Invoice state', size=16),
               'ura_id':fields.many2one('account.invoice','Ulazni račun'),
               'ura':fields.char('Br.ul.račun', size=16),
               'ira_id':fields.many2one('account.invoice','Izlazni račun'),
               'ira':fields.char('Br.izl.račun', size=16),
               'product_id':fields.many2one('product.product','Product'),
               'product_name':fields.char('Product name', size=256),
               'intrastat_id':fields.many2one('intrastat.code','Intrastat code'),
               'weight_net':fields.float('Težina', digits=(12,3)),
               'country_origin':fields.char('Zemlja proizvodnje', size=2)
               }
    
    def init(self, cr, context=None):
        sql="""
            CREATE or REPLACE view intrastat_preview as( 
            SELECT 
                row_number() OVER (ORDER BY SP.id) as id  ,
                SP.id as picking_id,
                SP.name as picking_name,
                to_char(SP.date_done, 'YYYY') || '-' || to_char(SP.date_done, 'MM') as date,
                to_char(SP.date_done, 'MM') as month,
                to_char(SP.date_done, 'YYYY') as year,
                SP.partner_id as partner_id,
                PA.name as partner,
                CPAR.code as country_code,
                CPAR.intrastat as country_intrastat,
                SP.transaction_type_id as transaction_type_id,
                SP.invoice_state as invoiced_state,
                URA.id as ura_id,
                URA.number as ura,
                IRA.id as ira_id,
                IRA.number as ira,
                PPROD.id as product_id,
                PTEM.name as product_name,
                PTEM.intrastat_id as intrastat_id,
                PTEM.weight_net as weight_net,
                CPRO.code as country_origin
                
                
            FROM stock_picking as SP
                LEFT JOIN res_partner PA on (PA.id = SP.partner_id)
                LEFT JOIN res_country CPAR on CPAR.id = PA.country_id
                LEFT JOIN account_invoice URA on URA.id = SP.purchase_id
                LEFT JOIN account_invoice IRA on IRA.id = SP.sale_id
                LEFT JOIN stock_move SM on SM.picking_id=SP.id
                LEFT JOIN (product_template PTEM
                    LEFT JOIN product_product PPROD on (PPROD.product_tmpl_id = PTEM.id))
                    on (SM.product_id = PPROD.id)
                LEFT JOIN res_country CPRO on CPRO.id = PTEM.country_origin
                
                /*croatia_id=98*   AND CPAR.id <> '98' */
            WHERE 
                SP.state='done' AND SP.type<>'internal' AND CPAR.id <> '98'
        
            )
            """
        drop_view_if_exists(cr, 'intrastat_preview')
        cr.execute(sql)