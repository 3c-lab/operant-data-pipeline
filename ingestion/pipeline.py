import config
import psycopg2

class Pipeline(object):

    def __init__(self):
        self.conn, self.cur = self.connect_db()

    @staticmethod
    def connect_db():        
        try:
            conn = psycopg2.connect(user=config.DATABASE_USERNAME,
                                    password=config.DATABASE_PASSWORD,
                                    host=config.DATABASE_HOST,
                                    port=config.DATABASE_PORT,
                                    database=config.DATABASE_NAME,
                                    options=f'-c search_path={config.DATABASE_SCHEMA}'
                                    )
            cur = conn.cursor()
        
        except Exception as error:
            print(f'Cannot connect to DB due to "{error}" error')

        return (conn, cur)