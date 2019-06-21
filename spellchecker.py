# Main part of the program mostly taken from Peter Norvig's post about spell checking: https://norvig.com/spell-correct.html
# Updated the code for readability and moved into a class. The argument-parsing is custom.

import re
import argparse
from collections import Counter

class SpellChecker:
    def __init__(self, wordlist_filename):
        self.wordlist = Counter(
            #self._get_words(open('big-wordlist.txt').read())
            self._get_words(open(wordlist_filename).read())
        )
        self.word_count = sum(self.wordlist.values())

    def _get_words(self, text):
        return re.findall(r'\w+', text.lower())

    def probability(self, word):
        return (float(self.wordlist[word]) / float(self.word_count))

    def correct_spelling(self, word):
        return max(self._candidate_spellings(word), key=self.probability)


    def _candidate_spellings(self, word):
        return (
            self._known([word]) or 
            self._known(self._one_edit_away(word)) or
            self._known(self._two_edits_away(word)) or
            [word]
        )

    def _known(self, words):
        return set(w for w in words if w in self.wordlist)

    def _one_edit_away(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [left + right[1:] for left, right in splits if right]
        transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]
        replaces = [left + char + right[1:] for left, right in splits if right for char in letters]
        inserts = [left + char + right for left, right in splits for char in letters]
        return set(deletes + transposes + replaces + inserts)


    def _two_edits_away(self, word):
        return set(edit2 for edit1 in self._one_edit_away(word) for edit2 in self._one_edit_away(edit1))

spell_checker = SpellChecker('big-wordlist.txt')

parser = argparse.ArgumentParser(description='Correct any typos, either from a text file or direct input')
parser.add_argument('input_file', metavar='input_file', type=str, help='The text file to read')
parser.add_argument('output_file', metavar='output_file', type=str, help='The text file where the spell-checked results will be written. Will be created if does not exist')


args = parser.parse_args()

if args.input_file and args.output_file:
    file_contents = open(args.input_file).read()
    file_words = file_contents.split(' ')

    output = ''

    for word in file_words:
        corrected_word = spell_checker.correct_spelling(word)

        # Preserve capitalization if possible
        if len(corrected_word) == len(word):
            for i in range(0, len(word)):
                properly_capizalized_char = corrected_word[i].upper() if word[i].isupper() else corrected_word[i]
                corrected_word = corrected_word[0:i] + properly_capizalized_char + corrected_word[i+1:]

        output = output + corrected_word + ' '


    output_file = open(args.output_file, 'w')
    output_file.write(output)
