from rich.console import Console
from rich.panel import Panel
from colorama import init, Fore, Style
import database_setup
from database_operations import from_table_questions, from_table_statistics, get_unique_random_question_id, save_score
from timer import QuizTimer
from info_messages import MessageHandler
import time

console = Console()
init()

database_setup.create_database() 
database_setup.create_tables() 
database_setup.load_csv_file_to_database('C:\\the\\file\\path\\questions.csv')

def print_question(question):
    console.print(Panel(question, title=Fore.GREEN + f'Question' + Style.RESET_ALL))

def print_answers(answers):
    for option, text in answers.items():
        console.print(Panel(text, title=Fore.YELLOW + f'Option {option}' + Style.RESET_ALL))

def display_user_statistics(user_name): 
    stats = from_table_statistics(user_name)  
    if stats: 
        print(Fore.GREEN + f"User ID: {stats['user_id']}\nUser Name: {stats['user_name']}\nScores: {stats['scores']}" + Style.RESET_ALL) 
    else: 
        print(Fore.RED + f'No statistics found for this user.' + Style.RESET_ALL)  

def request_nickname():
    nickname = input(Fore.BLUE + f'Enter your nickname: ' + Style.RESET_ALL)
    return nickname

def display_instructions(): 
    message_handler = MessageHandler()
    message_handler.display_rules_message() 
    print(Fore.YELLOW + f'You have 10 seconds to read the instructions.\n' + Style.RESET_ALL) 
    time.sleep(10) 
    input(Fore.GREEN + f'Press Enter to confirm you have read the instructions...' + Style.RESET_ALL)

def get_valid_user_input_and_handle_response(answer, quiz_timer):
    while True:
        quiz_timer.restart()
        answer = input(Fore.BLUE + f'Your answer (A/B/C/D) or "quit" to exit quiz: ' + Style.RESET_ALL).lower()
        if answer in ['a', 'b', 'c', 'd', 'quit']:
            if answer in ['a', 'b', 'c', 'd']:
                quiz_timer.stop()
                return answer
            else:
                quiz_timer.stop()
                if confirm_exit(quiz_timer):
                    return None
        else:
            print(Fore.RED + f'Invalid input.\n' + Style.RESET_ALL)

def handle_user_answer(answer, correct_answer, lives, score):
    if answer == correct_answer.lower():
        score += 1
        print(Fore.GREEN + f'Well done! You got 1 point. \nCurrent score: {score} points\n' + Style.RESET_ALL)
    else:
        lives -= 1
        print(Fore.RED + f'Wrong. The correct answer is {correct_answer}\nLives remaining: {lives} \nCurrent score: {score} points\n' + Style.RESET_ALL)
        time.sleep(3)
    return lives, score

def confirm_exit(quiz_timer):
    confirm_quit = input(Fore.BLUE + f'Are you sure you want to exit the quiz? Confirm by entering "Y" or "N" : ' + Style.RESET_ALL).lower()
    if confirm_quit in ['y', 'n']:
        if confirm_quit == 'n':
            print(Fore.YELLOW + f'What do we say to the God of Death? Not today! \nI am glad that you decided to stay.\n' + Style.RESET_ALL)
            quiz_timer.restart()
            #interaction_with_quiz()
            return False
        else:
            print(Fore.YELLOW + f'Thanks for playing. See you next time!\n' + Style.RESET_ALL)
            return True
    else:
        print(Fore.RED + f'Invalid input. Please enter "Y" or "N": ' + Style.RESET_ALL)
        return confirm_exit(quiz_timer)
    
