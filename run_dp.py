#!/usr/bin/env python
__author__ = 'scobb'
import sys


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
        self.words = {}
        for _ in range(num_words):
            self.words[f.readline().strip()] = True
        self.phrase = f.readline().strip()

    def output(self):
        """
        method - prints output to stdout

        """
        print(len(self.sentences))
        for phrase in self.sentences:
            print(phrase)

    def find_sentences(self):
        """
        dynamic programming!! populate dat array. populates self.sentences when finished.
        :return: None
        """
        # declare array full of Nones, NxN where N = len(phrase)
        total_length = len(self.phrase)
        fragments = [[] for _ in range(total_length)]
        runs = 0

        # don't need to check every column; just the first and those we find entries pointing to
        start_to_check = [0]
        for start in start_to_check:
            for end in range(start, total_length):
                length = end + 1 - start
                # slice does [start, end), so we'll add 1 to end
                word = self.phrase[start:end + 1]
                if word in self.words:
                    # found the word -- append to its predecessors
                    if start > 0:
                        # if we aren't the first entry
                        for fragment in fragments[start - 1]:
                            runs += 1
                            fragments[end].append(fragment + ' ' + word)
                    else:
                        fragments[end] = [word]
                    if end + 1 not in start_to_check:
                        # need to make sure we check the words starting right after we end
                        start_to_check.append(end + 1)
                        start_to_check.sort()
        # print(runs)
        for sentence in fragments[-1]:
            self.sentences.append(sentence)


if __name__ == '__main__':
    filename = ''
    try:
        filename = sys.argv[1]
    except:
        print("Usage: %s <filename>" % sys.argv[0])
        exit(1)
    main(filename)