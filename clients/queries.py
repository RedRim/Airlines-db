class Tickets:
    @classmethod
    def get_all_client_tickets(cls, client_id: int):
        return f"""
        select 
            tickets.id 
        from 
            sale_ticket
        join tickets
            on sale_ticket.ticket=tickets.id
        left join clients 
            on sale_ticket.client=clients.id
        where clients.id = {client_id}
        """