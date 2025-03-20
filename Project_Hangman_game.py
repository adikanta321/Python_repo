"""import tkinter as tk
import random

# List of words to guess
words = ['apple', 'banana', 'cherry', 'date', 'grape']

# Choose a random word
word = random.choice(words)
guessed = ['_' for _ in word]  # List to keep track of guessed letters

def guess(letter):
    if letter in word:
        update_guessed(letter)
    update_display()

def update_guessed(letter):
    for index, char in enumerate(word):
        if char == letter:
            guessed[index] = letter

def update_display():
    label.config(text=' '.join(guessed))
    if '_' not in guessed:
        label.config(text='You win!')

# Create the main window
root = tk.Tk()
root.title("Hangman Game")

# Create a label to show the word to guess
label = tk.Label(root, text=' '.join(guessed), font=('Helvetica', 24))
label.pack(pady=20)

# Create a frame to hold the buttons
frame = tk.Frame(root)
frame.pack()

# Create buttons for each letter
for ascii_code in range(97, 123):  # ASCII codes for a-z
    letter = chr(ascii_code)
    btn = tk.Button(frame, text=letter.upper(), command=lambda l=letter: guess(l),bg="#4CAF50", fg="white")
    btn.pack(side='left')

# Run the application
root.mainloop()"""  #Gui Application using tkinter TAP ON IT

# Python Program to illustrate
# Hangman Game
import random
from collections import Counter

someWords = '''apple banana mango strawberry
orange grape pineapple apricot lemon coconut watermelon
cherry papaya berry peach lychee muskmelon'''

someWords = someWords.split(' ')
# randomly choose a secret word from our "someWords" return in [] LIST. (split always return list).
word = random.choice(someWords)

if __name__ == '__main__':
    print('Guess the word! HINT: word is a name of a fruit')

    for i in word:
        # For printing the empty spaces for letters of the word
        print('_', end=' ')
    print()

    playing = True
    # List for storing the letters guessed by the player
    letterGuessed = ''
    chances = len(word) +2
    correct = 0
    flag = 0
    try:
        while (chances != 0) and flag == 0:  # Flag is updated when the word is correctly guessed
            print()
            chances -= 1
            try:
                guess = str(input('Enter a letter to guess: '))
            except:
                print('Enter only a letter!')
                continue

            # Validation of the guess
            if not guess.isalpha():
                print('Enter only a LETTER')
                continue
            elif len(guess) > 1:
                print('Enter only a SINGLE letter')
                continue
            elif guess in letterGuessed:
                print('You have already guessed that letter')
                continue

            # If letter is guessed correctly
            if guess in word:
                # k stores the number of times the guessed letter occurs in the word
                k = word.count(guess)
                for _ in range(k):
                    letterGuessed += guess  # The guessed letter is added as many times as it occurs

            # Print the word
            for char in word:
                if char in letterGuessed and (Counter(letterGuessed) != Counter(word)):
                    print(char, end=' ')
                    correct += 1
                # If user has guessed all the letters
                # Once the correct word is guessed fully,
                elif Counter(letterGuessed) == Counter(word):
                    # the game ends, even if chances remain
                    print("The word is: ", end=' ')
                    print(word)
                    flag = 1
                    print('Congratulations, You won!')
                    break  # To break out of the for loop
                    break  # To break out of the while loop
                else:
                    print('_', end=' ')

        # If user has used all of his chances
        if chances <= 0 and (Counter(letterGuessed) != Counter(word)):
            print()
            print('You lost! Try again..')
            print('The word was {}'.format(word))

    except KeyboardInterrupt:
        print()
        print('Bye! Try again.')
        exit()



