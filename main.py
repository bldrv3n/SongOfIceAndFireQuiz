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
database_setup.load_csv_file_to_database('C:\\Users\\ReDI User\\Desktop\\my_project\\questions.csv')

def print_question(question):
    console.print(Panel(question, title=f'Question'))

def print_answers(answers):
    for option, text in answers.items():
        console.print(Panel(text, title=f'Option {option}'))

def display_user_statistics(user_name): 
    stats = from_table_statistics(user_name)  
    if stats: 
        print(Fore.BLUE + f"User ID: {stats['user_id']}\nUser Name: {stats['user_name']}\nScores: {stats['scores']}" + Style.RESET_ALL) 
        return
    else: 
        print(Fore.RED + f'No statistics found for this user.' + Style.RESET_ALL)  
        exit          

def request_nickname():
    nickname = input(Fore.BLUE + f'Enter your nickname: ' + Style.RESET_ALL)
    return nickname

def display_instructions(): 
    message_handler = MessageHandler()
    message_handler.display_rules_message() 
    print(Fore.YELLOW + f'You have 10 seconds to read the instructions.' + Style.RESET_ALL) 
    time.sleep(10) 
    input(Fore.GREEN + f'Press Enter to confirm you have read the instructions...' + Style.RESET_ALL)

def quiz(nickname):
    def interaction_with_quiz():
        lives = 3
        score = 0
        asked_questions = []
        timeout = 20 

        def time_up(): 
            nonlocal lives, score 
            print(Fore.RED + f'Time\'s up! You lose 1 life. \nChoose the correct answer (A, B, C, D) or type "quit" to exit the quiz.' + Style.RESET_ALL) 
            lives -= 1 
            if lives == 0: 
                print(Fore.RED + f'You\'ve run out of time and 3 lives. Game over.' + Style.RESET_ALL) 
                return

        quiz_timer = QuizTimer(timeout, time_up)

        while lives > 0: 
            question_id = get_unique_random_question_id(asked_questions) 
            if question_id is None:
                print(Fore.RED + f'No question available.' + Style.RESET_ALL) 
                break 

            question_data = from_table_questions(question_id)
            if question_data is None:
                print(Fore.RED + f'Question not found.' + Style.RESET_ALL)
                break
            
            asked_questions.append(question_id) 
            print_question(question_data['question'])

            answers = {
                'A': question_data['A'],
                'B': question_data['B'],
                'C': question_data['C'],
                'D': question_data['D']
            }

            print_answers(answers)
            quiz_timer.restart()

            while True:
                answer = input(f'Your answer (A/B/C/D) or "quit" to exit quiz: ').lower()
                if answer in ['a', 'b', 'c', 'd', 'quit']:
                    break
                else:
                    print(Fore.RED + f'Invalid input. Choose the correct answer (A, B, C, D) or type "quit" to exit the quiz.' + Style.RESET_ALL)

            if answer == 'quit':
                confirm_quit = input(f'Are you sure you want to exit the quiz? Confirm by entering "Y" or "N" : ').lower()
                if confirm_quit == 'n':
                    print(Fore.BLUE + f'What do we say to the God of Death? Not today! \n I am glad that you decided to stay.\n' + Style.RESET_ALL)
                    quiz_timer.restart()
                    continue
                elif confirm_quit == 'y':
                    print(Fore.YELLOW + f'Thanks for playing. See you next time!' + Style.RESET_ALL)
                    quiz_timer.stop()
                    break
                else:
                    print(Fore.RED + f'Invalid input. Please enter "Y" or "N" :' + Style.RESET_ALL)
                    continue
              
            if answer == question_data['correct_answer'].lower():
                print(Fore.GREEN + f'Well done! You got 1 point. \n' + Style.RESET_ALL)
                score += 1
            else:
                print(Fore.RED + f'Wrong. The correct answer is {question_data['correct_answer']}\n' + Style.RESET_ALL)
                lives -= 1
                if lives == 0:
                    retry = input(Fore.RED + f'You lost. Want to try again? Enter "Y" or "N" : ' + Style.RESET_ALL).lower()
                    if retry == 'y':
                        print(Fore.BLUE + f'What do we say to the God of Death? Not today!\n Restarting the quiz.\n' + Style.RESET_ALL)
                        return interaction_with_quiz()
                    elif retry == 'n':
                        print(Fore.YELLOW + f'Your watch has ended. See you next time!' + Style.RESET_ALL)
                        break
                    else:
                        print(Fore.RED + f'Invalid input. Exiting the quiz.' + Style.RESET_ALL)
                        return
                    
        quiz_timer.stop()
        print(Fore.BLUE + f'Your final score is: {score}' + Style.RESET_ALL)

        save_score(nickname, score)

    interaction_with_quiz()


def main():
    display_instructions()
    nickname = request_nickname()
    quiz(nickname)
    view_stats = input(Fore.BLUE + f'Would you like to view your statistics? Enter "Y" or "N" : ' + Style.RESET_ALL).lower()
    if view_stats == 'y': 
        user_name = input(Fore.BLUE + f'Enter your nickname to view statistics: ' + Style.RESET_ALL) 
        display_user_statistics(user_name) 
        exit
    elif view_stats == 'n': 
        print(Fore.YELLOW + f'Thank you for playing!' + Style.RESET_ALL)
        exit 
    else: 
        print(Fore.RED + f'Invalid input. Skipping statistics view.' + Style.RESET_ALL)



if __name__ == '__main__':
    main()
