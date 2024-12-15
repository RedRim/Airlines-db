from fastapi import HTTPException

class NotAuthenticatedClient(HTTPException):
    def __init__(self, detail: str = "Client is not authenticated"):
        super().__init__(status_code=401, detail=detail)

class NotAuthenticatedCashier(HTTPException):
    def __init__(self, detail: str = "Cashier is not authenticated"):
        super().__init__(status_code=401, detail=detail)

class NotAuthenticatedAdmin(HTTPException):
    def __init__(self, detail: str = "Admin is not authenticated"):
        super().__init__(status_code=401, detail=detail)