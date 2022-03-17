import string
from pathlib import Path
from collections import Counter
from itertools import chain
import operator


# list of words
DICT = '/usr/share/dict/british-english'

# rules of the game
ALLOWED_CHARACTERS = set(string.ascii_letters) # only aplhabetical characters
ALLOWED_ATTEMPTS = 6 # no more than 6 attempts
WORD_LENGTH = 5 # length of word is always 5

# set comprehension to generate a set of legit words
# that adhere the rules of the game
WORDS = {word.lower() for word in Path(DICT).read_text().splitlines() if \
        len(word) == WORD_LENGTH and set(word) < ALLOWED_CHARACTERS}

# absolute count of letters in DICTIONARY
LETTER_COUNTER = Counter(chain.from_iterable(WORDS))

# dict comprehension to enumerate each key and value of 
# LETTER_COUNTER and dividing values by the total overall count
LETTER_FREQUENCY = {character: value / sum(LETTER_COUNTER.values()) for \
    character, value in LETTER_COUNTER.items()}


def is_word_common(word):
    """
    function to score words by the frequency of its letters.
    More unique characters are given more weight than the ones
    with fewer unique characters

    """

    score = 0.0

    for char in word:
        score += LETTER_FREQUENCY[char]
    return score / (WORD_LENGTH - len(set(word)) + 1) # + 1 to prevent ZeroDivision exception

def sort_common_words(words):
    """
    Generate a list of tuples containing the word and calculated score for that
    word, sorted by score in descending order.
    """
    sort_by = operator.itemgetter(1)
    return sorted([(word, is_word_common(word)) for word in words], \
            key=sort_by, reverse=True, )

def word_table(word_commonalities):
    """
    format words and their score to a siple table
    """
    for (word, freq) in word_commonalities:
        print(f"{word:<10} | {freq:<5.2}")

def input_word():
    """
    The word we input to Wordle
    """
    while True:
        word = input("The wordle Word: ")
        if len(word) == WORD_LENGTH and word.lower() in WORDS:
            break
    return word.lower()

def wordle_response():
    """
    Recording Wordle response 
    Green letters are limited to just that letter
    Yellow implies complement of that letter
    Gray imply the exlusion of that letter across the vector
    """
    print("Enter color code from Wordle ")
    print(" G for Green")
    print(" Y for Yellow")
    print(" ! for Gray")
    while True:
        response = input("Wordle response: ")
        if len(response) == WORD_LENGTH and set(response) <= {"G", "Y", "!"}:
            break
        else:
            print(f"Invalid answer {response}")
    return response

# Filetring Green, Yellow and Gray letters with Word Vector
# creating a list of sets
word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]

def match_word_vector(word, word_vector):
    """
    If letter is not in the word vector set ath that position, exit with a
    failed match. Otherwise, proceed and, if we exit the loop naturally, return
    True indicating a match.
    """

    assert len(word) == len(word_vector)
    for letter, v_letter in zip(word, word_vector):
        if letter not in v_letter:
            return False
    return True

def match(word_vector, possible_words):
    """
    testing each word against word vector with match_word_vector
    """
    return [word for word in possible_words if match_word_vector(word, \
        word_vector)]


def solve():
    possible_words = WORDS.copy()
    word_vector = [set(string.ascii_lowercase) for _ in \
    range(WORD_LENGTH)]

    for attempt in range(1, ALLOWED_ATTEMPTS + 1):
        print(f"Attempt {attempt} with {len(possible_words)} possible_words")
        word_table(sort_common_words(possible_words)[:15])
        word = input_word()
        response = wordle_response()
        for idx, letter in enumerate(response):
            if letter == 'G':
                word_vector[idx] = {word[idx]}
            elif letter == 'Y':
                try:
                    word_vector[idx].remove(word[idx])
                except KeyError:
                    pass
            elif letter == "!":
                for vector in word_vector:
                    try:
                        vector.remove(word[idx])
                    except KeyError:
                        pass
        possible_words = match(word_vector, possible_words)



solve()
