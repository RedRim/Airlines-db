import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException


from settings import DATABASE_CONFIG

class Connect:
    @staticmethod
    def get_db_connection():
        try:
            conn = psycopg2.connect(**DATABASE_CONFIG)
            return conn
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Произошла ошибка при подключении к базе данных: {str(e)}")
        
    @classmethod
    def fetchall(cls, query: str):
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
    
    @classmethod
    def fetchone(cls, query: str):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchone()
            conn.commit()
            return rows
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Произошла ошибка при выполнении запроса: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    
    @classmethod
    def execute(cls, query: str):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Произошла ошибка при выполнении запроса: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    
