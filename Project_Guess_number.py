import random
print(''' Hi Welcome to the game, This is a Number Guessing Game.
You Got 7 chances to Guess the Number.
Let's Start the game. ''')

number_to_guess = random.randrange ( 1,101 )
chances = 7
guess_counter = 0

while guess_counter < chances:
    guess_counter += 1
    try:
        my_guess = int(input(" Please enter Your Guess Number:-  "))
        if my_guess == number_to_guess:
            print(f" The Number is { number_to_guess } and you Found it Right !! in the {guess_counter} attempt ")
            break
        elif my_guess > number_to_guess:
            print(" Your Guess is higher ")
        elif my_guess < number_to_guess:
            print("Your guess is lesser")
    except ValueError:
        print("Invalid input. Please Enter valid integer. ")
    if guess_counter >= chances and my_guess != number_to_guess:
       print(f" Oops Sorry 😉, The number is {number_to_guess} better luck next time 😊 ")


"""import random
import tkinter as tk
from tkinter import messagebox

# Function to start a new game
def new_game():
    global number_to_guess, guess_counter, chances
    number_to_guess = random.randrange(1, 101)
    guess_counter = 0
    chances = 7
    guess_entry.delete(0, tk.END)
    status_label.config(text="You have 7 chances to guess the number.")

# Function to process the guess
def make_guess():
    global guess_counter
    try:
        my_guess = int(guess_entry.get())
        guess_entry.delete(0, tk.END)
        guess_counter += 1

        if my_guess == number_to_guess:
            messagebox.showinfo("Congratulations!", f"The number is {number_to_guess}. You found it right in {guess_counter} attempt(s)!")
            new_game()
        elif my_guess > number_to_guess:
            status_label.config(text="Your guess is higher. Try again!")
        elif my_guess < number_to_guess:
            status_label.config(text="Your guess is lesser. Try again!")

        if guess_counter >= chances:
            messagebox.showinfo("Game Over", f"Oops, sorry! The number was {number_to_guess}. Better luck next time!")
            new_game()
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid integer.")
        guess_entry.delete(0, tk.END)

# Initializing main window
root = tk.Tk()
root.title("Number Guessing Game")

# Game variables
number_to_guess = random.randrange(1, 101)
guess_counter = 0
chances = 7

# UI Elements
title_label = tk.Label(root, text="Welcome to the Number Guessing Game!", font=("Helvetica", 16), pady=10)
title_label.pack()

instruction_label = tk.Label(root, text="You have 7 chances to guess the number between 1 and 100.", font=("Helvetica", 12), pady=10)
instruction_label.pack()

guess_entry = tk.Entry(root, font=("Helvetica", 14))
guess_entry.pack(pady=5)

guess_button = tk.Button(root, text="Make a Guess", command=make_guess, font=("Helvetica", 14), bg="#4CAF50", fg="white", padx=20, pady=5)
guess_button.pack(pady=10)

status_label = tk.Label(root, text="You have 7 chances to guess the number.", font=("Helvetica", 12), pady=10)
status_label.pack()

# Start the first game
new_game()

# Run the application
root.mainloop()"""  #Gui Application using tkinter tap on it
