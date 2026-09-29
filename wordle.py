import random
import os


##prompts user for a guess of the word
def get_guess(dictionary):
    guess = input("Guess: ").lower()
    #check if guess is 5 characters long
    while len(guess) != 5:
        print("Guess must be 5 letters long")
        guess = input("Guess: ").lower()
        print("\n")
    #check if guess is actually a word
    count = 0
    while count == 0:
        for word in dictionary:
            if word == guess:
                count = 1
        if count == 0:
            print("Guess must be an actual word........")
            guess = input("Guess: ").lower()
            print("\n")

    return guess

## desplays the results of the guess and all previous guesses
def display_results(secret_word, guess_list):
    print('\n\n')
    #iterate thru each letter of each guessed word and print in correct color
    for word in guess_list:
        #count position of each letter of word
        letter_list = list(word)
        pair_list = []
        for let in letter_list:
            pair = [let, 'N/A']
            pair_list.append(pair)

        #list to count how many characters of each type have been colored        
        y_count = []
        p = ['5', 0, 0]
        y_count.append(p)
        c = 0 
        for char in secret_word:
            for pair__ in y_count:
                if pair__[0] == char:
                    pair__[1] += 1
                    c += 1
            if c == 0:
                p = [char, 1, 0]
                y_count.append(p)
            c = 0
                                
        count = 0
        for letter in letter_list:
            print_check =  False
            #iterate thru each char in secret word to find matching pair and color letter appropriately 
            for character in secret_word:
                if letter == character:
                    #color either green if letter matches letter in secret word, or yellow if letter is somewhere in secret word
                    if word[count] == secret_word[count] and print_check == False:
                        prGreen(letter.upper())
                        print_check = True
                        pair_list[count][1] = 'G'
                        for entry in y_count:
                            if entry[0] == letter:
                                entry[2] += 1
                    else:
                        if print_check == False:
                            # determine if another character that is same letter has also been highlighted or if word has also been found
                            for pair_ in pair_list:
                                if pair_[0] == letter and pair_[1] != 'G' and pair_[1] != 'Y':
                                    for pp in y_count: 
                                        if pp[2] < pp[1] and letter == pp[0]:
                                         count_count = 0
                                         for i in range(count + 1, 5):
                                            if letter == letter_list[i]:
                                                count_count = 1
                                         if count_count == 0:
                                                prYellow(letter.upper())
                                                print_check = True
                                                pair_list[count][1] = 'Y'
                                                pp[2] += 1
            if print_check == False:
                print(letter.upper(), end= '')
                pair = [letter, 'N/A']
                pair_list.append(pair)
            count += 1
        print("\n")

    
#color text functions ---> Citation: https://www.geeksforgeeks.org/python/print-colors-python-terminal/
def prGreen(s): print("\033[92m{}\033[00m".format(s), end= '')
def prYellow(s): print("\033[93m{}\033[00m".format(s), end= '')



def check_game(guess, lives, secret_word):
    #check if player guessed secret word or ran out of guesses
    if guess == secret_word or lives == 0:
        return True
    else:
        return False

def generate_word(dictionary):
    random_word = ''
    length = len(dictionary) - 1
    #generate word until word is 5 characters long
    while len(random_word) != 5:
        rand_entry = random.randint(0, length)
        random_word = dictionary[rand_entry]
    return random_word
    

def load_dict():
   # 1. Get the directory where this script file lives
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Safely join that directory path with your relative path
    dictionary_txt = os.path.join(script_dir, "words_alpha.txt")

    # open dictionary and make copy to return
    with open(dictionary_txt, encoding="utf-8") as file:
        # make copy
        lines = file.readlines()
        dictionary_copy = []
        for line in lines:
            clean_line = line.strip()
            dictionary_copy.append(clean_line)
        # return copy
        return dictionary_copy


### !!!!!AI SECTION!!!!
##Comments:
## My AI makes random guesses that are weighted with the distribution of letters in the English vocabulary
## It makes guesses until the guess matches a word in my loaded dictionary
## then, it goes through each letter of the guess and records whether that letter is in the word at all, and appends it to dont_letters
## then the cycle repeats until it either runs out of guesses or guesses correctly

## Pros: My AI almost always makes the correct guess within 6 guesses, and usually beats the user(me). It is very accurate and effective
## Cons: The data it has to store and sift through takes up a lot of memory, making it a bit slow ---> it brute forces the solution (not very elegant)

##random number generator that the ai uses
def get_number(nums, weights, dont_letters, placement, common_letters):
    #this generates a random number corresponding to a letter thats weighted to the natural frequency of letters in the english vocabulary
    rand_num = random.choices(nums, weights=weights, k=1 )
    number = int(rand_num[0])
    #this checks if the letter was already guessed and was false... or if the letter even appears in the mystery word
    if common_letters[number] not in dont_letters[placement]:
        return number
    else:
        #if not, the generation process is run again
        number = get_number(nums, weights, dont_letters, placement, common_letters)
    return number
         

