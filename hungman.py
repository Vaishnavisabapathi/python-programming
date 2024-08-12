import random

def hangman():
    # List of words to choose from
    word_list = ["python", "java", "javascript", "computer", "hangman", "programming", "developer"]
    
    # Select a random word from the list
    word = random.choice(word_list).lower()
    guessed_word = ['_'] * len(word)
    attempts = 6  # Number of allowed incorrect guesses
    guessed_letters = []
    
    print("Welcome to Hangman!")
    print("You have", attempts, "attempts to guess the word.")
    
    while attempts > 0:
        print("\nWord: ", ' '.join(guessed_word))
        guess = input("Guess a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue
        
        if guess in guessed_letters:
            print("You've already guessed that letter. Try again.")
            continue

        guessed_letters.append(guess)
        
        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed_word[i] = guess
            print(f"Good job! '{guess}' is in the word.")
        else:
            attempts -= 1
            print(f"Sorry, '{guess}' is not in the word. You have {attempts} attempts left.")
        
        if '_' not in guessed_word:
            print("\nCongratulations! You've guessed the word:", word)
            break
    else:
        print("\nYou've run out of attempts! The word was:", word)

# Run the game
hangman()
