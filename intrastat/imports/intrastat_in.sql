SELECT 
	SP.id, SP.name,
	to_char(SP.date_done, 'YYYY') || '-' || to_char(SP.date_done, 'MM') as date,
    to_char(SP.date_done, 'MM') as month,
    to_char(SP.date_done, 'YYYY') as year,
	PA.name as partner,
	C.name as country,
	SP.transaction_type_id as transaction_type_id,
	SP.invoice_state as invoiced_state,
	URA.name as ura,
	PT.intrastat_id,
	IC.NAME as intrastat_code,/*remove*/
	PT.name as product		
		
FROM stock_picking as SP
	LEFT JOIN res_partner PA on (PA.id = SP.partner_id)
	LEFT JOIN res_country C on C.id = PA.country_id
	LEFT JOIN account_invoice URA on URA.id = SP.purchase_id
	LEFT JOIN stock_move SM on SM.picking_id=SP.id
    LEFT JOIN (product_template PT 
         LEFT JOIN product_product PP on (PP.product_tmpl_id = PT.id)
		 LEFT JOIN intrastat_code IC on (IC.id = PT.intrastat_id))
            on (SM.product_id = PP.id)

WHERE SP.state='done' 
