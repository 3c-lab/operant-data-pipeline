import psycopg2
from config import *

class Pipeline(object):

    def __init__(self):
        self.conn, self.cur = self.connect_db()

    @staticmethod
    def connect_db():        
        try:
            conn = psycopg2.connect(user=DATABASE_USERNAME,
                                    password=DATABASE_PASSWORD,
                                    host=DATABASE_HOST,
                                    port=DATABASE_PORT,
                                    database=DATABASE_NAME,
                                    options=f'-c search_path={DATABASE_SCHEMA}'
                                    )
            cur = conn.cursor()
        
        except Exception as error:
            print(f'Cannot connect to DB due to "{error}" error')

        return (conn, cur)