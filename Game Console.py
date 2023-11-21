import random 
import string
import tkinter as tk

root = tk.Tk()
root.title("Game Console")
root.geometry('400x400')

WORDLIST_FILENAME = "words.txt"

lettersGuessed = []
guessNo = 8

# function to close the game console
def close_window():
    root.destroy()

# function to return to clear all elements, and return to main window
def return_to_main(root):
    for widget in root.winfo_children():
        widget.destroy()

    game_launch(root)

# function to create generic UI for each game
def game_interface(root, game_function):
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Enter your answer:")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    submit_button = tk.Button(root, text="Submit", command=lambda: game_function(entry.get()))
    submit_button.pack()
    
    exit_button = tk.Button(root, text="Exit", command=lambda: return_to_main(root))
    exit_button.pack()

# function to create elements for the main window
def game_launch(root):
    label = tk.Label(root, text="Choose a Game:")
    label.pack()
    
    game1_button = tk.Button(root, text="Hangman", command=lambda: game_interface_hangman(root, hangmanGame))
    game1_button.pack()

    game2_button = tk.Button(root, text="Rock Paper Scissors", command=lambda: game_interface(root, rpsGame))
    game2_button.pack()

    game3_button = tk.Button(root, text="Who wants to be a millionaire?", command=lambda: game_interface_millionaire(root, millionaireGame))
    game3_button.pack()
    
    quit_button = tk.Button(root, text="Quit Console", command=lambda: close_window())
    quit_button.pack()

# function for rock-paper-scissors game logic
def rpsGame(answer):
    game_interface(root, rpsGame)
        
    if answer not in ["rock", "paper", "scissors"]:
        result_label = tk.Label(root, text="That is not a valid response. Please choose from rock/paper/scissors.")
        result_label.pack()
    
    else:
        random.seed()
        choices = ["rock", "paper", "scissors"]
        computer_choice = random.choice(choices)
    
        if computer_choice == answer:
            rpsResult = tk.Label(root, text="It's a tie! Both you and the computer choose " + str(computer_choice) + ".")
            rpsResult.pack()
            
        elif(
            (answer == "rock" and computer_choice == "scissors") or 
            (answer == "paper" and computer_choice == "rock") or 
            (answer == "scissors" and computer_choice == "paper")
        ):
            rpsResult = tk.Label(root, text="You win! The computer choose " + str(computer_choice) + ".")
            rpsResult.pack()
            
        else:
            rpsResult = tk.Label(root, text="You lose! The computer choose " + str(computer_choice) + ".")
            rpsResult.pack()

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    for k in range(0, len(secretWord)):
        if secretWord[k] in lettersGuessed and k+1 == len(secretWord):
            return True
            break
        elif secretWord[k] in lettersGuessed:
            continue
        else:
            return False
            break

def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    Word = ''
    for k in range(0, len(secretWord)):
        if secretWord[k] in lettersGuessed and k+1 == len(secretWord):
            Word = Word[:k] + secretWord[k]
            return Word
            break
        elif secretWord[k] in lettersGuessed:
            Word = Word[:k] + secretWord[k]
        elif secretWord [k] not in lettersGuessed and k+1 == len(secretWord):
            Word = Word[:k] + "_ "
            return Word
        else:
            Word = Word[:k] + "_ "

def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    Unguess = ''
    for k in range(0, len(string.ascii_lowercase)):
        if string.ascii_lowercase[k] in lettersGuessed and k+1 == len(string.ascii_lowercase):
            return Unguess
        elif string.ascii_lowercase[k] not in lettersGuessed and k+1 == len(string.ascii_lowercase):
            Unguess = Unguess[:k] + string.ascii_lowercase[k]
            return Unguess
        elif string.ascii_lowercase[k] in lettersGuessed:
            continue
        else: 
            Unguess = Unguess[:k] + string.ascii_lowercase[k]
            
def game_interface_hangman(root, game_function):
    wordlist = loadWords()
    global secretWord
    secretWord = chooseWord(wordlist).lower()
    
    for widget in root.winfo_children():
        widget.destroy()
        
    welcome_msg = tk.Label(root, text="Welcome to the game, Hangman!")
    welcome_msg.pack()
    
    loading_words = tk.Label(root, text="Loading word list from file...")
    loading_words.pack()
    
    words_loaded = tk.Label(root, text=" " + str(len(wordlist)) + " words loaded.")
    words_loaded.pack()
    
    think_word = tk.Label(root, text="I am thinking of a word that is " + str(len(secretWord)) + " letters long.")
    think_word.pack()
    
    label = tk.Label(root, text="Enter your answer:")
    label.pack()
    
    entry = tk.Entry(root)
    entry.pack()
    
    submit_button = tk.Button(root, text="Submit", command=lambda: game_function(entry.get()))
    submit_button.pack()
    
    exit_button = tk.Button(root, text="Exit", command=lambda: return_to_main(root))
    exit_button.pack()

    hangmananswer = tk.Label(root, text=secretWord)
    hangmananswer.pack()
            
# function for hangman game logic
def hangmanGame(answer):
    if isWordGuessed(secretWord, lettersGuessed) == False:
        label = tk.Label(root, text="You have " + str(guessNo) + " guesses left.")
        label.pack()
        label = tk.Label(root, text="Available letters: " + str(getAvailableLetters(lettersGuessed)))
        label.pack()
        
    if answer == "31":
        result_label = tk.Label(root, text="Correct!")
    else:
        result_label = tk.Label(root, text="Incorrect!")
        
    result_label.pack()
    
# Questions and answers
questions = [
    {
        "question": "What is the capital of France?",
        "answers": ["Berlin", "Madrid", "Paris", "Rome"],
        "correct": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "answers": ["Mars", "Venus", "Jupiter", "Saturn"],
        "correct": "Mars"
    },
    # Add more questions here
]

def check_answer(number, index):
    selected_answer = possible_answers[number]
    correct_answer = questions[index]["correct"]

    if selected_answer == correct_answer:
        question_label = tk.Label(root, text="correct!")
        question_label.pack()
    else:
        question_label = tk.Label(root, text="incorrect!")
        question_label.pack()
        
def game_interface_millionaire(root, game_function):
    for widget in root.winfo_children():
        widget.destroy()
        
    possible_answers = []
        
    welcome_msg = tk.Label(root, text="Welcome to Who Wants to be a Millionaire!?")
    welcome_msg.pack()
    
    random.seed()
    computer_mil_choice = random.choice(enumerate(questions))
    index, question = computer_mil_choice
    
    question_label = tk.Label(root, text=question["question"])
    question_label.pack()
    
    for k in range(len(question["answers"])):
        choice_button = tk.Button(root, text=question["answers"][k], command=lambda k=k: check_answer(k, index))
        choice_button.pack()
        possible_answers.append(question["answers"][k])
    
    exit_button = tk.Button(root, text="Exit", command=lambda: return_to_main(root))
    exit_button.pack()

# function for who wants to be a millionare game logic
def millionaireGame(answer):
    game_interface_millionaire(root, millionaireGame)
    
    if answer == "11":
        result_label = tk.Label(root, text="Correct!")
    else:
        result_label = tk.Label(root, text="Incorrect")
        
    result_label.pack()

game_launch(root)
root.mainloop()