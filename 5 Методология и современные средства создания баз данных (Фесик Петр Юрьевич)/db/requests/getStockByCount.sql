SELECT id, part_number, name, unit, price, stock_qty
FROM parts
WHERE stock_qty < 10
ORDER BY stock_qty ASC, name;