def handle_retry(nickname, quiz_timer):
    while True:
        retry = input(Fore.RED + f'Want to retry? Enter "Y" or "N" : ' + Style.RESET_ALL).lower()
        if retry in ['y', 'n']:
            if retry == 'y':
                print(Fore.YELLOW + f'What do we say to the God of Death? Not today! \nRestarting the quiz.\n' + Style.RESET_ALL)
                quiz_timer.restart()
                quiz(nickname)
            else:
                print(Fore.RED + f'Your watch has ended. See you next time!\n' + Style.RESET_ALL)
                return 
        else:
            print(Fore.RED + f'Invalid input. Please enter "Y" or "N: ' + Style.RESET_ALL)        

def handle_game_over(nickname, quiz_timer):
    handle_retry(nickname, quiz_timer)

def retry_question(question_data, answers, lives, score, quiz_timer, nickname): 
    print_question(question_data['question']) 
    print_answers(answers) 
    answer = get_valid_user_input_and_handle_response(question_data['correct_answer'], quiz_timer) 
    if answer == 'quit': 
        quiz_timer.stop() 
        if confirm_exit(quiz_timer): 
            return 
    else: 
        lives, score = handle_user_answer(answer, question_data['correct_answer'], lives, score) 
        if lives == 0: 
            handle_game_over(nickname, quiz_timer) 
            return 
        if lives > 0: 
            quiz_timer.start()
            interaction_with_quiz()  # type: ignore
                      
def quiz(nickname):
    lives = 3
    score = 0
    asked_questions = []
    timeout = 60 
    question_data = None 
    answers = None
    
    def interaction_with_quiz():
        nonlocal lives, score, asked_questions, quiz_timer, question_data, answers
        question_id = get_unique_random_question_id(asked_questions)
        if question_id is None:
            print(Fore.RED + f'No question available.\n' + Style.RESET_ALL)
            return
        
        question_data = from_table_questions(question_id)
        if question_data is None:
            print(Fore.RED + f'Question not found.\n' + Style.RESET_ALL)
            return

        asked_questions.append(question_id) 
        print_question(question_data['question'])

        answers = {
            'A': question_data['A'],
            'B': question_data['B'],
            'C': question_data['C'],
            'D': question_data['D']
        }

        print_answers(answers)
        quiz_timer.start()
        handle_question()

    def handle_question():
        nonlocal lives, score, quiz_timer, question_data
        answer = get_valid_user_input_and_handle_response(question_data['correct_answer'], quiz_timer)
        if answer is None:
            return
        
        lives, score = handle_user_answer(answer, question_data['correct_answer'], lives, score)
        if lives <= 0:
            handle_game_over(nickname, quiz_timer)
            return
    
        if lives > 0:
            interaction_with_quiz()

    def time_up(): 
        nonlocal lives, question_data, answers
        lives -= 1
        print(Fore.RED + f'\nTime\'s up! You lose 1 life. \nLives remaining: {lives} \n' + Style.RESET_ALL)     
        if lives > 0: 
            interaction_with_quiz()
        else:
            print(Fore.RED + f'Game over.\n' + Style.RESET_ALL) 
            handle_game_over(nickname, quiz_timer)

    quiz_timer = QuizTimer(timeout, time_up)

    interaction_with_quiz()
    print(Fore.WHITE + f'Your final score is: {score} points \n' + Style.RESET_ALL)
    save_score(nickname, score)
    handle_game_over(nickname, quiz_timer)

def main():
    display_instructions()
    nickname = request_nickname()
    quiz(nickname)
    while True:
        view_stats = input(Fore.BLUE + f'Would you like to view your statistics? Enter "Y" or "N" : ' + Style.RESET_ALL).lower()
        if view_stats in ['y', 'n']:
            if view_stats == 'y': 
                user_name = input(Fore.BLUE + f'Enter your nickname to view statistics: ' + Style.RESET_ALL) 
                display_user_statistics(user_name) 
            else:
                print(Fore.YELLOW + f'Thank you for playing!\n' + Style.RESET_ALL)
                break
        else: 
            print(Fore.RED + f'Invalid input. Skipping statistics view.\n' + Style.RESET_ALL)

if __name__ == '__main__':
    main()
