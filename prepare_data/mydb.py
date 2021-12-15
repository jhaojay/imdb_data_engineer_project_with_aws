import psycopg2
from config import config


class MyDB:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)

            # create a cursor
            self.cur = self.conn.cursor()
            print('Connection opened successfully.')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
            
    def query(self, query, value=None, fetch=False):
        if self.cur and self.conn:
            try:
                if value:
                    self.cur.execute(query, value)
                else:
                    self.cur.execute(query)

                if fetch:
                    records = [row for row in self.cur.fetchall()]
                    return records

                self.conn.commit()
            except Exception as e:
                print(e)
                self.close()
        else:
            print(f"{type(self).__name__} is not connected.")
    
    def status_message(self):
        if self.cur and self.conn:
            return self.cur.statusmessage
        else:
            return None
                
    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print(f"{type(self).__name__} connection closed.")
