import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException


from settings import DATABASE_CONFIG

class Connect:
    @staticmethod
    def get_db_connection():
        try:
            conn = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
            return conn
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Произошла ошибка при подключении к базе данных: {str(e)}")
        
    @classmethod
    def execute(cls, query: str):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            return rows
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Произошла ошибка при выполнении запроса: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    
