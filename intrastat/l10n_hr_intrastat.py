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
from datetime import datetime, date
from lxml import etree
from psycopg2.errorcodes import NO_DATA_FOUND
import base64
#import XML_Generator

NO_DATA = 'NO_DATA'

class l10n_hr_intrastat(osv.Model):
    _name='l10n.hr.intrastat'
    _description = "Croatian intrastat reports"
   
    #def count_lines(self, cr, uid, field, value, context=None):
        
     
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
    
    
    def header_fill(self, cr, uid, envelope, context=None):
        header = etree.SubElement(envelope,'Header')
        if context is None:
            context={}
        company_id = context.get('company_id') or 1
        company = self.pool.get('res.partner').browse(cr, uid, company_id)
        
        tok_robe = etree.SubElement(header,'FlowOfGoods')
        tok_robe.text='1'
        ###
        izv_jed = etree.SubElement(header,'PSI')
        jed_id = etree.SubElement(izv_jed,'PSIId')
        jed_id_cc = etree.SubElement(jed_id,'PSICountryCode')
        jed_id_cc.text = company.country_id.code
        jed_id_vat = etree.SubElement(jed_id,'PSININumber')
        jed_id_vat.text = company.vat[2:]
        
        jed_name = etree.SubElement(izv_jed,'PSIName')
        jed_name.text = company.name
        jed_adresa = etree.SubElement(izv_jed,'PSIAddress')
        jed_adresa.text = company.street
        if company.street2:
            jed_adresa.text += ', '+ company.street2
        jed_adresa.text += ', ' + company.city
        
        period = etree.SubElement(header,'ReferencePeriod')
        period.text = '2014-01'
        
        #declarant = etree.SubElement(int_header,'Declarant')
        #dec_id = etree.SubElement(declarant,'DeclarantId')
        #dec_id_cc = etree.SubElement(dec_id,'DeclarantCountryCode')
        #dec_id_vat = etree.SubElement(dec_id,'DeclarantNINumber')
        #dec_name = etree.SubElement(declarant,'DeclarantName')
        #dec_address = etree.SubElement(declarant,'DeclarantAddress')
        #dec_country = etree.SubElement(declarant,'DeclarantCountry')
        
        dep_type = etree.SubElement(header,'IntrastatDepartment')
        #TODO : generira se automatski?
        
        rep_type = etree.SubElement(header,'ReportType')
        rep_type.text = 'I'
        rep_date= etree.SubElement(header,'ReportDate')
        rep_date.text = datetime.strftime(datetime.now(),"%Y-%m-%d")
        return header
    
    def declaration_fill(self,cr, uid, envelope):
        declaration = etree.SubElement(envelope, 'declaration')
        datas = self.pool.get('l10n.hr.intrastat.line')
        data_ids = datas.search(cr, uid, [('type','=','1')])
        #ITERCIJA PO PROIZVODIMA
        br = 0
        for p in datas.browse(cr, uid, data_ids):
            br +=1
            item = etree.SubElement(declaration,'Item')
            redni_broj = etree.SubElement(item,'ItemNr')
            redni_broj.text = str(br)
            sifra_robe = etree.SubElement(item,'CN8Code')
            sifra_robe.text = p.sifra_robe and p.sifra_robe or NO_DATA
            opis_robe = etree.SubElement(item,'GoodsDescription')
            opis_robe.text = p.opis_robe and p.opis_robe or NO_DATA
            sifra_zemlje = etree.SubElement(item,'DestinationCountryCode')
            sifra_zemlje.text = p.zemlja and p.zemlja or NO_DATA
            incoterm = etree.SubElement(item,'DeliveryTerms')
            incoterm.text = p.incoterm_id and p.incoterm_id.code or NO_DATA
            vrsta_posla = etree.SubElement(item, 'NatureOfTransaction')
            vrsta_posla = p.vrsta_posla and p.vrsta_posla or NO_DATA
            vrsta_prometa = etree.SubElement(item, 'TransportMode')
            #vrsta_prometa.text = 
            porijeklo_robe = etree.SubElement(item, 'CountryOfOriginCode')
            porijeklo_robe.text = p.porijeklo_robe and p.porijeklo_robe or NO_DATA
            neto_masa = etree.SubElement(item, 'NetWeight')
            neto_masa.text = p.neto_masa and p.neto_masa or NO_DATA
            kolicina_jm = etree.SubElement(item, 'QuantityInSU')
            kolicina_jm = p.kolicina and p.kolicina or NO_DATA
            fakturna = etree.SubElement(item, 'InvoicedAmount')
            fakturna = p.fak_vrijedi and p.fak_vrijedi or NO_DATA
            statisticka = etree.SubElement(item, 'StatisticalValue')
            statisticka.text = p.stat_vrijedi and p.stat_vrijedi or NO_DATA 
            
        
        return declaration, br
    
    def export_to_xml(self, cr, uid, ids, context=None):
        report = etree.Element('IR001A') #, attrib=None, nsmap=None, **_extra)
        envelope = etree.SubElement(report,'Element')    
        #HEADER
        header = self.header_fill(cr, uid, envelope)     
        #DECLARATION
        declaration , rb = self.declaration_fill(cr, uid, envelope) #etree.SubElement(envelope, 'declaration')
        total_items = etree.SubElement(header,'TotalItems')
        total_items.text = str(rb)
        
        xml_string = etree.tostring(report, pretty_print=True)  
        attach_id = self.attach_xml_file(cr, uid, ids, xml_string, context)
        return True
    
    def attach_xml_file(self, cr, uid, ids, xml_string, context=None):
        assert len(ids) == 1, "Only one ID accepted"
        #joppd_obj= self.pool.get('l10n.hr.joppd')
        #jop_obj= joppd_obj.browse(cr, uid, ids[0])
        file_name = '-'.join(['INTRASTAT' , 'I', datetime.strftime(datetime.now(),"%Y-%m-%d")])+'.xml'
        attach_name = file_name
        attach_obj = self.pool.get('ir.attachment')
        context.update({'default_res_id': ids[0], 'default_res_model': 'l10n.hr.intrastat'})
        attach_id = attach_obj.create(cr, uid, {'name': attach_name, 
                                                'datas': base64.encodestring(xml_string), 
                                                'datas_fname': file_name}, context=context)
        return attach_id
    
    def fill_data_wiz(self, cr, uid, ids, context=None):
        #pretpostavljam da je single id
        izv = self.browse(cr, uid, ids[0])
        if not izv.period_id:
            raise osv.except_osv('Greška','Morate odabrati period')
        p_start = izv.period_id.date_start
        p_stop = izv.period_id.date_stop
        
        sp = self.pool.get('stock.picking')
        sp_ids = sp.search(cr, uid, ['&',('date_done','>=',p_start),('date_done','<=',p_stop)])
        line = []
        for l in izv.line_ids:
            line.append((2,l.id))
        for p in sp.browse(cr, uid, sp_ids):
            type =False
            if p.purchase_id: type ='1'
            elif p.sale_id:   type ='2'
                         
            
            
            values = {
                      'type': type,
                      'product_id':p.product_id.id,
                      'sifra_robe':p.product_id.product_tmpl_id.intrastat_id.name,
                      'opis_robe':p.product_id.name,
                      'porijeklo_robe':p.product_id.country_origin.code or False,
                      'neto_masa':p.product_id.weight_net or 0.000,
                      'zemlja':p.partner_id.country_id.code or False,
                      }
            line.append((0,0, values))
        period = izv.period_id.name
        name = izv.vrsta + ' obrazac za ' + period #
        name += ' (' +datetime.strftime(datetime.now(),"%d.%m.%Y.") + ')'
        vals = {
                'date':datetime.now(),
                'name':name,
                'year':izv.period_id.date_start[:4],
                'month':izv.period_id.date_start[5:][:2],
                'line_ids':line}
        return izv.write(vals)

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
                #vrsta prometa
                'fak_vrijedi':fields.float('Fakturna vrijednost', digits=(16,2)),
                'stat_vrijedi':fields.float('Statistička vrijednost', digits=(16,2))
                }




##############################################################################
#########  AL IN ONE : TO BE REMOVED !
##############################################################################
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