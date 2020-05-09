# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
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



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_list = []

    for letter in secret_word:
        secret_list.append(letter)
    
    if sorted(secret_list) == sorted(letters_guessed):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    inv_list = ["_ "] * len(secret_word)
    letter_counted = []
    secret_list = []
    inv_word = ""
    i=0

    for letter in secret_word:
        secret_list.append(letter)

    while i <= len(secret_list):
        for char in letters_guessed:
            if char in  secret_list and char not in letter_counted:
                letter_counted.append(char)
                inv_list[secret_list.index(char)] = char
                secret_list[secret_list.index(char)] = "_ "
            
            elif char in secret_list and char in letter_counted:
                inv_list[secret_list.index(char)] = char

        i += 1
    
    for char in inv_list:
        inv_word += char
    
    return inv_word




def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ""
    
    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter

    return available_letters

def unique_chars(s):
    '''
    s: string.
    Returns number of unique characters in string
    '''
    char_count = []
    unique = 0
    for char in s:
        if char not in char_count:
            unique += 1
            char_count.append(char)
    return unique
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    

    guess = 6

    warnings = 3

    secret_list = []

    for letter in secret_word:
        secret_list.append(letter)




    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")


    while guess > 0 and warnings >= 0:


        while warnings >= 0:

            print("-----------")
            print("You have", guess, "guesses and", warnings, "warnings left.")
            print("Available letters:", get_available_letters(letters_guessed))
            letter = str.lower(input("Enter your guess: "))
            
            if not str.isalpha(letter):
                    
                    if warnings != 0:
                        print("Try again with a letter! You lost a warning.")
                        warnings -= 1
                    else:
                        print("Try again with a letter! You've lost all your warnings so you lose a guess.")
                        guess -= 1

            elif len(letter) > 1:
                    if warnings != 0:
                        print("Please input only one letter at a time. You lost a warning.")
                        warnings -= 1
                    else:
                        print("Please input only one letter at a time. You've lost all your warnings so you lose a guess.")
                        guess -= 1

            elif letter in letters_guessed and letter in secret_list:
                print("You've already guessed that, try another letter.")

            else:
                    break

        
        letters_guessed.append(letter)
        

        if letter in secret_list:
            if get_guessed_word(secret_word, letters_guessed) == secret_word:
                break
            print("You got it!")
            print(get_guessed_word(secret_word, letters_guessed))
        else:
            print("Sorry, this letter is not in the word.")
            print(get_guessed_word(secret_word, letters_guessed))
            guess -= 1
            if guess != 0:
                print("Try again.")

    if guess != 0:
        score = guess * unique_chars(secret_word)
        print("You've won!")
    else:
        print("Tough luck! The word was", secret_word +".")

    return None




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

#Building with hints

def turn_list(s):
    L = []
    for char in s:
        L.append(char)
    return L



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_list = turn_list(my_word)
    other_list = turn_list(other_word)

    for element in my_list:
        if element == "_":
            my_list.remove(element)
    

    if len(my_list) == len(other_list):
        for i in range(len(my_list)):
            if my_list[i] == " ":
                other_list[i] = " "

    if other_list == my_list:
        return True
    else:
        return False




def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    counter = 0
    for word in wordlist:
        if match_with_gaps(my_word, word):
            print(word, end = " ")
            counter += 1

    if counter == 0:
        print("No matches found.")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    

    guess = 6

    warnings = 3

    secret_list = []

    for letter in secret_word:
        secret_list.append(letter)




    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")


    while guess > 0 and warnings >= 0:


        while warnings >= 0:

            print("-----------")
            print("You have", guess, "guesses and", warnings, "warnings left.")
            print("Available letters:", get_available_letters(letters_guessed))
            letter = str.lower(input("Enter your guess: "))
            
            if not str.isalpha(letter) and letter != "*":
                    
                    if warnings != 0:
                        print("Try again with a letter! You lost a warning.")
                        warnings -= 1
                    else:
                        print("Try again with a letter! You've lost all your warnings so you lose a guess.")
                        guess -= 1

            elif len(letter) > 1:
                    if warnings != 0:
                        print("Please input only one letter at a time. You lost a warning.")
                        warnings -= 1
                    else:
                        print("Please input only one letter at a time. You've lost all your warnings so you lose a guess.")
                        guess -= 1

            elif letter in letters_guessed and letter in secret_list:
                print("You've already guessed that, try another letter.")

            else:
                    letters_guessed.append(letter)
                    break
        
        if letter == "*":
            print("Possible matches are:") 
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print("\n")       


        else: 
            if letter in secret_list:
                if get_guessed_word(secret_word, letters_guessed) == secret_word:
                    break
                print("You got it!")
                print(get_guessed_word(secret_word, letters_guessed))


            else:
                print("Sorry, this letter is not in the word.")
                print(get_guessed_word(secret_word, letters_guessed))
                guess -= 1
                if guess != 0:
                    print("Try again.")

    if guess != 0:
        score = guess * unique_chars(secret_word)
        print("You've won! Your score is", score, ".")
    else:
        print("Tough luck! The word was", secret_word +".")

    return None



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
# #     # pass

# #     # To test part 2, comment out the pass line above and
# #     # uncomment the following two lines.
    
#     secret_word = random.choice(wordlist)
#     hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = "apple"
    hangman_with_hints(secret_word)
