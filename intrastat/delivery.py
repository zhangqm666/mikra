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

class delivery_carrier(osv.Model):
    _inherit  = "delivery.carrier"
    
    _VRSTE_PROMETA=[('1','Pomorski promet'),
                    ('2','Željeznički promet'),
                    ('3','Cestovni promet'),
                    ('4','Zračni promet'),
                    ('5','Poštanska pošiljka'),
                    ('6','Fiksne prometne instalacije'),
                    ('7','Promet kopnenim plovnim putevima'),
                    ('8','Vlastiti pogon')]
    
    _columns = {
                'vrsta':fields.selection(_VRSTE_PROMETA,'Vrsta prometa',help="Potrebno radi intrastat izvještaja", required="True")
                }
    
    
    