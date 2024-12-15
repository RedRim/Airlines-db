-- Функции для таблицы "Airlines"
CREATE OR REPLACE FUNCTION add_airline(p_name varchar, p_city varchar, p_street varchar, p_house varchar) 
RETURNS bigint AS $$
DECLARE
    new_id bigint;
BEGIN
    INSERT INTO airlines (name, city, street, house) 
    VALUES (p_name, p_city, p_street, p_house) RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_airline(p_id bigint, p_name varchar, p_city varchar, p_street varchar, p_house varchar)
RETURNS bigint AS $$
BEGIN
    UPDATE airlines 
    SET name = p_name, city = p_city, street = p_street, house = p_house
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_airline(p_id bigint) 
RETURNS bigint AS $$
BEGIN
    DELETE FROM airlines WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

-- Функции для таблицы "Ticket_offices"
CREATE OR REPLACE FUNCTION add_ticket_office(p_city varchar, p_street varchar, p_house varchar) 
RETURNS bigint AS $$
DECLARE
    new_id bigint;
BEGIN
    INSERT INTO ticket_offices (city, street, house) 
    VALUES (p_city, p_street, p_house) RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_ticket_office(p_id bigint, p_city varchar, p_street varchar, p_house varchar)
RETURNS bigint AS $$
BEGIN
    UPDATE ticket_offices 
    SET city = p_city, street = p_street, house = p_house
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_ticket_office(p_id bigint) 
RETURNS bigint AS $$
BEGIN
    DELETE FROM ticket_offices WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

-- Функции для таблицы "Cashiers"
CREATE OR REPLACE FUNCTION add_cashier(
p_ticket_office bigint,
p_first_name varchar, 
p_last_name varchar,
p_middle_name varchar,
p_password varchar, 
p_email varchar,
p_role integer) 
RETURNS bigint AS $$
DECLARE
    new_id bigint;
BEGIN
    INSERT INTO cashiers (ticket_office, first_name, last_name, middle_name, password, email, role) 
    VALUES (p_ticket_office, p_first_name, p_last_name, p_middle_name, p_password, p_email, p_role) RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;ql;

CREATE OR REPLACE FUNCTION update_cashier(
p_id bigint, 
p_ticket_office bigint, 
p_first_name varchar, 
p_last_name varchar,
p_middle_name varchar,
p_email varchar,
p_role integer)
RETURNS bigint AS $$
BEGIN
    UPDATE cashiers 
    SET ticket_office = p_ticket_office, 
		first_name = p_first_name, 
		last_name = p_last_name, 
		middle_name = p_middle_name,
		email = p_email,
		role = p_role
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_cashier(p_id bigint) 
RETURNS bigint AS $$
BEGIN
    DELETE FROM cashiers WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

-- Функции для таблицы "Clients"
CREATE OR REPLACE FUNCTION add_client(p_email varchar, p_password varchar, p_passport_number bigint, p_passport_series bigint, p_first_name varchar, p_last_name varchar, p_middle_name varchar) 
RETURNS bigint AS $$
DECLARE
    new_id bigint;
BEGIN
    INSERT INTO clients (email, password, passport_number, passport_series, first_name, last_name, middle_name) 
    VALUES (p_email, p_password, p_passport_number, p_passport_series, p_first_name, p_last_name, p_middle_name) RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_client(p_id integer, p_email varchar, p_passport_number integer, p_passport_series integer, p_first_name varchar, p_last_name varchar, p_middle_name varchar, p_role integer)
RETURNS bigint AS $$
BEGIN
    UPDATE clients 
    SET email = p_email, passport_number = p_passport_number, passport_series = p_passport_series, first_name = p_first_name, last_name = p_last_name, middle_name = p_middle_name, role = p_role
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_client(p_id bigint) 
RETURNS bigint AS $$
BEGIN
    DELETE FROM clients WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

-- Функции для таблицы "Tickets"
CREATE OR REPLACE FUNCTION add_ticket(p_type bigint, p_airline bigint) 
RETURNS bigint AS $$
DECLARE
    new_id bigint;
BEGIN
    INSERT INTO tickets (type, airline) 
    VALUES (p_type, p_airline) RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_ticket(p_id bigint, p_type bigint, p_airline bigint)
RETURNS bigint AS $$
BEGIN
    UPDATE tickets 
    SET type = p_type, airline = p_airline
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_ticket(p_id bigint) 
RETURNS bigint AS $$
BEGIN
    DELETE FROM tickets WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;


-- Функции для таблицы "Coupones"
CREATE OR REPLACE FUNCTION add_coupone(
    p_departure VARCHAR, 
    p_destination VARCHAR, 
    p_fare NUMERIC, 
    p_ticket integer,
	p_num integer,
	p_flight_time timestamp,
	p_duration integer
) RETURNS integer AS $$
DECLARE
    new_id integer;
BEGIN
    INSERT INTO coupones (departure, destination, fare, ticket, num, flight_time, duration)
    VALUES (p_departure, p_destination, p_fare, p_ticket, p_num, p_flight_time, p_duration)
    RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_coupone(
    p_id integer,
    p_departure VARCHAR, 
    p_destination VARCHAR, 
    p_fare NUMERIC, 
    p_ticket integer,
	p_num integer,
	p_flight_time timestamp,
	p_duration integer
) RETURNS integer AS $$
BEGIN
    UPDATE coupones 
    SET 
        departure = p_departure, 
        destination = p_destination, 
        fare = p_fare, 
        ticket = p_ticket,
		num = p_num,
		flight_time = p_flight_time,
		duration = p_duration
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION delete_coupone(p_id BIGINT) RETURNS BIGINT AS $$
BEGIN
    DELETE FROM coupones WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

-- Функции для таблицы "Sale_ticket"
CREATE OR REPLACE FUNCTION add_sale_ticket(p_ticket bigint, p_cashier bigint, p_client bigint, p_sale_date date) 
RETURNS bigint AS $$
DECLARE
    new_id bigint;
BEGIN
    INSERT INTO sale_ticket (ticket, cashier, client, sale_date) 
    VALUES (p_ticket, p_cashier, p_client, p_sale_date) RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_sale_ticket(p_id bigint, p_ticket bigint, p_cashier bigint, p_client bigint, p_sale_date date)
RETURNS bigint AS $$
BEGIN
    UPDATE sale_ticket 
    SET ticket = p_ticket, cashier = p_cashier, client = p_client, sale_date = p_sale_date
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_sale_ticket(p_id bigint) 
RETURNS bigint AS $$
BEGIN
    DELETE FROM sale_ticket WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

-- Функции для таблицы "Admin"
CREATE OR REPLACE FUNCTION add_admin(p_username varchar, p_role bigint) 
RETURNS bigint AS $$
DECLARE
    new_id bigint;
BEGIN
    INSERT INTO admin (username, role) 
    VALUES (p_username, p_role) RETURNING id INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_admin(p_id bigint, p_username varchar, p_role bigint)
RETURNS bigint AS $$
BEGIN
    UPDATE admin 
    SET username = p_username, role = p_role
    WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_admin(p_id bigint) 
RETURNS bigint AS $$
BEGIN
    DELETE FROM admin WHERE id = p_id;
    RETURN p_id;
END;
$$ LANGUAGE plpgsql