## generates the next guess the ai makes
def get_next_guess(common_letters, correct_dict, dict_check, dont_letters, char_list):
    #this function is really the ai itself --> it generates the guesses
    #here im just defining some variables for inputs to other functions.

    # I arbitrairly set the guess list to this so i had a list of 5 items
    guess = ["z","z","z","z","z"]
    #weights and nums are used to generate a random number, 0-25, corresponding to a letter in common_letters in the get_number function
    #this generator is weighted to the natural frequency of letters in words --> https://norvig.com/mayzner.html
    weights = [445, 330, 286, 272, 269, 257, 232, 223, 180, 145, 136, 119, 97, 89, 85, 76, 66, 59, 59, 52, 37, 19, 8, 5, 4, 3]
    nums = range(0, 26)
    #the dont list is used to make sure the letters which were guessed correctly dont change
    dont = []
    keys = correct_dict.keys()
    for key in keys:
        for number in correct_dict[key]:
            num = int(number)
            guess[num] = key
            dont.append(num)
    
  #this while loop generates guesses until it matches a word in the dictionary & contains the letters that were guessed correctly
    check = False
    while check == False:
        for i in range(5):
            if i not in dont:
                rand_num = get_number(nums, weights, dont_letters, i, common_letters)
                number = rand_num
                guess[i] = common_letters[number]
        if dict_check[guess[0]][guess[1]][guess[2]][guess[3]][guess[4]] == True:
            check = True
    
    #here I append my dont_letters nested list. this list is used to compile all the letters in each position that are either a) not in that position 
    # or b) not in the word
    for i in range(5):
        for j in range(5):
            if char_list[j] != guess[i] and guess[i] not in dont_letters[j]:
                dont_letters[j].append(guess[i])
    
    word = ''.join(guess)
    return word, dont_letters           

 #this function returns a nested dictionary, where all the paths corresponding to the words in my loaded dictionary words_alpha.txt are set to true. 
#this makes it easier to check the guesses the ai makes
def get_dictionary_check(dictionary):
    dict_check = {}
    alpha = "abcdefghijklmnopqrstuvwxyz"
    alphabet = list(alpha)
    for letter in alphabet:
        dict_check[letter] = {}
        for lette in alphabet:
            dict_check[letter][lette] = {}
            for lett in alphabet:
                dict_check[letter][lette][lett] = {}
                for let in alphabet:
                    dict_check[letter][lette][lett][let] = {}
                    for le in alphabet:
                        dict_check[letter][lette][lett][let][le] = False

    for word in dictionary:
        if len(word) == 5:
            l_list = list(word)
            dict_check[l_list[0]][l_list[1]][l_list[2]][l_list[3]][l_list[4]] = True
    return dict_check


            
# executes ai methods to guess the hidden word
def ai(dictionary, secret_word):
    #list of list of letters that is not in word
    dont_letters = [[], [], [], [], []]
    #split secret word into characters 
    character_list = list(secret_word)
    lives = 5
    dict_check = get_dictionary_check(dictionary)
    #list of letters ranked by frequency in the english language
    common = "etaoinsrhldcumfpgwybvkxjqz"
    common_letters = list(common)
    #get first guess
    correct_dict = {}
    guesses_list = []
    guess, dont_letters = get_next_guess(common_letters, correct_dict, dict_check, dont_letters, character_list)
    #make list of ai guesses
    guesses_list.append(guess)
    possible_dict = {}
    #makes guesses
    while lives != 0:

        guess_list = list(guess)
        for i in range(5):
            possible_dict[guess_list[i]] = 0
            correct_dict[guess_list[i]] = []
        #compare initial guess to secret word and check if there are any matching letters --> record position
        for i in range(5):
            g_letter = guess_list[i]
            s_letter = character_list[i]
            if g_letter == s_letter:
                correct_dict[g_letter].append(str(i))
        guess, dont_letters = get_next_guess(common_letters, correct_dict, dict_check, dont_letters, character_list)
        guesses_list.append(guess)
        lives -= 1
        if guess == secret_word:
            lives = 0
    print("\n")
    print("~~~~AI~~~~")
    display_results(secret_word, guesses_list)
    #Return guesses list so i can figure out who won
    return guesses_list


## TEST + MAIN SECTION

def test():
    #test if dictionary gets loaded properly
    dictionary = load_dict()
    print(dictionary)

    
    #test if word generation works
    for i in range(5):
        word = generate_word()
        print(word)

    #test if get_guess works
    word = get_guess()

    #test if display results works
    words = ["CRANE", "PORTS"]
    display_results(word, words)

    #test if check_game works
    guess = "SPORT"
    lives = 3
    check = check_game(guess, lives, word)
    print(str(check))

#
def ai_test():
    dictionary = load_dict()
    secret_word = generate_word(dictionary)
    print(secret_word)
    ai(dictionary, secret_word)

# executes a game of wordle where you play against the ai
def play_wordle():
    #load in dicitonary
    dictionary = load_dict()
    #Generate a five letter random word
    secret_word = generate_word(dictionary)
    secret_word_ai = secret_word
    secret_word = secret_word.upper()
    #generate empty string to store guess + list to append all guesses to
    guess_list = []
    guess = ''
  
    #repeat until player guesses word correctly or runs out of guesses
    lives = 6
    while check_game(guess, lives, secret_word) == False:
        #prompt user for a guess
        guess = get_guess(dictionary).upper()
        guess_list.append(guess)
        # deduct number of remaining guesses if guess is incorrect
        if guess != secret_word:
            lives -= 1

        #display results of guess 
        display_results(secret_word, guess_list)
    #check if player has won or lost
    if len(guess_list) == 6:
        print("Word: ", secret_word)
    #run ai and display results
    ai_list = ai(dictionary, secret_word_ai)
    #check to see who won
    if len(ai_list) < len(guess_list):
        print("You lost.....")
   

def main():
    play_wordle()


main();

