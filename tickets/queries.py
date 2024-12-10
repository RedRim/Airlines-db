class IndexTicketsQueries:
    @classmethod
    def get_all(cls, departure_date_from, departure_date_to, departure, destination):
        return f"""
            SELECT 
                subquery.ticket_id AS ticket_id,
                subquery.num,
                subquery.airline_name AS airline_name,
                subquery.ticket_type AS ticket_type,
                subquery.departure AS departure,
                subquery.destination AS destination,
                subquery.flight_time,
                subquery.total_fare,
                subquery.start_point,
                subquery.end_point
            FROM 
                (
                    SELECT 
                        t.id AS ticket_id,
                        c.num,
                        a.name AS airline_name,
                        t.type AS ticket_type,
                        c.departure AS departure,
                        c.destination AS destination,
                        c.fare AS fare,
                        SUM(c.fare) OVER (PARTITION BY t.id) AS total_fare,
                        FIRST_VALUE(c.departure) OVER (PARTITION BY t.id ORDER BY c.num) AS start_point,
                        LAST_VALUE(c.destination) OVER (PARTITION BY t.id ORDER BY c.num ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS end_point,
                        c.flight_time
                    FROM 
                        tickets t
                    JOIN 
                        coupones c 
                        ON t.id = c.ticket
                    JOIN 
                        airlines a
                        ON a.id = t.airline
                ) AS subquery
            WHERE 
                subquery.flight_time BETWEEN '{departure_date_from}' AND '{departure_date_to}'
                AND subquery.start_point = '{departure}'
                AND subquery.end_point = '{destination}'
            ORDER BY 
                subquery.ticket_id, subquery.num;
        """

