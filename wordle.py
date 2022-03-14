import string
from pathlib import Path
from collections import Counter
from itertools import chain
import operator

DICT = '/usr/share/dict/british-english'

ALLOWED_CHARACTERS = set(string.ascii_letters)
ALLOWED_ATTEMPTS = 6
WORD_LENGTH = 5


WORDS = {word.lower() for word in Path(DICT).read_text().splitlines() if \
        len(word) == WORD_LENGTH and set(word) < ALLOWED_CHARACTERS}

LETTER_COUNTER = Counter(chain.from_iterable(WORDS))

LETTER_FREQUENCY = {character: value / sum(LETTER_COUNTER.values()) for \
    character, value in LETTER_COUNTER.items()}


def is_word_common(word):
    score = 0.0

    for char in word:
        score += LETTER_FREQUENCY[char]
    return score / (WORD_LENGTH - len(set(word)) + 1)

def sort_common_words(words):
    sort_by = operator.itemgetter(1)
    return sorted([(word, is_word_common(word)) for word in words], \
            key=sort_by, reverse=True, )

def word_table(word_commonalities):
    for (word, freq) in word_commonalities:
        print(f"{word:<10} | {freq:<5.2}")

def input_word():
    while True:
        word = input("The wordle Word: ")
        if len(word) == WORD_LENGTH and word.lower() in WORDS:
            break
    return word.lower()

def wordle_response():
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


word_vector = [set(string.ascii_lowercase) for _ in range(WORD_LENGTH)]

def match_word_vector(word, word_vector):
    assert len(word) == len(word_vector)
    for letter, v_letter in zip(word, word_vector):
        if letter not in v_letter:
            return False
    return True

def match(word_vector, possible_words):
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
