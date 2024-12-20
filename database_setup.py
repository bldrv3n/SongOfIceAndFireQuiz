import csv
from mysql.connector import connect, Error

def create_database():
    try:
        with connect(
                host='localhost',
                user='root',
<<<<<<< HEAD
                password='my_password') as connection:
=======
                password='your_password') as connection:
>>>>>>> 59117b10ffa23559e3618429fe93a484306550a6
            with connection.cursor() as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS quiz_database")
                connection.commit()
            print(f'Database connection established:', connection)
    except Error as e:
        print(e)

def create_tables():

    try:
        with connect(
                host='localhost',
                user='root',
<<<<<<< HEAD
                password='my_password',
=======
                password='your_password',
>>>>>>> 59117b10ffa23559e3618429fe93a484306550a6
                database='quiz_database',) as connection:
            with connection.cursor() as cursor:
                create_questions_table_query = """
                CREATE TABLE IF NOT EXISTS questions(
                    question_id INT AUTO_INCREMENT PRIMARY KEY,
                    question VARCHAR(500),
                    A VARCHAR(255),
                    B VARCHAR(255),
                    C VARCHAR(255),
                    D VARCHAR(255),
                    correct_answer VARCHAR(1)
                )
                """
                cursor.execute(create_questions_table_query)
                
                create_statistics_table_query = """
                CREATE TABLE IF NOT EXISTS statistics(
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(100),
                    scores INT
                )
                """
                cursor.execute(create_statistics_table_query)
                connection.commit()
            print(f'Tables created successfully:', connection)
    except Error as e: 
        print(e)


def load_csv_file_to_database(csv_file_path):
<<<<<<< HEAD
    csv_file_path = 'C:\\your\\file\\path\\\\questions.csv'
=======
    csv_file_path = 'put:\\the\\file\\path\\here'
>>>>>>> 59117b10ffa23559e3618429fe93a484306550a6
    print(f'Loading csv data from {csv_file_path}.')
    try:
        with open(csv_file_path, 'r', encoding = 'utf-8') as file:
            reader = csv.DictReader(file, quotechar="'")
            questions = [row for row in reader]

        with connect(
                host='localhost',
                user='root',
<<<<<<< HEAD
                password='my_password',
=======
                password='your_password',
>>>>>>> 59117b10ffa23559e3618429fe93a484306550a6
                database='quiz_database',) as connection:
            with connection.cursor() as cursor:
                insert_questions_query = """
                INSERT INTO questions (question, A, B, C, D, correct_answer)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                for question in questions:
                    cursor.execute(insert_questions_query, (question['question'], question['A'], question['B'], question['C'], question['D'], question['correct_answer']))
                connection.commit()
            print(f'Data from csv file loaded successfully.')
    except Error as e:
        print(e)

<<<<<<< HEAD
 
=======
 
>>>>>>> 59117b10ffa23559e3618429fe93a484306550a6
