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


def make_chains(text_string, size_of_ngram):
    """Takes input text as string; returns dictionary of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}
    word_list = text_string.split()

    # for i in range(len(word_list)-size_of_ngram):

    #     key = tuple(word_list[i:i+size_of_ngram])
    #     value = word_list[size_of_ngram+1]      

    #initialize first ngram (which will become the tuple/key) with the first n words in the text
    ngram_list = []
    for i in range(size_of_ngram):
        ngram_list.append(word_list[i])
    ngram = tuple(ngram_list)
    
    # OLD CODE FOR BIGRAMS:
    # first_word = word_list.pop(0)
    # second_word = word_list.pop(0)

    # for each word in our text, add it to the dictionary entry for the ngram preceeding it
    for word in word_list:
        if ngram in chains:
            chains[ngram].append(word)
        else:
            chains[ngram] = [word]

        # also would work:
        # chains[(first_word, second_word)] = chains.get((first_word, second_word), []) + [word]

        # OLD CODE FOR BIGRAMS:
        # first_word = second_word
        # second_word = word

        ngram = ngram[1:] + (word,)
       
        #would also work:
        # ngram_list.pop(0)
        # ngram_list.append(word)
        # ngram = tuple(ngram_list)


        
    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    end_reached = False

    # get first ngram and use it (capitalized) to start our text
    ngrams = chains.keys()  # list of ngrams
    active_ngram = choice(ngrams)  # pick a random starting n-gram

    # if our current starting n-gram doesn't begin with a capital, choose another until it does
    while not active_ngram[0][0].isupper():
        active_ngram = choice(ngrams)

    #put the initial n-gram into the list of words in the new text
    text_list = list(active_ngram)

    # until we reach the end (flagged by an empty list of following words), keep picking a random word from the
    # active ngram's list of followers

    while not end_reached:
        try:
            possible_next_words = chains[active_ngram]  # if at end, throws KeyError
            new_word = choice(possible_next_words)  # if at end, throws IndexError
            text_list.append(new_word)

            # set active_ngram to be new final n words
            active_ngram = active_ngram[1:] + (new_word,)

        #will happen when we hit an ngram with no folowers
        except (KeyError, IndexError):
            end_reached = True

    text = " ".join(text_list)
    return text


input_path = argv[1]
size_of_ngram = int(argv[2])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, size_of_ngram)

# Produce random text
random_text = make_text(chains)

print random_text
