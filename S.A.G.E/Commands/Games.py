import random
import difflib
from Commands.Voice_utils import speak, takeCommand

def similar_command(query, options):
    if query is None:
        return None
    matches = difflib.get_close_matches(query, options)
    return matches[0] if matches else None

def play_rock_paper_scissors():
    options = ["rock", "paper", "scissors"]
    variations = {
        "rock": ["rock", "roc", "rack", "rok"],
        "paper": ["paper", "piper", "papa", "ppr"],
        "scissors": ["scissors", "scisor", "seizer", "sizzor", "sissor"]
    }
    
    user_score = 0
    assistant_score = 0
    
    speak("Let's play Rock Paper Scissors! First to 3 wins.")
    
    while user_score < 3 and assistant_score < 3:
        speak("Say your choice: rock, paper, or scissors.")
        user_choice = takeCommand()
        if user_choice:
            user_choice = similar_command(user_choice, sum(variations.values(), []))
            if not user_choice:
                speak("Invalid choice. Please choose rock, paper, or scissors.")
                continue
            else:
                for key, value in variations.items():
                    if user_choice in value:
                        user_choice = key
                        break
        else:
            speak("Sorry, I didn't catch that. Please try again.")
            continue
        
        assistant_choice = random.choice(options)
        speak(f"I chose {assistant_choice}.")
        
        if user_choice == assistant_choice:
            speak("It's a tie.")
        elif (user_choice == "rock" and assistant_choice == "scissors") or \
             (user_choice == "paper" and assistant_choice == "rock") or \
             (user_choice == "scissors" and assistant_choice == "paper"):
            speak("You win this round!")
            user_score += 1
        else:
            speak("I win this round.")
            assistant_score += 1
        
        speak(f"Score - You: {user_score}, Assistant: {assistant_score}")
    
    if user_score == 3:
        speak("Congratulations! You won the game.")
    else:
        speak("I won the game. Better luck next time!")

def play_number_guessing():
    speak("Let's play a number guessing game!")

    while True:
        try:
            speak("What's the starting range of number?")
            lower_bound = int(takeCommand())
            speak("What's the ending range of number?")
            upper_bound = int(takeCommand())
            
            if lower_bound >= upper_bound:
                speak("Invalid range. Lower bound must be less than upper bound. Try again.")
                continue
            else:
                break
        except ValueError:
            speak("Invalid input. Please provide numeric values. Try again.")
            continue

    number_to_guess = random.randint(lower_bound, upper_bound)
    attempts = 0
    max_attempts = 5

    speak(f"Guess a number between {lower_bound} and {upper_bound}. You have {max_attempts} attempts.")

    while attempts < max_attempts:
        speak("Enter your guess.")
        user_guess = takeCommand()
        
        if not user_guess.isdigit():
            speak("Please enter a valid number.")
            continue

        user_guess = int(user_guess)
        attempts += 1

        if user_guess < lower_bound or user_guess > upper_bound:
            speak(f"Your guess is out of range. Please guess a number between {lower_bound} and {upper_bound}.")
        elif user_guess < number_to_guess:
            speak("Higher!")
        elif user_guess > number_to_guess:
            speak("Lower!")
        else:
            speak(f"Congratulations! You guessed the number in {attempts} attempts.")
            return

    speak(f"Sorry, you've used all {max_attempts} attempts. The number was {number_to_guess}.")

def start_game():
    while True:
        speak("Which game would you like to play? Available games are Rock Paper Scissors and Number Guessing.")
        game_choice = takeCommand()
        
        if not game_choice:
            speak("Sorry, I didn't catch that. Please try again.")
            continue

        game_choice = game_choice.lower()  # Convert to lowercase to standardize

        if similar_command(game_choice, ["rock paper scissors"]):
            play_rock_paper_scissors()
        elif similar_command(game_choice, ["number guessing"]):
            play_number_guessing()
        else:
            speak("Sorry, that game is not available right now.")
        
        speak("Would you like to play another game? Say yes to continue or no to exit.")
        response = takeCommand()
        
        if not response:
            speak("Sorry, I didn't catch that. Please try again.")
            continue

        response = response.lower()  # Convert to lowercase to standardize

        if similar_command(response, ["no"]):
            speak("Okay, have a great day!")
            break
        elif similar_command(response, ["yes"]):
            continue
        else:
            speak("Sorry, I didn't understand your response.")