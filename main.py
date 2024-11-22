from connection import Connection #import Connection class from connection file
from questions import QuestionGenerator # import QuestionGenerator class from question file
from answer import AnswerChecker #imports AnswerChecker class from answer file
from quiz_module import test_quiz ##imports test_quiz func 
from rich.console import Console  #rich library is used for frames and nice visualization
from rich.panel import Panel  #rich library is used for frames and nice visualization



console = Console()

def main ():
    test_quiz ()

if __name__ == '__main__':
    main ()

def print_question(question):
    panel = Panel(question, title = 'Question', expand = False)
    console.print(panel)

def print_answer(answers):
    for option, text in answers.items(): #answer.items() returns a list of key-value pairs in the answers dictionary, option - each key (a, b, c,d), text - corresponding value (the answer text)
        panel = Panel(text, title = f'Option {option}', expand = False)
        console.print(panel)

#define database configuration, including the host, user, password, and database name. im replacing it with kwargs
db_settings = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'SarutobiHokage3',
    'database' : 'password'
}

connection = Connection(**db_settings) #create connection object with DB settings
connection.connect() #method is called to establish the connection to MySQL database


question_generator = QuestionGenerator(connection) #create question generator object
answer_checker = AnswerChecker(connection) #create answer checker object

question_generator.generate_question() #generates and shows question/ the method is called to fetch and display a random question from DB


#simulate user input
while True:
    user_input = input ('Enter your answer (A, B, C, D) or ''quit'' to exit: ')

    if answer_checker.check_for_qiut(user_input):
        print('Goodbye! See you next time.')
        break

    elif answer_checker.check_user_input(user_input):
        question_id = question_generator.get_question_id()
        if answer_checker.is_answer_correct(question_id):
            print('Well done!')
        else:
            print('Be attentive!')
            
    else:
        print('Invalid input! Please enter (A, B, C, D) or ''quit''.')
