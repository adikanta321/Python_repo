#This One is Using CUI! THANKS 😊
import random

name = input ("What is Your Name?:-  ")

print("Good Luck ! ", name)

words=[ "rainbow" , " computer" , "Programming", "Python" ,
        "Mathmatics", "player", "Condition", "Reverse",
        "water", "board" , "geeks"]
word = random.choice(words)

print("Guess the characters")

guesses = ''
turns = 12
while turns > 0:
    failed = 0
    for char in word:
        if char in guesses:
            print(char, end=" ")
        else:
            print("_")
            failed += 1
    if failed == 0:
        print("You Win")
        print("The word is: ", word)
        break
    print()
    guess = input("Guess a character: ")
    guesses += guess
    if guess not in word:
        print("wrong")
        print("You Have", + turns, "More Guesses")
        if turns == 0:
            print("You Loose")

#This is using GUI 
"""import random
import tkinter as tk
from tkinter import messagebox

# Function to start a new game
def new_game():
    global word, guesses, turns
    word = random.choice(words)
    guesses = ''
    turns = 12
    word_label.config(text="_ " * len(word))
    guess_entry.delete(0, tk.END)
    status_label.config(text=f"Good Luck! {name}, you have {turns} turns left.")

# Function to process the guess
def guess_character():
    global guesses, turns
    guess = guess_entry.get().strip()
    guess_entry.delete(0, tk.END)

    if len(guess) != 1:
        messagebox.showwarning("Invalid input", "Please enter a single character.")
        return

    if guess in guesses:
        messagebox.showwarning("Invalid input", "You've already guessed that character.")
        return

    guesses += guess
    displayed_word = ""

    for char in word:
        if char in guesses:
            displayed_word += char + " "
        else:
            displayed_word += "_ "

    word_label.config(text=displayed_word)

    if guess not in word:
        turns -= 1
        status_label.config(text=f"Wrong guess! You have {turns} turns left.")
        if turns == 0:
            messagebox.showinfo("Game Over", f"Oops! You lost. The word was: {word}")
            new_game()
    else:
        if "_" not in displayed_word:
            messagebox.showinfo("Congratulations!", "You guessed the word!")
            new_game()

# Initializing main window
root = tk.Tk()
root.title("Word Guessing Game")

# Game variables
words = ["rainbow", "computer", "programming", "python", "mathematics", "player", "condition", "reverse", "water", "board", "geeks"]
name = "Player"  # Replace with dynamic input if needed
word = ""
guesses = ""
turns = 12

# UI Elements
name_label = tk.Label(root, text=f"Good Luck! {name}", font=("Helvetica", 16))
name_label.pack(pady=10)

word_label = tk.Label(root, text="", font=("Helvetica", 24))
word_label.pack(pady=20)

guess_entry = tk.Entry(root, font=("Helvetica", 14))
guess_entry.pack(pady=10)

guess_button = tk.Button(root, text="Guess", command=guess_character, font=("Helvetica", 14), bg="#4CAF50", fg="white")
guess_button.pack(pady=10)

status_label = tk.Label(root, text=f"You have {turns} turns left.", font=("Helvetica", 14))
status_label.pack(pady=20)

# Start the first game
new_game()

# Run the application
root.mainloop()"""  #Gui Application using tkinter TAP ON IT
