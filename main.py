import pymysql
from pymysql import connect, MySQLError 
from rich.console import Console
from rich.panel import Panel
from colorama import init, Fore, Style

console = Console() 
init() 

db_settings = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SarutobiHokage3',
    'database': 'quiz_db'
}

connection = None
try:
    connection = connect(
            host = db_settings['host'],
            user = db_settings['user'],
            password = db_settings['password'],
            database = db_settings['database']
    )
    if connection: 
        print('Successfil connection to MySQL DB')
except MySQLError as e:
    print(f'Error connecting to DB: {e}')

def from_table_questions(id): 
    if connection:
        cursor = connection.cursor() 
        cursor.execute(f'SELECT id, question, A, B, C, D, correct_answer FROM questions WHERE id = %s', (id,)) 
        result = cursor.fetchone() 
        cursor.close() 
        if result: 
            return { 
                'id': result[0], 
                'question': result[1], 
                'A': result[2], 
                'B': result[3], 
                'C': result[4], 
                'D': result[5], 
                'correct_answer': result[6] } 
        else: 
            return None
    else:
        print(Fore.RED + '1DB connection is not established.' + Style.RESET_ALL)
        return None
    
def from_table_stats(user_id): 
    if connection:
        cursor = connection.cursor() 
        cursor.execute(f'SELECT user_id, nickname, scores FROM stats WHERE user_id = %s', (user_id,)) 
        result = cursor.fetchone() 
        cursor.close() 
        if result: 
            return { 
                'user_id': result[0], 
                'nickname': result[1], 
                'scores': result[2] 
                } 
        else: 
            return None
    else:
        print(Fore.RED + '2DB connection is not established.' + Style.RESET_ALL)
        return None
 
def print_question(question): 
    console.print(Panel(question, title = 'Question')) 

def print_answers(answers):
    for option, text in answers.items():  
        console.print(Panel(text, title = f'Option {option}')) 

def quiz():  
    def get_random_question_id(): 
        if connection:
            cursor = connection.cursor() 
            cursor.execute('SELECT id FROM questions ORDER BY RAND() LIMIT 1') 
            result = cursor.fetchone() 
            cursor.close() 
            return result[0] if result else None
        else:
            print(Fore.RED + '3DB connection is not established.' + Style.RESET_ALL)
            return None

    def fetch_question(id):
        return from_table_questions(id)

    def interaction_with_quiz():
        lives = 3
        score = 0
        
        while lives > 0: 
            id = get_random_question_id() 
            if id is None: 
                print(Fore.RED + 'No quesstion available.' + Style.RESET_ALL) 
                break

            question_data = fetch_question(id)
            if question_data is None:
                print(Fore.RED + 'Question not found.' + Style.RESET_ALL)
                break
            
            print_question(question_data['question']) 
            
            answers = { 
                'A': question_data['A'], 
                'B': question_data['B'], 
                'C': question_data['C'], 
                'D': question_data['D'] 
                }
            
            print_answers(answers)
        
            while True:
                answer = input('Your answer (A/B/C/D) or \'quit\' to exit quiz: ').lower()
                if answer in ['a', 'b', 'c', 'd', 'quit']:
                    break
                else:
                    print(Fore.RED + 'Invalid input. Choose the correct answer (A, B, C, D) or type \'quit\' to exit the quiz.' + Style.RESET_ALL)

            if answer == 'quit':
                confirm_quit = input('Are you sure you want to exit the quiz?\nConfirm by entering \'Y\' for yes or \'N\' for no: ').lower()
                if confirm_quit == 'y':
                    print(Fore.YELLOW +  'Thanks for playing. See you next time!' + Style.RESET_ALL)
                    break
                else:
                    print(Fore.YELLOW +'Good that you decided to stay!\n' + Style.RESET_ALL)
                    continue

            if answer == question_data['correct_answer'].lower():
                print(Fore.GREEN + 'Well done! You got 1 point. \n' + Style.RESET_ALL)
                score += 1
            else:
                print(Fore.RED + f'Wrong.\nThe correct answer is {question_data["correct_answer"]}\n' + Style.RESET_ALL)
                lives -= 1
                if lives == 0:
                    retry = input(Fore.CYAN + 'You lost. Want to try again? Enter \'Y\' for yes and \'N\' for no:' + Style.RESET_ALL).lower()
                    if retry == 'y':
                        print(Fore.GREEN + 'Good choice. Restarting the quiz.\n' + Style.RESET_ALL)
                        return interaction_with_quiz()
                    elif retry == 'n':
                        print(Fore.YELLOW + 'Thanks for playing. See you next time!' + Style.RESET_ALL)
                        break
                    else:
                        print(Fore.RED + 'Invalid input. Exiting the quiz.' + Style.RESET_ALL)
                        return

        print(Fore.CYAN + f'Your final score is: {score}' + Style.RESET_ALL)

    interaction_with_quiz()

def main():
    quiz()

if __name__ == '__main__':
    main()

if connection:
    connection.close()
    print('MySQL connection is closed')