# Things to edit
# Need an Exit button to return the user to the main window within every game interface
# Need a Quit button on the main window to close game console
# For Rock Paper Scissors, need to stop console from returning user to main window after every selection
# For Hangman, need to fix Guesses left counter from being stuck
# For Hangman, need to draw randomly from words.txt instead
# For Millionaire, need to figure out a way to download a list of random questions, and draw randomly from that .txt instead

import tkinter as tk
from tkinter import messagebox
import random

class GameConsole:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Console")

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()

        self.label = tk.Label(self.main_frame, text="Welcome to the Game Console!")
        self.label.pack(pady=10)

        self.play_hangman_button = tk.Button(self.main_frame, text="Play Hangman", command=self.play_hangman)
        self.play_hangman_button.pack(pady=5)

        self.play_millionaire_button = tk.Button(self.main_frame, text="Play Who Wants to Be a Millionaire", command=self.play_millionaire)
        self.play_millionaire_button.pack(pady=5)
        
        self.play_rps_button = tk.Button(self.main_frame, text="Play Rock, Paper, Scissors", command=self.play_rock_paper_scissors)
        self.play_rps_button.pack(pady=5)
        
    def play_rock_paper_scissors(self):
        self.main_frame.destroy()

        rps_frame = tk.Frame(self.master)
        rps_frame.pack()

        rps_label = tk.Label(rps_frame, text="Rock, Paper, Scissors Game")
        rps_label.pack(pady=10)

        choices = ["Rock", "Paper", "Scissors"]

        def computer_choice():
            return random.choice(choices)

        def play(user_choice):
            comp_choice = computer_choice()
            result = determine_winner(user_choice, comp_choice)
            messagebox.showinfo("Result", f"You chose {user_choice}\nComputer chose {comp_choice}\n{result}")
            rps_frame.destroy()
            self.__init__(self.master)

        def determine_winner(user, comp):
            if user == comp:
                return "It's a tie!"
            elif (
                (user == "Rock" and comp == "Scissors") or
                (user == "Paper" and comp == "Rock") or
                (user == "Scissors" and comp == "Paper")
            ):
                return "You win!"
            else:
                return "Computer wins!"

        for choice in choices:
            choice_button = tk.Button(rps_frame, text=choice, command=lambda choice=choice: play(choice))
            choice_button.pack(pady=5)

    def play_hangman(self):
        self.main_frame.destroy()

        word_list = ["python", "hangman", "programming", "computer", "tkinter"] # Edit this part to randomly draw from words.txt
        secret_word = random.choice(word_list).lower()
        guesses_left = 8
        guessed_letters = set()

        hangman_frame = tk.Frame(self.master)
        hangman_frame.pack()

        hangman_label = tk.Label(hangman_frame, text="Hangman Game")
        hangman_label.pack(pady=10)

        word_display = ["_" if letter.isalpha() else letter for letter in secret_word]

        word_label = tk.Label(hangman_frame, text=" ".join(word_display))
        word_label.pack(pady=10)

        def guess_letter():
            nonlocal guesses_left
            nonlocal word_display
            nonlocal guessed_letters

            letter = guess_entry.get().lower()
            guess_entry.delete(0, tk.END)

            if letter.isalpha() and letter not in guessed_letters:
                guessed_letters.add(letter)

                if letter in secret_word:
                    for i, char in enumerate(secret_word):
                        if char == letter:
                            word_display[i] = letter
                else:
                    guesses_left -= 1

                word_label.config(text=" ".join(word_display))

                if "_" not in word_display:
                    messagebox.showinfo("Hangman", "Congratulations! You guessed the word.")
                    hangman_frame.destroy()
                    self.__init__(self.master)

                if guesses_left == 0:
                    messagebox.showinfo("Hangman", f"Sorry, you ran out of guesses. The word was {secret_word}.")
                    hangman_frame.destroy()
                    self.__init__(self.master)

            else:
                messagebox.showwarning("Invalid Guess", "Please enter a valid and unique letter.")

        guess_label = tk.Label(hangman_frame, text="Enter a letter:")
        guess_label.pack(pady=5)

        guess_entry = tk.Entry(hangman_frame)
        guess_entry.pack(pady=5)

        guess_button = tk.Button(hangman_frame, text="Guess", command=guess_letter)
        guess_button.pack(pady=5)

        info_label = tk.Label(hangman_frame, text=f"Guesses left: {guesses_left}")
        info_label.pack(pady=5)

    def play_millionaire(self):
        self.main_frame.destroy()

        question_list = [
            {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": "Paris"},
            {"question": "Which planet is known as the Red Planet?", "options": ["Mars", "Jupiter", "Venus", "Saturn"], "answer": "Mars"},
            {"question": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "answer": "William Shakespeare"},
            # Edit this part to randomly draw from question_list.txt
        ]

        random.shuffle(question_list)
        question_number = 0

        millionaire_frame = tk.Frame(self.master)
        millionaire_frame.pack()

        millionaire_label = tk.Label(millionaire_frame, text="Who Wants to Be a Millionaire?")
        millionaire_label.pack(pady=10)

        current_question = question_list[question_number]

        question_text = tk.Label(millionaire_frame, text=current_question["question"])
        question_text.pack(pady=10)

        def check_answer(option):
            nonlocal question_number
            nonlocal question_list

            if option == current_question["answer"]:
                if question_number < len(question_list) - 1:
                    question_number += 1
                    next_question()
                else:
                    messagebox.showinfo("Congratulations", "You've answered all questions correctly! You win $1,000,000.")
                    millionaire_frame.destroy()
                    self.__init__(self.master)
            else:
                messagebox.showinfo("Game Over", "Sorry, your answer is incorrect. You did not win the million.")
                millionaire_frame.destroy()
                self.__init__(self.master)

        def next_question():
            nonlocal current_question
            current_question = question_list[question_number]
            question_text.config(text=current_question["question"])
            for i in range(4):
                option_buttons[i].config(text=current_question["options"][i])

        option_buttons = []
        for i in range(4):
            option_button = tk.Button(millionaire_frame, text=current_question["options"][i], command=lambda i=i: check_answer(current_question["options"][i]))
            option_button.pack(pady=5)
            option_buttons.append(option_button)

# Main part of the script
root = tk.Tk()
game_console = GameConsole(root)
root.mainloop()
