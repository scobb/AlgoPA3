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
                        predecessors = []
                        if end >= 0:
                            for inner_start in range(len(arr)):
                                # find those who pointed us here
                                if arr[inner_start][start-1]:
                                    predecessors.append(arr[inner_start][start-1])
                        arr[start][end] = {'word': word,
                                           'predecessors': predecessors}
                        start_to_check.append(end+1)

        for row in arr:
            if row[-1]:
                self.build_sentences('', row[-1])

    def build_sentences(self, sentence, obj):
        sentence = copy(sentence)
        sentence = obj['word'] + " " + sentence
        if not obj['predecessors']:
            self.sentences.append(sentence.strip())
        else:
            for predecessor in obj['predecessors']:
                self.build_sentences(sentence, predecessor)





if __name__ == '__main__':
    filename = ''
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Usage: %s <filename>" % sys.argv[0])
        exit(1)
    main(filename)