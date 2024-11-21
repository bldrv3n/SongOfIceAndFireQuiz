from connection import Connection

class AnswerChecker:
    def __init__ (self, db_connection): #initializes the AnswerChecker class with a database connection and a private variable _answer to store the users input
        self.db_connection = db_connection
        self.answer = None

    def check_user_input(self, user_input): #checks if the inout is one of the valid answers and if it is - store it
        valid_answers = ['A', 'B', 'C', 'D']
        if user_input in valid_answers:
            self.answer = user_input
            return True
        return False
    
    def is_answer_correct(self, question_id): #fetches the correct answer from the database for the given question id and compares it with the users answer
        if not self.db_connection.is_connected():
            self.show_no_connection()
            return False
        
        query = f'SELECT correct_answer FROM questions WHERE id = {question_id}'
        cursor = self.db_connection.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            correct_answer = result[0]
            return self._answer == correct_answer
        return False
    
        # pass

    def check_for_qiut(self, user_input): #checks if the user input is 'quit'
        if user_input.lower() == 'quit':
            confirmation = input("You chose to quit. Are you sure? Enter: {Y}/{N}: ") 
            return confirmation.lower() == 'y'

    def show_no_connection(self): #prints the message if there is no database connection
        print('No connection to the database')