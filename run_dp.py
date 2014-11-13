#!/usr/bin/env python
__author__ = 'scobb'
import sys
from copy import copy


def main(filename):
    """
    Does main processing and produces output
    :param filename: filename to be parsed
    """
    my_pp = Preprocessor(filename)
    my_pp.find_sentences()
    my_pp.output()

class Preprocessor(object):
    """
    class - takes care of the parsing
    """

    def __init__(self, filename):
        f = open(filename, 'r')
        num_words = int(f.readline())
        self.sentences = []
        self.words_by_length = {}
        for _ in range(num_words):
            word = f.readline().strip()
            if len(word) in self.words_by_length:
                self.words_by_length[len(word)].append(word)
            else:
                self.words_by_length[len(word)] = [word]
        self.phrase = f.readline().strip()

    def output(self):
        """
        method - prints output to stdout

        """
        print(len(self.sentences))
        for phrase in self.sentences:
            print(phrase)

    def find_sentences(self):
        arr = [[None for _ in range(len(self.phrase))] for _ in range(len(self.phrase))]

        # don't actually need to check every column; just the first and those we find entries pointing to
        start_to_check = [0]
        for start in start_to_check:
            for end in range(len(arr)):
                length = end+1 - start
                if length <= 0:
                    # can't check words that end before they start
                    continue
                # slice does [start, end), so we'll add 1 to end
                word = self.phrase[start:end+1]
                if length in self.words_by_length:
                    if word in self.words_by_length[length]:
                        # found the word -- find its predecessors
                        fragments = []
                        if start > 0:
                            # if we aren't the first entry
                            for inner_start in range(len(arr)):
                                # find those who pointed us here
                                if arr[inner_start][start-1]:
                                    for their_frag in arr[inner_start][start-1]:
                                        fragments.append(their_frag + ' ' + word)
                        else:
                            fragments = [word]
                        arr[start][end] = fragments
                        start_to_check.append(end+1)

        for row in arr:
            if row[-1]:
                for sentence in row[-1]:
                    self.sentences.append(sentence)


if __name__ == '__main__':
    filename = ''
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Usage: %s <filename>" % sys.argv[0])
        exit(1)
    main(filename)