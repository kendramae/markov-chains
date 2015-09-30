from random import choice
from sys import argv


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    text_file = open(file_path)
    text = text_file.read()

    return text


def add_text_to_chains(chains, size_of_ngram, text_string):
    """
    Takes a dictionary (our dictionary of chains) and a text string; returns the same dictionary
    with markov chains added from the text string.

    A chain will be a key that consists of a tuple of (word1, word2, ..., wordn)
    and the value would be a list of the word(s) that follow those n words in the input text.

       >>> make_chains({}, 2, "hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}

    """
    word_list = text_string.split()
    word_list.append(None)

    #initialize first ngram (which will become the tuple/key) with the first n words in the text
    ngram_list = []
    for i in range(size_of_ngram):
        ngram_list.append(word_list[i])
    ngram = tuple(ngram_list)
    
    # for each word in our text, add it to the dictionary entry for the ngram preceeding it
    for word in word_list:
        if ngram in chains:
            chains[ngram].append(word)
        else:
            chains[ngram] = [word]

        ngram = ngram[1:] + (word,)

    return chains



def make_master_chains_dict(size_of_ngram, text_strings_list):
    """Takes the size_of_ngram and a list of text strings, feeds those to add_text_to_chains; 
    returns one dictionary with all markov chains.
    """

    chains = {}
    for text_string in text_strings_list:
        chains = add_text_to_chains(chains, size_of_ngram, text_string)
    
    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    ngrams = chains.keys()  # list of ngrams (which are tuples)
    active_ngram = choice(ngrams)  # pick a random starting n-gram

    # if our current starting n-gram doesn't begin with a capital, choose another until it does
    while not active_ngram[0][0].isupper():
        active_ngram = choice(ngrams)

    #put the initial n-gram into the list of words which will be joined to become new text
    text_list = list(active_ngram)

    # until we reach the end (flagged by a None from choice(possible_next_words)), keep picking 
    # a random word from the active ngram's list of followers
    while True:
        possible_next_words = chains[active_ngram]
        new_word = choice(possible_next_words)

        if new_word == None:
            break
        elif len(text_list) >= 500 and new_word.endswith((".", "?", "!")):
            text_list.append(new_word)
            break
        else:
            text_list.append(new_word)

            # set active_ngram to be new final n words
            active_ngram = active_ngram[1:] + (new_word,)

    #convert list into text string and return it
    text = " ".join(text_list)

    return text


size_of_ngram = int(argv[1])

#get filepaths from command line
input_path_list = []
for arg in argv[2:]:
    input_path_list.append(arg)

# Open the file(s) and turn it/them into one long string, which then gets added to list of text strings
input_text_list = []
for input_path in input_path_list:
    text_string = open_and_read_file(input_path)
    input_text_list.append(text_string)

#create master dictionary of chains
master_chains_dict = make_master_chains_dict(size_of_ngram, input_text_list)

# Produce random text
random_text = make_text(master_chains_dict)

print random_text
