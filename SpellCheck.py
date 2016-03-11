### Assignment 2 for CE/CZ 1003 by LAKHOTIA SUYASH ###


import time

start_time = time.time() # Stores the start time of the database creation.

flag_wordlist = False

print("Initial setup started.")
print("")

try:
    words_set = set(open('big.txt', 'r').read().lower().split()) # Words are put in a set instead of a list to avoid duplicates.

    # The statements below add word_list.txt to the database as well. They have been commented out to decrease the setup time from ~5.2s to ~1.3s.
    # words_set = words_set | set(open('word_list.txt', 'r').read().lower().split())
    # flag_wordlist = True
except FileNotFoundError:
    print("File(s) not found. Please make sure the file(s) are in the same directory as the Python program.") # Program comes here if either of the .txt files are not in the same directory as the .py file.
    raise SystemExit(0) # Quits the program.

if flag_wordlist:
    print("Files < big.txt > & < word_list.txt > have been read.")
else:
    print("File < big.txt > has been read.")

words_list = list(words_set) # Converted to list to allow ordered iteration & indexing.


for i in range(0, len(words_list)): # Iterates over the list of extracted words.
    w = list(words_list[i]) # Creates a list of the characters in the particular word.

    nonalpha = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "=", "[", "]", "{", "}", "|", "\\", ";", ":", "\"", ",", ".", "<", ">", "/", "?"]
    # In nonalpha[], there is no single hyphen or single apostrophe as specific filtration happens for these two characters later.
    
    for j in range(0, len(w)): # Loops through all the characters of the word.
        if ord(w[j]) in range(48, 58):
            words_list[i] = "" # Deletes any word that contains a numerical digit.
            break

        if w[j] in nonalpha:
            words_list[i] = words_list[i].replace(w[j], "") # Deletes any character in the word that is non-alphanumeric. Does not delete the word.               


    w = list(words_list[i]) # Resets w so that it is now the semi-filtered word (without digits & characters from nonalpha[]).

    for j in range(0, len(w)): # w needs to be reset because the following filtration depends on the positioning of the characters.
        if w[j] == "'" and j != (len(w) - 2) and j != (len(w) - 3) and j != 1: # Deletes apostrophes only when the apostrophe is not at the second, second-last or third-last position to allow words like "o'clock", "can't" and "he'll".
            words_list[i] = words_list[i].replace("'", "")

        if len(w) > 1 and w[j] == "-" and ((j == 0 and w[j + 1] != "-") or (j == (len(w) - 1) and w[j - 1] != "-")): # Deletes hyphens only at the start or end of the word and only if it is not part of a double hyphen i.e. "--".
            words_list[i] = words_list[i].replace(w[j], "")
            

    words_list[i] = words_list[i].replace("--", "") # Deletes double hyphens from the word. Not in nonalpha[] because it is not a single character.


words_list = [x for x in words_list if x != ""] # Removes all blank elements that may have been created during filtration.

words_set = set(words_list) # Converted back to set to remove any duplicates that may have been created during filtration.

print("{} unique words extracted.".format(len(words_set))) # Prints the final number of words in the database.
print("")

words_list = list(words_set) # Converted back to list to allow ordered iteration & indexing.

print("Initial setup took {} seconds.".format(str((time.time() - start_time))[:6])) # Prints the time taken to create the database.
print("")

print("Type < spellcheck(\"yourWord\") > for spelling suggestions.")




