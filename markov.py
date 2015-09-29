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

    #initialize first ngram (which will become the tuple/key) with the first n words in the text
    ngram_list = []
    for i in range(size_of_ngram):
        ngram_list.append(word_list.pop(0))
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

        ngram_list.pop(0)
        ngram_list.append(word)
        ngram = tuple(ngram_list)
        
    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""


    ngrams = chains.keys()  # list of ngrams
    end_reached = False

    # get first ngram and use it (capitalized) to start our text
    active_ngram = list(choice(ngrams))
    text = "{}".format(active_ngram[0].capitalize())
    if len(active_ngram) > 1:
        for word in active_ngram[1:]:  #everything but the first word in the n-gram
            text += " {}".format(word)

    # text = "{first} {second}".format(first=active_ngram[0].capitalize(), second=active_ngram[1])

    # until we reach the end (flagged by an empty list of following words), keep picking a random word from the
    # active ngram's list of followers
    while not end_reached:
        try:
            possible_next_words = chains[tuple(active_ngram)]  # if at end, throws KeyError
            new_word = choice(possible_next_words)  # if at end, throws IndexError
            text += " {new}".format(new=new_word)

            # set active_ngram to be new final n words
            active_ngram.pop(0)
            active_ngram.append(new_word)

            # active_ngram = (active_ngram[1], new_word)

        #will happen when we hit an ngram with no folowers
        except (KeyError, IndexError):
            end_reached = True

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
