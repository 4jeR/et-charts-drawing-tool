import psycopg2
import atexit



class DataBaseConnector:
    def __init__(self, db_name='et_charts', username='ajer', password='', ip_address='localhost', port='5432'):
        self.db_name = db_name
        self.user = username
        self.password = password
        self.ip_address = ip_address
        self.port = port
        atexit.register(self.disconnect)

    
    def db_safe(func):
        def wrapper(self):
            try:
                return func(self)
            except (Exception, psycopg2.DatabaseError) as error:
                print(f'[{self.__class__.__name__}] - {error}')
                #self.connection.close()
        return wrapper


    @db_safe
    def connect(self):
        self.connection = psycopg2.connect(
            database = self.db_name,
            user = self.user,
            password = self.password,
            host = self.ip_address,
            port = self.port
        )
        self.cursor = self.connection.cursor()
        print(f'Succesfully made connection with the /{self.db_name}/ database!')
        return None
    
    def insert_data(self, table_name):
        pass
    


    def refresh(self):
        pass

    @db_safe
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print(f'Succesfully closed connection to the /{self.db_name}/database !')
        return None

    @db_safe
    def get_db_data(table_name):
        self.cursor.execute(f'SELECT * FROM {table_name}')
        conn.commit()
        