def worddistance(input_word, database_word):
    """Checks the "distance" between two words to get possible outcomes for spellcheck()."""
    
    dist_left = 0 # Word distance based on character comparison from the left.
    dist_right = 1000 # Word distance based on character comparison from the right. Set to 1000 here for cases when the length of input_word & database_word is same.
    dist_strip = 1000 # Word distance based on character stripping. Set to 1000 here for cases when the difference in the word lengths not 1 or 2.
    distance = 0 # Final word distance. This will be returned by the function.

    input_word = input_word.replace("-", "") # Removes any hyphen from the input word.
    database_word = database_word.replace("-", "") # Removes any hyphen from the database word. However, suggestions will still show the hyphen.
    
    inList = list(input_word) # Makes a list of the characters in the input word.
    dataList = list(database_word) # Makes a list of the characters in the database word.


    x = min(len(inList), len(dataList)) # Checks which word is shorter to avoid IndexError in the following while loop.

    i = 0
    
    while i < x:
        if inList[i] != dataList[i]: # Checks whether two corresponding characters are different.
            if (i+1) < x and inList[i] == dataList[i+1] and inList[i+1] == dataList[i]: # Checks for a transposition error. Minimum word distance (1) is added for a transposition error because it is the most common error while typing.
                dist_left = dist_left + 1
                i = i + 2
                continue
            else: # Comes here if the characters are different but it is not a transposition error.
                dist_left = dist_left + 2 # Without the if statement, this statement would have run twice for a transposition error, adding 4 to the word distance.
                i = i + 1
                continue
        
        i = i + 1



    if len(inList) < len(dataList): # Checks the word distance from the right for inputs like "esting" whose suggestions should be "testing", "resting" etc i.e. words that have a missing character(s) at the start.
        dist_right = 0
        
        y = abs(len(inList) - len(dataList))

        i = x - 1

        while i >= 0:
            if inList[i] != dataList[i + y]: # Checks whether two corresponding characters are different from the right side.
                if (i - 1) >= 0 and inList[i] == dataList[(i + y) - 1] and inList[i - 1] == dataList[i + y]:
                    dist_right = dist_right + 1
                    i = i - 2
                    continue
                else:
                    dist_right = dist_right + 2
                    i = i - 1
                    continue
            
            i = i - 1


    if len(inList) > len(dataList): # Checks the word distance from the right for inputs like "abut" whose most likely suggestion should be "but" i.e. words that have an extra character(s) at the start.
        dist_right = 0

        y = abs(len(inList) - len(dataList))

        i = x - 1

        while i >= 0:
            if inList[i + y] != dataList[i]: # Checks whether two corresponding characters are different from the right side.
                if (i - 1) >= 0 and inList[(i + y) - 1] == dataList[i] and inList[i + y] == dataList[i - 1]:
                    dist_right = dist_right + 1
                    i = i - 2
                    continue
                else:
                    dist_right = dist_right + 2
                    i = i - 1
                    continue
            
            i = i - 1



    # The below code gives the word distance for user inputs where they may have inserted 1 or 2 extra characters. For eg. "truley" for "truly".
    # The user is given an error margin of two extra characters as this would be the maximum for a normal person typing.
    # Character stripping (below) allows the word distance to be lesser than what it would be with character comparison (above).
    if len(input_word) == (len(database_word) + 1):
       in_strip = list(input_word)

       for s in range(0, len(input_word)):
            del in_strip[s]
            
            stripped_in = "".join(in_strip)

            if stripped_in == database_word:
                dist_strip = 0 # If a word is found with only a single character deletion, the word distance will only come from the length difference i.e. 2 * 1 = 2.

            in_strip = list(input_word)
            
    elif len(input_word) > 2 and len(input_word) == (len(database_word) + 2):
       in_strip = list(input_word)

       for s in range(0, len(input_word)):
           del in_strip[s]
           
           for t in range(0, len(input_word)):
               if t != s:
                    del in_strip[t]
                    
                    stripped_in = "".join(in_strip)

                    if stripped_in == database_word:
                        dist_strip = 0 # If a word is found with a double character deletion, the word distance will only come from the length difference i.e. 2 * 2 = 4.

                    in_strip = list(input_word)
        


    # The below code gives the minimum word distance for user inputs where they may have forgotten 1 or 2 characters. For eg. "honstly" for "honestly".
    # The user is given an error margin of two missing characters as this would be the maximum for a normal person typing.
    if (len(input_word) + 1) == len(database_word):
       data_strip = list(database_word)

       for s in range(0, len(database_word)):
            del data_strip[s]
            
            stripped_data = "".join(data_strip)

            if input_word == stripped_data:
                dist_strip = 0 # If a word is found with only a single character insertion, the word distance will only come from the length difference i.e. 2 * 1 = 2.

            data_strip = list(database_word)

    elif len(database_word) > 2 and (len(input_word) + 2) == len(database_word):
       data_strip = list(database_word)

       for s in range(0, len(database_word)):
            del data_strip[s]

            for t in range(0, len(input_word)):
                if t != s:
                    del data_strip[t]
                    
                    stripped_data = "".join(data_strip)

                    if input_word == stripped_data:
                        dist_strip = 0 # If a word is found with a double character insertion, the word distance will only come from the length difference i.e. 2 * 2 = 4.

                    data_strip = list(database_word)

    

    distance = min(dist_left, dist_right, dist_strip) # Takes the minimum of the three word distances calculated in order to give the most accurate suggestion(s).
        
    distance = distance + 2*(abs(len(inList) - len(dataList))) # The difference in the length of the words has more weightage than differing characters.
    
    return distance




