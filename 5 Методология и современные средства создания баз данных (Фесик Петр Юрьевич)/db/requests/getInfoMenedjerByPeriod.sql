SELECT
  o.id AS order_id, o.opened_at, o.closed_at, o.status, o.comment,
  c.name AS client_name,
  ca.make, ca.model, ca.license_plate
FROM orders o
JOIN employees m   ON m.id = o.manager_id
JOIN clients  c    ON c.id = o.client_id
JOIN cars     ca   ON ca.id = o.car_id AND ca.client_id = o.client_id
WHERE m.full_name = 'Смирнов Игорь Алексеевич'
  AND o.opened_at >= '2025-01-01'
  AND o.opened_at <  '2025-05-20'
ORDER BY o.opened_at;

