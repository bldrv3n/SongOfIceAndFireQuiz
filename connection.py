from mysql.connector import connect, Error

class Connection: #iniatilize connection parameters and set self.connection to None
    def __init__(self, **kwargs):
        self.db_settings = kwargs
        self.connection = None

    def connect(self): #attempt to connect to the database and prints a confirmation message. in case of failure it prints an error
        try: 
            self.connection = connect(**self.db_settings)
            print('Connected to database')
        except Error as e:
            print(f'Error: {e}')
    
    def is_connected(self): #check if the connection is established and active
        return self.connection is not None and self.connection.is_connected()