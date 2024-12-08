SELECT 
	t.id,
	a.name,
	c.fare,
    t.type,
	c.flight_time,
	c.departure,
	c.destination,
	sum(c.fare) over (partition by t.id) as total_fare
FROM 
    tickets t
JOIN 
    coupones c 
	ON t.id = c.ticket
join 
	airlines a
	on a.id=t.airline
order BY 
	t.id, c.num
