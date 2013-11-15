# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2011 Camptocamp SA
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

# TODO : create a base_merge module to provide abstractions for merges ?

from openerp.osv import orm, fields, osv
from tools.translate import _
import tools
from osv.orm import browse_record

class BaseProductMerge(orm.TransientModel):
    """ Merges two products """
    _name = 'base.product.merge'
    _description = 'Merges Two Products'

    _columns = {
        'uom_po_id': fields.selection([('', '')], 'Purchase Unit of Measure',),
        'seller_id': fields.selection([('', '')], 'Seller',),
        'seller_info_id': fields.selection([('', '')], 'SellerInfo'),
        'supply_method': fields.selection([('', '')], 'Supply method',),
        'seller_delay': fields.selection([('', '')], 'Supplier Lead Time',),
        'type': fields.selection([('', '')], 'Product Type',),
        'uom_id': fields.selection ([('', '')], 'Default Unit Of Measure',),
        'list_price': fields.selection ([('', '')], 'Sale Price',),
        'standard_price': fields.selection ([('', '')], 'Cost Price',),
        'name': fields.selection ([('', '')], 'Name' ,),
        'procure_method': fields.selection ([('', '')], 'Procurement Method',),
        'sale_delay': fields.selection ([('', '')], 'Customer Lead Time'),
        'categ_id': fields.selection ([('', '')], 'Category',),
        'code': fields.selection ([('', '')], 'Reference' ,),
        'default_code': fields.selection ([('', '')], 'Reference',),
        'name_template': fields.selection ([('', '')], 'Name',),
        'partner_ref': fields.selection ([('', '')], 'Customer',),
        'lst_price': fields.selection ([('', '')], 'Public Price',),
        'warranty': fields.selection ([('', '')], 'Warranty',),
        'produce_delay': fields.selection ([('', '')], 'Manufacturing Lead Time',),
        'product_manager': fields.selection ([('', '')], 'Product Manager',),
        'state': fields.selection ([('', '')], 'Status',),
        'loc_rack': fields.selection ([('', '')], 'Rack',),
        'loc_row': fields.selection ([('', '')], 'Row',),
        'loc_case': fields.selection ([('', '')], 'Case',),
        'description': fields.selection ([('', '')], 'Description',),
        'description_sale': fields.selection ([('', '')], 'Sale Description',),
        'description_purchase': fields.selection ([('', '')], 'Purchase Description',),
        'nabavna_kn': fields.selection ([('', '')], 'Nabavna u KN',),
        'nabavna_eur' : fields.selection ([('', '')], 'Nabavna u EUR',),
        'nabavna_chf' : fields.selection ([('', '')], 'Nabavna u CHF',),
        'fak1' : fields.selection ([('', '')], 'Faktor 1',),
        'fak2': fields.selection ([('', '')], 'Faktor 2',),
        'p_base': fields.selection ([('', '')], 'Osnovica',),
        }

    _values = {}

    MERGE_SKIP_FIELDS = ['product_tmpl_id', 'product_image']

    def _build_form(self, cr, uid, field_datas, value1, value2):
        formxml = '''<?xml version="1.0"?>
            <form string="%s" version="7.0">
            <separator colspan="4" string="Select datas for new record"/>
            <group>
            ''' % _('Merge')

        update_values = {}
        update_fields = {}
        columns = {}

        for fid, fname, fdescription, ttype, required, relation, readonly in field_datas:
            if fname in self.MERGE_SKIP_FIELDS:
                continue

            val1 = value1[fname]
            val2 = value2[fname]
            my_selection = []
            size = 24

            if (val1 and val2) and (val1 == val2):
                if ttype in ('many2one'):
                    update_values.update({fname: val1.id})
                elif ttype in ('many2many'):
                    update_values.update({fname: [(6, 0, map(lambda x: x.id, val1))]})
                else:
                    update_values.update({fname: val1})

            if (val1 and val2) and (val1 != val2) and not readonly:
                if ttype in ('char', 'text', 'selection'):
                    my_selection = [(val1, val1), (val2, val2)]
                    size = max(len(val1), len(val2))
                if ttype in ('float', 'integer'):
                    my_selection = [(str(val1), str(val1)), (str(val2), str(val2))]
                if ttype in ('many2one'):
                    val1_name = val1.name
                    val2_name = val2.name

                    if isinstance(val1_name, browse_record):
                        val1_name = val1_name.name
                    if isinstance(val2_name, browse_record):
                        val2_name = val2_name.name

                    my_selection = [(str(val1.id), val1_name),
                                    (str(val2.id), val2_name)]
                if ttype in ('many2many'):
                    update_values.update({fname: [(6, 0, list(set(map(lambda x: x.id, val1 + val2))))]})
                if my_selection:
                    if not required:
                        my_selection.append((False, ''))
                    columns.update({fname: fields.selection(my_selection, fdescription, required=required, size=size)})
                    update_fields.update({fname: {'string': fdescription, 'type': 'selection', 'selection': my_selection, 'required': required}})
                    formxml += '\n<field name="%s"/><newline/>' % (fname,)
            if (val1 and not val2) or (not val1 and val2):
                if ttype == 'many2one':
                    update_values.update({fname: val1 and val1.id or val2 and val2.id})
                elif ttype == 'many2many':
                    update_values.update({fname: [(6, 0, map(lambda x: x.id, val1 or val2))]})
                elif ttype == 'one2many':
                    #skip one2many values
                    pass
                else:
                    update_values.update({fname: val1 or val2})

        formxml += """
        </group>
        <separator colspan="4"/>
        <group col="4" colspan="4">
            <label string="" colspan="2"/>
            <footer>
                <button special="cancel" string="Cancel" icon="gtk-cancel"/>
                <button name="action_merge" string="Merge" type="object" icon="gtk-ok"/>
            </footer>
        </group>
        </form>"""
        return formxml, update_fields, update_values, columns

    def check_resources_to_merge(self, cr, uid, resource_ids, context):
        """ Check validity of selected resources.
         Hook for other checks
        """
        if not len(resource_ids) == 2:
            raise osv.except_osv(_('Error!'), _('You must select only two resources'))
        return True

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}
        res = super(BaseProductMerge, self).fields_view_get(cr, uid, view_id, view_type, context=context, toolbar=toolbar, submenu=submenu)
        resource_ids = context.get('active_ids') or []

        if resource_ids:
            self.check_resources_to_merge(cr, uid, resource_ids, context)

