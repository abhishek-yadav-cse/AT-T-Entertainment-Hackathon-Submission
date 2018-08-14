import os
import nltk
import random
import numpy as np
from sentiment_testing import *

from nltk.corpus import sentiwordnet as swn
'''
def average_polarity(input_word):
    words = list(swn.senti_synsets(input_word))
    output_polarity=[]
    if len(words) == 1:
        this_word = words[0]
        return this_word.pos_score() - this_word.neg_score()
    for this_word in words:
        usage = int(this_word.synset.name()[-2:])
        if usage <3:
            output_polarity.append(this_word.pos_score() - this_word.neg_score())
    if len(output_polarity) == 0:
        return 0
    else:
        return np.mean(output_polarity)
'''
def most_polarizing_word(words):
    polarity=1
    # out = words.split()[0]
    if not words: return ''
    out = words[0]
    for word in words:
        polarity_buf = average_polarity(word)
        # print(word, polarity_buf)
        if polarity_buf<polarity:
            polarity = polarity_buf
            out=word
    return out

def words_family(input_word):
    words = list(swn.senti_synsets(input_word))
    out = []
    for word in words:
        if word.synset.name().split('.')[0] not in out:
            out.append(word.synset.name().split('.')[0])
    return out if out else [input_word]

def alternate_sentences(input_sentence):
    out = []
    for word in input_sentence.split():
        words_fam = words_family(word)
        # print('words_fam>', words_fam)
        edgiest_word = most_polarizing_word(words_fam)
        # print('most_polarizing_word(words_fam)>', most_polarizing_word(words_fam))
        sentence = input_sentence.replace(word, edgiest_word)
        out.append(sentence)
    return out

out_fp = open('positive_out.txt', 'w')
positive_sentences = alternate_sentences('5 kids killed in accident')

def process_sentence(sentence):
    polarized_word = most_polarizing_word(sentence.strip('.').split())

    positive_word = random.choice(list(get_positive_list(polarized_word)))
    return sentence.replace(polarized_word, positive_word)


# for sentence in alternate_sentences('5 kids killed in accident'):
#     out_fp.write(sentence+'\n')
# out_fp.close()
# print('positive_out.txt>', open('positive_out.txt', 'r').read())
#
# os.system('./fasttext predict-prob model.bin positive_out.txt 2 >x.txt')
# sentences_positivity = open('x.txt', 'r').read()
# print('sentences_positivity>', sentences_positivity)
#
# max_pos = .0
# i=0
# sen_out = ''
# for sent_pos in sentences_positivity.split('\n'):
#     pos_list = sent_pos.split()
#     print('pos_list>', pos_list)
#     if float(pos_list[-1]) > max_pos:
#         max_pos = pos_list[-1]
#         sen_out = positive_sentences[i]
#     i += 1
#
# print(sen_out)
