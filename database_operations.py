from mysql.connector import connect, Error
import random
from colorama import init, Fore, Style

def from_table_questions(question_id):
    try:
        with connect(
                host="localhost",
                user="root",
                password="my_password",
                database="quiz_database") as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT question_id, question, A, B, C, D, correct_answer FROM questions WHERE question_id = %s', (question_id,))
                result = cursor.fetchone()
                if result:
                    return {
                        'question_id': result[0],
                        'question': result[1],
                        'A': result[2],
                        'B': result[3],
                        'C': result[4],
                        'D': result[5],
                        'correct_answer': result[6]
                    }
                else:
                    return None
    except Error as e:
        print(Fore.RED + f'DB connection is not established.' + Style.RESET_ALL)

def from_table_statistics(user_name):
    try:
        with connect(
                host="localhost",
                user="root",
                password="my_password",
                database="quiz_database") as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT user_id, user_name, scores FROM statistics WHERE user_name = %s', (user_name,))
                result = cursor.fetchone()
                if result:
                    return {
                        'user_id': result[0],
                        'user_name': result[1],
                        'scores': result[2]
                    }
                else:
                    return None
    except Error as e:
        print(Fore.RED + 'Error getting statistics' + Style.RESET_ALL)

def get_unique_random_question_id(asked_questions):
    try:
        with connect(
                host="localhost",
                user="root",
                password="my_password",
                database = 'quiz_database') as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT question_id FROM questions ORDER BY RAND() LIMIT 1')
                question_ids = cursor.fetchall()
                question_ids = [qid[0] for qid in question_ids if qid[0] not in asked_questions]
                if not question_ids:
                    return None
                return random.choice(question_ids)
    except Error as e:
        print(e)
        return None
        
def save_score(nickname, score): 
    try: 
        with connect( 
                host="localhost", 
                user="root", 
                password="my_password", 
                database="quiz_database") as connection: 
            with connection.cursor() as cursor: 
             
                cursor.execute('SELECT user_id, scores FROM statistics WHERE user_name = %s', (nickname,)) 
                result = cursor.fetchone() 
                
                if result: 
                    user_id, current_score = result 
                    new_score = current_score + score 
                    cursor.execute('UPDATE statistics SET scores = %s WHERE user_id = %s', (new_score, user_id)) 
                    print(Fore.GREEN + 'Score updated successfully' + Style.RESET_ALL) 
                else: 
                    cursor.execute('INSERT INTO statistics (user_name, scores) VALUES (%s, %s)', (nickname, score)) 
                    print(Fore.GREEN + 'Score saved successfully' + Style.RESET_ALL) 
                    
                connection.commit() 
    except Error as e: 
        print(Fore.RED + f'Error saving score: {e}' + Style.RESET_ALL)