#BOLE: ovo je duplana provjera.. za izbaciti
        if not len(resource_ids) == 2: 
            return res
        ####
        obj = self.pool.get('product.product')
        cr.execute("SELECT id, name, field_description, ttype, required, relation, readonly from ir_model_fields where model in ('product.product', 'product.template')")
        field_datas = cr.fetchall()
        obj1 = obj.browse(cr, uid, resource_ids[0], context=context)
        obj2 = obj.browse(cr, uid, resource_ids[1], context=context)
        myxml, merge_fields, self._values, columns = self._build_form(cr, uid, field_datas, obj1, obj2)
        self._columns.update(columns)
        res['arch'] = myxml
        res['fields'] = merge_fields
        return res

    def cast_many2one_fields(self, cr, uid, data_record, context=None):
        """ Some fields are many2one and the ORM expect them to be integer or in the form
        'relation,1' wher id is the id.
         As some fields are displayed as selection in the view, we cast them in integer.
        """
        cr.execute("SELECT name from ir_model_fields where model in ('product.product', 'product.template') and ttype='many2one'")
        fields = cr.fetchall()
        for field in fields:
            if data_record.get(field[0], False):
                data_record[field[0]] = int(data_record[field[0]])
        return data_record

    def action_merge(self, cr, uid, ids, context=None):
        """
        Merges two resources and create 3rd and changes references of old resources with new
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user s ID for security checks,
        @param ids: id of the wizard
        @param context: A standard dictionary for contextual values

        @return : dict to open the new product in a view
        """
        record_id = context and context.get('active_id', False) or False
        pool = self.pool
        if not record_id:
            return {}
        res = self.read(cr, uid, ids, context = context)[0]

        res.update(self._values)
        resource_ids = context.get('active_ids') or []
        
        self.check_resources_to_merge(cr, uid, resource_ids, context)

        resource1 = resource_ids[0]
        resource2 = resource_ids[1]

        obj, obj_parent = pool.get('product.product'), pool.get('product.template')

        remove_field = {}
        # for uniqueness constraint: empty the field in the old resources
        c_names = []
        for check_obj in (obj, obj_parent):
            if hasattr(check_obj, '_sql_constraints'):
                remove_field = {}
                for const in check_obj._sql_constraints:
                    c_names.append(check_obj._name.replace('.', '_') + '_' + const[0])
        if c_names:
            c_names = tuple(map(lambda x: "'"+ x +"'", c_names))
            cr.execute("""select column_name from \
                        information_schema.constraint_column_usage u \
                        join  pg_constraint p on (p.conname=u.constraint_name) \
                        where u.constraint_name in (%s) and p.contype='u' """ % c_names)
            for i in cr.fetchall():
                remove_field[i[0]] = False

        remove_field.update({'active': False})

        obj.write(cr, uid, [resource1, resource2], remove_field, context=context)

        res = self.cast_many2one_fields(cr, uid, res, context)

        res_id = obj.create(cr, uid, res, context=context)

        self.custom_updates(cr, uid, res_id, [resource1, resource2], context)

        # For one2many fields on the resource
        cr.execute("select name, model from ir_model_fields where relation in ('product.product', 'product.template') and ttype not in ('many2many', 'one2many');")
        for name, model_raw in cr.fetchall():
            if hasattr(pool.get(model_raw), '_auto'):
                if not pool.get(model_raw)._auto:
                    continue
            elif hasattr(pool.get(model_raw), '_check_time'):
                continue
            else:
                if hasattr(pool.get(model_raw), '_columns'):
                    from osv import fields
                    if pool.get(model_raw)._columns.get(name, False) and isinstance(pool.get(model_raw)._columns[name], fields.many2one):
                        model = model_raw.replace('.', '_')
                        if name not in self.MERGE_SKIP_FIELDS:
                            cr.execute("update "+model+" set "+name+"="+str(res_id)+" where "+ tools.ustr(name) +" in ("+ tools.ustr(resource1) +", "+tools.ustr(resource2)+")")

        value = {
            'domain': str([('id', '=', res_id)]),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.product',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'res_id': res_id
        }
        return value

    def custom_updates(self, cr, uid, resource_id, old_resources_ids, context):
        """Hook for special updates on old resources and new resource
        """
        pass

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
