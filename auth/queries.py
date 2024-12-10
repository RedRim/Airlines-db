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
        """
    
    @classmethod
    def login_client(cls, email):
        return f"""
        select email, password
        from clients
        where 
        email='{email}'
        """

