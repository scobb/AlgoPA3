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
        """
        method - finds all possible phrases using build_phrase method

        """
        ind = len(self.phrase) - 1
        self.build_sentence('', ind, len(self.phrase))


    def build_sentence(self, sentence, ind, end_ind):
        """
        method - recursively builds phrases with words in self.words_by_length from
        self.phrase. Appends result to self.phrases
        :param sentence: sentence to this point
        :param ind: beginning index to look at self.phrase
        :param end_ind: end index to look at self.phrase
        :return: None
        """
        # make a new copy to manipulate
        sentence = copy(sentence)
        if ind < 0:
            # base case
            if end_ind == 0:
                # we've used the whole phrase
                self.sentences.append(sentence)
                return
            else:
                # we haven't used the whole phrase
                return
        # the phrase we're examining - a slice of the full phrase
        active_phrase = self.phrase[ind:end_ind]

        # can we make a word?
        if len(active_phrase) in self.words_by_length:
            if active_phrase in self.words_by_length[len(active_phrase)]:
                new_phrase = active_phrase + ' ' + sentence
                if new_phrase.endswith(' '):
                    new_phrase = new_phrase[0:-1]
                # "take" recursive call
                self.build_sentence(new_phrase, ind - 1, ind)
        # "leave" recursive call
        self.build_sentence(sentence, ind - 1, end_ind)


if __name__ == '__main__':
    filename = ''
    try:
        filename = sys.argv[1]
    except IndexError:
        print("Usage: %s <filename>" % sys.argv[0])
        exit(1)
    main(filename)