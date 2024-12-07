import os
from pathlib import Path
import psycopg2
from abc import ABC, abstractmethod

BASE_DIR = Path(__file__).resolve().parent.parent

class Database(ABC):
    def __init__(self, driver) -> None:
        self.driver = driver
    
    @abstractmethod
    def connect_to_database(self):
        pass
    
    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()

class PgDatabase(Database):
    def __init__(self) -> None:
        super().__init__(psycopg2)
    
    def connect_to_database(self):
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
