__author__ = 'scobb'
import os
import sys
import re
from run import Preprocessor

def main():
    for topfile in os.listdir(os.getcwd()):
        if topfile.startswith('.') or topfile.startswith('_'):
            continue
        if os.path.isdir(topfile):
            for f in os.listdir(os.path.join(os.getcwd(), topfile)):
                if f.startswith('.') or f.endswith('.out') or f.endswith('~'):
                    continue
                targ = os.path.join(os.getcwd(), topfile, f)
                print(targ)
                pp = Preprocessor(os.path.join(os.getcwd(), topfile, f))
                pp.find_sentences()
                out_file = open('%s_my_%s.out' % (topfile, f), 'w+')
                normal_stdout = sys.stdout
                sys.stdout = out_file
                pp.output()
                out_file.close()
                sys.stdout = normal_stdout



    for f in os.listdir(os.getcwd()):
        if 'my' in f:
            regex = r'([^_]*)_my_([^\.]*\.out)'
            match_obj = re.match(regex, f)
            if match_obj:
                folder = match_obj.group(1)
                file = match_obj.group(2)
                mine = f
                key = os.path.join(folder, file)

                key_file = open(key, 'r')
                my_file = open(mine, 'r')

                key_phrases = [line for line in key_file.readlines()]
                my_phrases = [line for line in my_file.readlines()]

                key_count = key_phrases[0]
                key_phrases = key_phrases[1:]
                my_phrases = my_phrases[1:]

                key_file.close()
                my_file.close()

                count = 0
                for phrase in key_phrases:
                    if phrase not in my_phrases:
                        print(phrase + ' not in my phrases.')
                        break
                    else:
                        count += 1

                if count != int(key_count):
                    print('Onoez! Count was %d while key_count was %s' % (count, key_count))
                else:
                    print('for %s, found %d matches' % (mine, count))
    print("complete")

if __name__ == '__main__':
    main()