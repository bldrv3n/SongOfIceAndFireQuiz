import pandas as pd
from mysql.connector import connect, Error

db_settings = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'password',
    'database' : 'SongOfIceAndFireQuiz'
}

def create_database():
    try:
        with connect(
                host='localhost',
                user='root',
                password='password') as connection:
            with connection.cursor() as cursor:
                cursor.execute('CREATE DATABASE SongOfIceAndFireQuiz')
                connection.commit()
            print(connection)
    except Error as e:
        print(e)


def create_tables():
    try:
        with connect(
                host='localhost',
                user='root',
                password='password',
                database = 'SongOfIcaAndFireQuiz') as connection:
            with connection.cursor() as cursor:
                create_questions_table_sql = '''
                CREATE TABLE questions(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    question VARCHAR(500),
                    A VARCHAR (255),
                    B VARCHAR (255),
                    C VARCHAR (255),
                    D VARCHAR (255),
                    correct_answer CHAR (1)
                )
                '''
                with connection.cursor() as cursor:
                    cursor.execute(create_questions_table_sql)
                    connection.commit()
                print('Table created')
    except Error as e:
        print(e)



# with open('questions.csv', 'r') as file:
#     questions = csv.load(file)
def import_csv(c:/SoIF quiz):
    try:
        data = pd.read_csv(c:/SoIF quiz)
        print('csv file read successfully')  
        return data
    except Exception as e:
        print(f'Error reading csv file: {e}')
        return None

def insert_data_to_db(data):
    if data is not None:
        try:
            with connect(
                    host='localhost',
                    user='root',
                    password='password',
                    database = 'SongOfIcaAndFireQuiz') as connection:
                with connection.cursor() as cursor:
                    insert_questions_query = '''
                    INSERT INTO questions (id, question, A, B, C, D, correct_answer)
                    VALUES (%s, %s, %s, %s);
                    '''
                    for question in questions:
                        cursor.execute(insert_questions_query, tuple(row))
                    connection.commit()
                print('Data inserted successfully')
        except Error as e:
            print(e) 
    else:
        print('No data to be inserted')
            

if __name__ == '__main__':
    create_database()
    create_tables()
    csv_file_path = 'c:/SoIF quiz'
    data = import_csv(csv_file_path)
    insert_data_to_db(data)




#db connection settings
# db_settings = {
#     'host' : 'localhost',
#     'user' : 'root',
#     'password' : 'password',
#     'database' : 'SongOfIceAndFireQuiz'
# }

