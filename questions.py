from connection import Connection #import Connection class from its file 
import random

class QuestionGenerator: #initialize the class with the database connection object
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def generate_question(self): #check the connection, generate a random question id and fetches the question
        if not self.db_connection.is_connected():
            self.show_no_connection()
            return
        question_id = self.get_question_id()
        self.request_question(question_id)

    def show_question(self, question, options): #display the question and answer options
        print(f'Question: {question}')
        for key, value in options.items():
            print(f'{key}: {value}')

    def show_no_connection(self): #method to print a message if there is no database connection
        print('No connection to the database')

    def get_question_id(self): #to fetch a random question id from the database
        query = 'SELECT id FROM questions ORDER BY RANDOM() LIMIT 1'
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone() #what is that
        return result[0] if result else None
    
    def request_question(self, question_id): #fetches the question and its options from the database using the question id and calls show_question() to display question and answers
        query = f'SELECT question, A, B, C, D, correct_answer FROM questions WHERE id = {question_id}'
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone() #what is that
        if result:
            question, A, B, C, D, correct_answer = result 
            options = {'A': A, 'B': B, 'C': C, 'D': D}
            self.show_question(question, options)

