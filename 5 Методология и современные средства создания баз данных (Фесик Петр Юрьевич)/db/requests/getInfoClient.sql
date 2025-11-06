SELECT c.id,
       c.name,
       c.phone,
       c.email,
       c.is_company,
	   o.comment,
	   o.id, 
	   o.status
FROM clients c
LEFT JOIN orders o ON o.client_id = c.id
WHERE c.id = 1

