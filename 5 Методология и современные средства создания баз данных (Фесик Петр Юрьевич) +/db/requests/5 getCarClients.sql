SELECT
  c.id AS client_id, c.is_company, c.name AS client_name, c.phone, c.email, c.comment,
  ca.id AS car_id, ca.make, ca.model, ca.vin, ca.license_plate, ca.year, ca.mileage
FROM clients c
LEFT JOIN cars ca ON ca.client_id = c.id
WHERE c.id = 3
ORDER BY ca.id;

