"""
Запросы к бд
"""

class AirlinesQueries:
    @classmethod
    def get_all(cls):
        return f"""
        SELECT * FROM Airlines
        """

    @classmethod
    def add_airline(cls, name: str, city: str, street: str, house: str):
        return f"""
        SELECT add_airline('{name}', '{city}', '{street}', '{house}')
        """

    @classmethod
    def update_airline(cls, id: int, name: str, city: str, street: str, house: str):
        return f"""
        SELECT update_airline({id}, '{name}', '{city}', '{street}', '{house}')
        """

    @classmethod
    def delete_airline(cls, id: int):
        return f"""
        SELECT delete_airline({id})
        """

class TicketOfficesQueries:
    def get_all(cls):
        return f"""
        SELECT * FROM ticket_offices
        """

    @classmethod
    def add_ticket_office(cls, city: str, street: str, house: str):
        return f"""
        SELECT add_ticket_office('{city}', '{street}', '{house}')
        """

    @classmethod
    def update_ticket_office(cls, id: int, city: str, street: str, house: str):
        return f"""
        SELECT update_ticket_office({id}, '{city}', '{street}', '{house}')
        """

    @classmethod
    def delete_ticket_office(cls, id: int):
        return f"""
        SELECT delete_ticket_office({id})
        """

class CashiersQueries:
    def get_all(cls):
        return f"""
        SELECT * FROM Cashiers
        """    

    @classmethod
    def add_cashier(cls, ticket_office: int, first_name: str, last_name: str, middle_name: str):
        return f"""
        SELECT add_cashier({ticket_office}, '{first_name}', '{last_name}', '{middle_name}')
        """

    @classmethod
    def update_cashier(cls, id: int, ticket_office: int, first_name: str, last_name: str, middle_name: str):
        return f"""
        SELECT update_cashier({id}, {ticket_office}, '{first_name}', '{last_name}', '{middle_name}')
        """

    @classmethod
    def delete_cashier(cls, id: int):
        return f"""
        SELECT delete_cashier({id})
        """

class ClientsQueries:
    def get_all(cls):
        return f"""
        SELECT * FROM Clients
        """   

    @classmethod
    def add_client(cls, passport_number: int, passport_series: int, first_name: str, last_name: str, middle_name: str):
        return f"""
        SELECT add_client({passport_number}, {passport_series}, '{first_name}', '{last_name}', '{middle_name}')
        """

    @classmethod
    def update_client(cls, id: int, passport_number: int, passport_series: int, first_name: str, last_name: str, middle_name: str):
        return f"""
        SELECT update_client({id}, {passport_number}, {passport_series}, '{first_name}', '{last_name}', '{middle_name}')
        """

    @classmethod
    def delete_client(cls, id: int):
        return f"""
        SELECT delete_client({id})
        """

class TicketsQueries:
    def get_all(cls):
        return f"""
        SELECT * FROM Tickets
        """ 

    @classmethod
    def add_ticket(cls, ticket_type: int, airline: int):
        return f"""
        SELECT add_ticket({ticket_type}, {airline})
        """

    @classmethod
    def update_ticket(cls, id: int, ticket_type: int, airline: int):
        return f"""
        SELECT update_ticket({id}, {ticket_type}, {airline})
        """

    @classmethod
    def delete_ticket(cls, id: int):
        return f"""
        SELECT delete_ticket({id})
        """

class CouponesQueries:
    def get_all(cls):
        return f"""
        SELECT * FROM Coupones
        """ 

    @classmethod
    def add_coupone(cls, departure: str, destination: str, fare: float, client: int, ticket: int):
        return f"""
        SELECT add_coupone({departure}, {destination}, {fare}, {client}, {ticket})
        """

    @classmethod
    def update_coupone(cls, id: int, departure: str, destination: str, fare: float, client: int, ticket: int):
        return f"""
        SELECT update_coupone({id}, {departure}, {destination}, {fare}, {client}, {ticket})
        """

    @classmethod
    def delete_coupone(cls, id: int):
        return f"""
        SELECT delete_coupone({id})
        """

class SaleTicketQueries:
    def get_all(cls):
        return f"""
        SELECT * FROM sale_ticket
        """ 

    @classmethod
    def add_sale_ticket(cls, ticket: int, cashier: int, client: int, sale_date: str):
        return f"""
        SELECT add_sale_ticket({ticket}, {cashier}, {client}, '{sale_date}')
        """

    @classmethod
    def update_sale_ticket(cls, id: int, ticket: int, cashier: int, client: int, sale_date: str):
        return f"""
        SELECT update_sale_ticket({id}, {ticket}, {cashier}, {client}, '{sale_date}')
        """

    @classmethod
    def delete_sale_ticket(cls, id: int):
        return f"""
        SELECT delete_sale_ticket({id})
        """

class AdminQueries:
    @classmethod
    def add_admin(cls, username: str, role: int):
        return f"""
        SELECT add_admin('{username}', {role})
        """

    @classmethod
    def update_admin(cls, id: int, username: str, role: int):
        return f"""
        SELECT update_admin({id}, '{username}', {role})
        """

    @classmethod
    def delete_admin(cls, id: int):
        return f"""
        SELECT delete_admin({id})
        """