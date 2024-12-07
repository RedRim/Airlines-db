-- Удаление всех таблиц
-- DO $$ DECLARE
--     r RECORD;
-- BEGIN
--     FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
--         EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
--     END LOOP;
-- END $$;

CREATE TABLE IF NOT EXISTS airlines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    house VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS ticket_offices (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    house VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS cashiers (
    id SERIAL PRIMARY KEY,
    ticket_office BIGINT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50) NOT NULL,

    CONSTRAINT cashiers_fk1 FOREIGN KEY (ticket_office) REFERENCES ticket_offices (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    passport_number BIGINT NOT NULL CHECK (passport_number > 0),
    passport_series BIGINT NOT NULL CHECK (passport_series > 0),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    type BIGINT NOT NULL CHECK (type > 0),
    airline BIGINT NOT NULL,

    CONSTRAINT tickets_fk1 FOREIGN KEY (airline) REFERENCES airlines (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS coupones (
    id SERIAL PRIMARY KEY,
    departure VARCHAR(100) NOT NULL,
	destination VARCHAR(100) NOT NULL,
    fare NUMERIC(10, 2) NOT NULL CHECK (fare >= 0),
    client BIGINT NOT NULL,
    ticket BIGINT NOT NULL,

	CHECK (departure <> destination),
    CONSTRAINT coupones_fk1 FOREIGN KEY (client) REFERENCES clients (id) ON DELETE CASCADE,
    CONSTRAINT coupones_fk2 FOREIGN KEY (ticket) REFERENCES tickets (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sale_ticket (
    id SERIAL PRIMARY KEY,
    ticket BIGINT NOT NULL,
    cashier BIGINT NOT NULL,
    client BIGINT NOT NULL,
    sale_date DATE NOT NULL CHECK (sale_date <= CURRENT_DATE),

    CONSTRAINT sale_ticket_fk1 FOREIGN KEY (ticket) REFERENCES tickets (id) ON DELETE CASCADE,
    CONSTRAINT sale_ticket_fk2 FOREIGN KEY (cashier) REFERENCES cashiers (id) ON DELETE CASCADE,
    CONSTRAINT sale_ticket_fk3 FOREIGN KEY (client) REFERENCES clients (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    role BIGINT NOT NULL CHECK (role >= 0)
);
