class intrastat_in(osv.AbstractModel):
    _name = 'intrastat.in'
    _description = 'Intrastat recived report'
    
    _columns= {
               'id':fields.integer('ID'),
               'picking_id':fields.many2one('stock.picking','Skladište ulaz'),
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
               'product_id':fields.many2one('product.product','Product'),
               'product_name':fields.char('Product name', size=256),
               'intrastat_id':fields.many2one('intrastat.code','Intrastat code'),
               'weight_net':fields.float('Težina', digits=(12,3)),
               'country_origin':fields.char('Zemlja proizvodnje', size=2)
               }
    def init(self, cr, context=None):
        sql="""
            CREATE or REPLACE view intrastat_in as( 
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
                UIL.price_subtotal as subtotal,
                UIL.quantity as quantity,
                UIL.dep_cost_amount as dep_cost,
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
                LEFT JOIN account_invoice_line UIL on UIL.id = SM.purchase_line_id
                /*croatia_id=98*   AND CPAR.id <> '98' */
            WHERE 
                SP.state='done' AND SP.type<>'internal' AND CPAR.id <> '98'
            )
            """
        drop_view_if_exists(cr, 'intrastat_in')
        cr.execute(sql) 

class intrastat_out(osv.AbstractModel):
    _name = 'intrastat.out'
    _description = 'Intrastat sent report'
    
    _columns= {
               'id':fields.integer('ID'),
               'picking_id':fields.many2one('stock.picking','Skladište izlaz'),
               'picking_name':fields.char('Dokument', size=64),
               'month':fields.char('Month',size=2),
               'year':fields.char('Year', size=4),
               'partner_id':fields.many2one('res.partner','Partner'),
               'country_code':fields.char('Zemlja', size=2),
               'country_intrastat':fields.boolean('Country intrastat'),
               'transaction_type_id':fields.many2one('intrastat.transaction.type','Transaction type'),
               'invoiced_state':fields.char('Invoice state', size=16),
               'ira_id':fields.many2one('account.invoice','Ulazni račun'),
               'ira':fields.char('Br.izl.račun', size=16),
               'product_id':fields.many2one('product.product','Product'),
               'product_name':fields.char('Product name', size=256),
               'intrastat_id':fields.many2one('intrastat.code','Intrastat code'),
               'weight_net':fields.float('Težina', digits=(12,3)),
               'country_origin':fields.char('Zemlja proizvodnje', size=2)
               }
    def init(self, cr, context=None):
        sql="""
            CREATE or REPLACE view intrastat_out as( 
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
                IRA.id as ura_id,
                IRA.number as ura,
                IIL.price_subtotal as subtotal,
                IIL.quantity as quantity,
                IIL.dep_cost_amount as dep_cost,
                PPROD.id as product_id,
                PTEM.name as product_name,
                PTEM.intrastat_id as intrastat_id,
                PTEM.weight_net as weight_net,
                CPRO.code as country_origin     
            FROM stock_picking as SP
                LEFT JOIN res_partner PA on (PA.id = SP.partner_id)
                LEFT JOIN res_country CPAR on CPAR.id = PA.country_id
                LEFT JOIN account_invoice IRA on IRA.id = SP.sale_id
                LEFT JOIN stock_move SM on SM.picking_id=SP.id
                LEFT JOIN (product_template PTEM
                    LEFT JOIN product_product PPROD on (PPROD.product_tmpl_id = PTEM.id))
                    on (SM.product_id = PPROD.id)
                LEFT JOIN res_country CPRO on CPRO.id = PTEM.country_origin
                LEFT JOIN account_invoice_line IIL on IIL.id = SM.sale_line_id
                /*croatia_id=98*   AND CPAR.id <> '98' */
            WHERE 
                SP.state='done' AND SP.type<>'internal' AND CPAR.id <> '98'
            )
            """
        drop_view_if_exists(cr, 'intrastat_out')
        cr.execute(sql) 
