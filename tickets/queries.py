class TicketsQueries:
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
						LAST_VALUE(c.flight_time) OVER (PARTITION BY t.id ORDER BY c.num ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS flight_time
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
    
    @classmethod
    def get_coupones(cls, ticket_id: int):
        return f"""
        SELECT 
            c.departure, 
            c.destination,
            c.fare,
            c.num,
            t.type,
            c.flight_time,
            c.flight_time + (c.duration * INTERVAL '1 minute') AS destination_time,
            CONCAT(FLOOR(duration / 60), 'ч ', MOD(duration, 60), 'м') AS time
        FROM 
            coupones c
        JOIN 
            tickets t ON c.ticket = t.id
        WHERE
            t.id = {ticket_id}
        order by c.num
        """
    
    @classmethod
    def get_user_tickets(cls, user_id: int, role: int):
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
						LAST_VALUE(c.flight_time) OVER (PARTITION BY t.id ORDER BY c.num ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS flight_time
                    FROM 
                        tickets t
                    JOIN 
                        coupones c 
                        ON t.id = c.ticket
                    JOIN 
                        airlines a
                        ON a.id = t.airline
					JOIn sale_ticket st
						on st.ticket=t.id
                    {'JOIN clients cl ON cl.id = st.client WHERE cl.id = ' + str(user_id) if role == 2 else 'JOIN cashiers cash ON cash.id = st.cashier WHERE cash.id = ' + str(user_id)}

                ) AS subquery
            ORDER BY 
                subquery.ticket_id, subquery.num;
        """