def spellcheck(input_word):
    """Type < spellcheck("yourWord") > for spelling suggestions."""

    auto_start = time.time() # Stores the current time as soon as spellcheck() is called.


    # Validating input_word:
    if input_word == "" or len(input_word.split()) > 1 or len(input_word) == 1: # Checks if the user input is one word that has more than one alphabet.
        print("Please enter one word that has more than one alphabet.") # print() instead of return statement to avoid quotation marks.
        return

    num_in = [num for num in list(input_word) if num.isdigit()]

    if len(num_in) > 0: # Checks if the user input has any digits in it.
        print("Encountered a digit. Please enter a valid word.")
        return
    

    input_word = input_word.lower()
    
    suggestions = [] # Will contain all the spelling suggestions.
    worddist = [] # Will contain the word distances of the suggestions in corresponding indexes to suggestions[].
    fin = [] # Will contain the final suggestions that are given to the user first i.e. suggestions with the minimum word distances.
    
    correct = False


    for y in range(0, len(words_list)): # Iterates over the database of words.
        wd = worddistance(input_word, words_list[y]) # Calculates the word distance between the user input and each word in the database.
        
        if wd == 0: # If word distance is equal to 0 with any word in the database, the spelling is correct and spellcheck() terminates.
            correct = True
            print("The spelling is correct.")
            print("Query took {} seconds.".format(str(time.time() - auto_start)[:6]))
            return # Exits spellcheck()

        if len(input_word) > 2:
            if wd <= (len(input_word) - 1): # A suggestion is only added if the word distance is lesser than (len(input_word) - 1)) to get the most accurate suggestions.
                suggestions.append(words_list[y])
                worddist.append(wd)
        else: # To allow accurate spelling suggestions for user inputs like "ru" or "ra".
            if wd <= len(input_word) and len(words_list[y]) > 2: # Most user inputs that have only two letters will have spelling suggestions that are longer than just two letters. For eg. "ra" will most probably mean "ran", "rat" etc.
                suggestions.append(words_list[y])
                worddist.append(wd)

    wait_time = time.time() # Stores the amount of time spent in waiting for user input for the below statement. Subtracted from the time taken to spellcheck.
    
    choice = raw_input("Unrecognized word. Type \"S\" to get spelling suggestions or \"A\" to add this word to dictionary: ").lower() # Takes the user's choice to either receive spelling suggestions or add the word to the database.

    validate = False # Used to validate user input from above. Should only be one of "s", "S", "a" or "A".

    while validate == False: # Runs until user input is valid.
        if choice == "a":
            validate = True
            wait_time = time.time() - wait_time
            
            words_list.append(input_word) # Appends the user input to the database.
            print("New word - \"{}\" - added to dictionary.".format(input_word))
            print("Query took {} seconds.".format(str(time.time() - (auto_start + wait_time))[:6]))
            return # Exits spellcheck()
        elif choice == "s":
            validate = True
            wait_time = time.time() - wait_time
        else:
            choice = raw_input("\"S\" or \"A\" please: ").lower()

    print("") # Prints a blank line.


    if len(suggestions) == 0: # In case no suggestions are found.
        print("The spelling is incorrect, however, spellcheck was unable to find the right spelling.")
        print("Query took {} seconds.".format(str(time.time() - (auto_start + wait_time))[:6]))
        return


    # Arranges suggestions[] according to the corresponding word distance using bubble sort:
    for l in range(len(worddist)):
        for k in range(len(worddist) - 1 - l):
            if worddist[k] > worddist[k + 1]:
                worddist[k], worddist[k + 1] = worddist[k + 1], worddist[k] # Swaps the two values.
                suggestions[k], suggestions[k + 1] = suggestions[k + 1], suggestions[k] # Swaps the two values.


    min_wd = min(worddist) # Calculates the minimum word distance.

    for i in range(0, len(worddist)): # To find the suggestions with the minimum word distance. Note: worddist[] & suggestions[] have corresponding indexes.
        if worddist[i] == min_wd:
            fin.append(suggestions[i]) # Appends a suggestion with the minimum word distance to fin[].

    print("Did you mean {}?".format(", ".join(fin))) # Prints the most likely suggestion(s) based on the word distance.


    # Code below prints the most likely suggestion from fin[] based on the number of occurences of the word in big.txt if there is more than one suggestion in fin[].
    if len(fin) > 1:
        occurences_list = (open("big.txt", "r")).read().lower().split() # Creates a list of all the words in big.txt in lowercase.
        counter_curr = 0
        counter_max = 0

        # Assigns the word in fin[] with the most occurences in big.txt to 'likely':
        for v in fin:
            counter_curr = 0
            
            for w in occurences_list:
                if v == w:
                    counter_curr = counter_curr + 1

            if counter_curr >= counter_max:
                counter_max = counter_curr
                likely = v

        print("The most likely word is: {}".format(likely)) # Prints the most likely suggestion based on the number of occurences in big.txt.
        print("Query took {} seconds.".format(str(time.time() - (auto_start + wait_time))[:6]))
    else:
        print("Query took {} seconds.".format(str(time.time() - (auto_start + wait_time))[:6]))
        


    # spellcheck() also allows the user to receive upto 10 spelling suggestions from suggestions[] if their required suggestion is not in fin[].
    if len(suggestions) != len(fin): # Only runs if fin[] and suggestions[] are of different lengths (i.e. are not same as values are shared).
        if len(suggestions) < 10: # Restricts number of spelling suggestions to 10 to avoid overwhelming the user.
            print("")
            print_all = raw_input("Displaying {} out of {} suggestion(s). Would you like to print all? Y or N? ".format(len(fin), len(suggestions))).lower()
        else:
            print("")
            print_all = raw_input("Displaying {} suggestion(s). Would you like to print the top 10 suggestions? Y or N? ".format(len(fin))).lower()

        validate = False # Used to validate user input from above. Should only be one of "y", "Y", "n" or "N".       
    
        while validate == False: # Runs until user input is valid.
            if print_all == "y": # Prints the Top 10 suggestions if user input is "y" or "Y".
                validate = True
                print("Did you mean {}?".format(", ".join(suggestions[:10]))) # Since suggestions[] is sorted according to the word distance, this will output the most likely 10 suggestions.
            elif print_all == "n":
                validate = True
            else:
                print_all = raw_input("Y or N please: ").lower()
