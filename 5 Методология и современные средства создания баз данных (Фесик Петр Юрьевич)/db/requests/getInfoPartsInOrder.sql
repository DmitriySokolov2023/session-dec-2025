SELECT 
	mi.quantity,
	mi.unit_price,
	mi.line_total,
	part.name
FROM public.material_items as mi
JOIN public.service_items as si
on mi.service_item_id = si.id
JOIN public.orders as ord
on ord.id = si.order_id
JOIN public.parts as part
on part.id = mi.part_id
where ord.id = 3