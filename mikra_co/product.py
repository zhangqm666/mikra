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

from osv import fields, osv

def get_tecaj_kn(self, cr, uid, context=None):
    tecajna=self.pool.get('res.currency')
    kn = tecajna.search(cr, uid, [('name','=','HRK')])
    return tecajna.browse(cr, uid, kn[0]).rate

class product_template(osv.Model):
    _inherit = "product.template"
    
    def _izracunaj(self, cr, uid, ids, field_name, field_values, context=None):
        res={}
        kn_tec = get_tecaj_kn(self, cr, uid)
        for prod in self.browse(cr, uid, ids):
            if prod.nabavna_eur:
                res[prod.id] = {'rnabavna_75': prod.nabavna_eur * 7.5,
                                'rnabavna_80': prod.nabavna_eur * 8,
                                'rnabavna_tec':prod.nabavna_eur * kn_tec,
                                'standard_price':prod.nabavna_eur * kn_tec
                                }
            elif prod.nabavna_kn:
                res[prod.id] = {
                                'rnabavna_tec':prod.nabavna_kn,
                                'standard_price':prod.nabavna_kn
                                }
        return res
    
    def digitron (self, cr, uid, ids, p_base=None, fak1=None, fak2=None, context=None):
        if isinstance(ids, int): ids = [ids]
        res={}
        pids , vals = [], []
        tecaj = get_tecaj_kn(self, cr, uid, ids)
        for p in self.pool.get('product.template').browse(cr, uid, ids):
            if p_base :
                base = p_base
            else :
                base = p.p_base and p.p_base or False
            base_p = ( base=='n75' and p.rnabavna_75 or
                       base=='n80' and p.rnabavna_80 or
                       base=='hrk' and p.rnabavna_tec or 
                       base=='dom' and p.nabavna_kn or False  )
            f1 = fak1 or p.fak1 
            f2 = fak2 or p.fak2
            if f1!=0 and f2!=0 and base_p:
                res[p.id]={'prodajna':base_p*f1*f2}
            
            if p.nabavna_eur and p.nabavna_eur != 0.0 :
                nab = p.nabavna_eur * tecaj
                pids.append(p.id)
                vals.append({'standard_price': nab})
                res[p.id].update({'standard_price': nab})
            elif p.nabavna_kn and p.nabavna_kn != 0.0 :
                pids.append(p.id)
                vals.append({p.id:{'standard_price':p.nabavna_kn}})
                res[p.id].update({'standard_price': p.nabavna_kn})
            
        return res, pids, vals
    
    def onchange_digitron(self, cr, uid, ids, p_base, fak1, fak2):
        return {'value':self.digitron(cr, uid, ids[0], p_base, fak1, fak2)[ids[0]]}
            
    _columns = {
                'name': fields.char('Name', size=256, required=True, translate=True, select=True),
                'nabavna_kn':fields.float('Nabavna KN',help="nabavna cijena u kunama"),
                'nabavna_eur':fields.float('Nabavna EUR',help="nabavna cijena u eurima"),
                'nabavna_chf':fields.float('Nabavna CHF', help="nabavna cijena u švicarcima"),
                'rnabavna_75':fields.function(_izracunaj, string='Nabavna EUR 7.5', type="float", multi="tecaj",help="nabavna cijena (eur) po tečaju 7,5", store = True),
                'rnabavna_80':fields.function(_izracunaj, string='Nabavna EUR 8.0', type="float", multi="tecaj", help="nabavna cijena (eur) po tečaju 8.0", store = True),
                'rnabavna_tec':fields.function(_izracunaj, string='Nabavna TEČAJ', type="float", multi="tecaj", help="nabavna cijena (eur) po trenutnom tečaju ", store = True),
                'fak1':fields.float('Faktor1'),
                'fak2':fields.float('Faktor2'),
                'p_base':fields.selection([('n75','Nabavna  7.5'),('n80','Nabavna 8.0'),('tec','Nabavna tecaj'),('dom','Nabavna KN')],'Osnovica',help="Odabir osnove za izračun javne cijene"),
                'prodajna':fields.float('Izr. Prod.', help="Pregled izračunate prodajne cijene prije uvrštenja")
                }
    
    _defaults = {
                 'fak1':1,
                 'fak2':1,
                 'p_base':'n75',
                 'type':'product',
                 'procure_method':'make_to_order'
                 }
    
    
        
    
class product_product(osv.Model):
    _inherit = 'product.product'
    
    
    
    def onchange_digitron(self, cr, uid, ids, p_base, fak1, fak2):
        if ids==[] : return False
        prod = self.browse(cr, uid, ids[0]).product_tmpl_id.id
        t = self.pool.get('product.template')
        return {'value':t.digitron(cr, uid, prod, p_base, fak1, fak2)[0][ids[0]]}
    
    
    
    def zapisi_nabavne(self, cr, uid, ids, context=None):
        template=self.pool.get('product.template')
        tecaj = get_tecaj_kn(self, cr, uid, ids)
        
        t_all_active=template.search(cr, uid, [('id','<',10000)])
        nabavne = []
        for t in template.browse(cr, uid, t_all_active):
            
            if t.nabavna_eur and t.nabavna_eur != 0.0 :
                nab = t.nabavna_eur * tecaj
                nabavne[t.id] = {'standard_price': nab}
            elif t.nabavna_kn and t.nabavna_kn != 0.0 :
                nabavne[t.id] = {'standard_price':t.nabavna_kn}
        pass
        #template.write(cr, uid, nabavne)
        return True
    
    def primjeni_prodajnu(self, cr, uid, ids, context=None):
        return self.primjeni_na_kategoriju(cr, uid, ids, tip="prod1", context=context )
    
    def primjeni_nabavnu(self, cr, uid, ids, context=None):
        return self.primjeni_na_kategoriju(cr, uid, ids, tip = "nab1",context=context )
        
    def primjeni_na_kategoriju(self, cr, uid, ids, tip, context=None):
        """
        Tipovi zapisivanja: 
        1. Prodajna sve prepiši
        2. Prepiši nabavnu za kategoriju
        """
        
        prod=self.browse(cr, uid, ids[0])
        template = prod.product_tmpl_id
        tcat = template.categ_id.id
        selected = self.pool.get('product.template').search(cr, uid, [('categ_id','=',tcat)])

        vals = self.pool.get('product.template').digitron(cr, uid, selected, template.p_base, template.fak1, template.fak2)
        values = vals[0] #mozda mi jos zatrebaju i drugacije formatirani.. 
        t=self.pool.get('product.template')
        for val in values:
            if tip == "prod1":
                t.write(cr, uid, val, {'list_price' : values[val]['prodajna'], 
                                   'fak1':template.fak1,
                                   'fak2':template.fak2,
                                   'p_base':template.p_base,
                                   'prodajna':values[val]['prodajna'],
                                   })
            elif tip == "nab1":
                if values[val]['standard_price']:
                    t.write(cr, uid, val, {'standard_price':values[val]['standard_price']})  
        
        return True
    
    _columns = {
                'name_template': fields.related('product_tmpl_id', 'name', string="Template Name", type='char', size=256, store=True, select=True),
                }
                

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: