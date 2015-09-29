from random import choice


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text, processing text to
    remove linebreaks.
    """

    text_file = open(file_path)
    text = text_file.read()
    text = text.replace("\n", " ")

    return text


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}
    word_list = text_string.split(" ")

    #initialize first and second words (which will become the tuple/key) with the first two words
    #in the text
    first_word = word_list.pop(0)
    second_word = word_list.pop(0)

    # for each word in our text, add it to the dictionary entry for the bigram preceeding it
    for word in word_list:
        if (first_word, second_word) in chains:
            chains[(first_word, second_word)].append(word)
        else:
            chains[(first_word, second_word)] = [word]

        # also would work:
        # chains[(first_word, second_word)] = chains.get((first_word, second_word), []) + [word]

        first_word = second_word
        second_word = word

        
        
    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""


    bigrams = chains.keys()
    end_reached = False
    active_bigram = choice(bigrams)
    text = "{first} {second}".format(first=active_bigram[0].capitalize(), second=active_bigram[1])

    while not end_reached:
        try:
            possible_next_words = chains[active_bigram]
            new_word = choice(possible_next_words)
            text += " {new}".format(new=new_word)
            active_bigram = (active_bigram[1], new_word)
        except (IndexError, KeyError):
            end_reached = True

    return text


input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print random_text
