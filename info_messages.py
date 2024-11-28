from rich.console import Console
from rich.panel import Panel
from colorama import init, Fore, Style

class MessageHandler:
    def __init__(self):
        self.console = Console()

    def display_rules_message(self):
        message = """
        Welcome to the 'Song of Ice and Fire' Quiz!

        Here are the rules:
        1. You will be presented with a question and 4 possible answers (A, B, C, D).
        2. Only one of the answers is correct.
        3. For each correct answer, you will earn 1 point.
        4. For each incorrect answer, you will lose 1 of your 3 lives.
        5. You have 20 seconds to answer each question.

        Good luck and enjoy the quiz!
        """
        self.console.print(Panel(message, title= Fore.GREEN + 'Quiz Rules' + Style.RESET_ALL, subtitle= Fore.YELLOW + 'Please read carefully' + Style.RESET_ALL))
