class AllEmailsQueries:
    @classmethod
    def get_all(cls, email: str):
        return f"""
            select email from (
                select email from admin
                union all	
                select email from cashiers
                union all 
                select email from clients
            ) as all_emails
            where email = '{email}'
        """

class Auth:
    @classmethod
    def register_client(cls, pasport_num, passport_series, first_name, last_name, middle_name, password, email):
        return f"""
        INSERT INTO clients (
            passport_number,
            passport_series,
            first_name,
            last_name,
            middle_name,
            password,
            email) 
        VALUES
        ('{pasport_num}', '{passport_series}', '{first_name}', '{last_name}', '{middle_name}', '{password}','{email}')
        RETURNING id, role;
        """
    
    @classmethod
    def login(cls, email):
        return f"""
        select email, password, role, id
          from (
                select email, password, role, id from admin
                union all	
                select email, password, role, id from cashiers
                union all 
                select email, password, role, id from clients
            ) as all_emails
            where email = '{email}'
        """

