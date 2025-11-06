WITH svc_total AS (
  SELECT COALESCE(SUM(line_total), 0) AS "услуги"
  FROM service_items
  WHERE order_id = 3
),
mat_total AS (
  SELECT COALESCE(SUM(mi.line_total), 0) AS "материалы"
  FROM material_items mi
  WHERE mi.service_item_id IN (SELECT id FROM service_items WHERE order_id = 3)
)
SELECT s."услуги",
       m."материалы",
       (s."услуги" + m."материалы") AS "сумма заказа"
FROM svc_total s CROSS JOIN mat_total m;