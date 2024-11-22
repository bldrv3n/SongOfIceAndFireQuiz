from rich.console import Console
from rich.panel import Panel

console = Console()

def test_quiz ():
    questions = [
        {
            'question': 'What is the sigil of House Stark?',
            'answer_options': ['A. a grey Direwolf on a white background', 'B. a golden Kraken on a black field', 'C.a golden rose on a pale green field', 'D.a crowned black stag on a gold field'],
            'correct_answer': 'a'
        },
        {
            'question': 'What is the capital of the Seven Kingdoms?',
            'answer_options': ['A. Dragonstone', 'B. Winterfell', 'C. King\'s Landing', 'D. Casterly Rock'],
            'correct_answer': 'c'
        },
        {
            'question': 'What do the men and women of the realm call the creatures that killed Waymar?',
            'answer_options': ['A. The Others', 'B. Shadow walkers', 'C. Wights', 'D. Wildings'],
            'correct_answer': 'a'
        },
    ]

    def play_quiz ():
        lives = 3
        score = 0
        for q in questions:
            print (q['question'])
            for option in q['answer_options']:
                print(option)
            while True:
                answer = input ('Your answer (A/B/C/D) or ''quit'' to exit quiz: ').lower()   
                if answer in ['a', 'b', 'c', 'd', 'quit']:
                    break
                else:
                    print('Invalid input. Choose the correct answer (A, B, C, D) or type ''quit'' to exit the quiz.')

            if answer == 'quit':
                while True:
                    confirm_quit = input('Are you sure you want to exit the quiz?\nConfirm by entering ''Y'' for yes or ''N'' for no:').lower()
                    if confirm_quit in ['y', 'n']:
                        break
                    else:
                        print ('Invalid input. Please type ''Y'' for yes or ''N'' for no.')

                if confirm_quit == 'y':
                    print('Thanks for playing. See you next time!')
                    return #or break
                elif confirm_quit == 'n':
                    print('Good that you decided to stay!\n')
                    continue
                

            if answer == q['correct_answer']: 
                print ('Well done! You got 1 point. \n')
                score += 1
            else:
                print ('Wrong.\nThe correct answer is' + ' ' + q['correct_answer'] + '\n')
                lives -= 1
                if lives == 0:
                    print ('You lost. Want to try again? Enter ''y'' for yes and ''n'' for no.')
                    retry = input ('Your choice:').lower()
                    if retry == 'y':
                        print ('Good choice. Restarting the quiz.\n')
                        return play_quiz()
                    elif retry == 'n':
                        print ('Thanks for playing. See you next time!')
                        return
                    else:
                        print ('Invalid input. Exiting the quiz.')
                        return
                    
        print(f'Your final score is: {score}')

    play_quiz()
test_quiz()