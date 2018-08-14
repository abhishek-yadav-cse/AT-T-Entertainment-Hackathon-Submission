# import textblob
# import csv
import numpy as np
# from gensim.models import Word2Vec
import gensim
from nltk.corpus import sentiwordnet as swn
import random

# import win32com.client as wincl
# speak = wincl.Dispatch("SAPI.SpVoice")

pv = np.load('polar_vector.npy')[0]


# breakdown = swn.senti_synset('breakdown.n.03')
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

gn = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
# tw = gensim.models.KeyedVectors.load_word2vec_format('./word2vec_twitter_model.bin', binary=True, unicode_errors='ignore')


def positivize(word,pm=1.5):
    if word not in gn.vocab: return set()
    x = gn.word_vec(word)
    print("{} polarity: {}".format(word, average_polarity(word)))
    x2 = x + pm * pv
    y = gn.similar_by_vector(x)
    y2 = gn.similar_by_vector(x2)
    return set([xx[0] for xx in y2]) - set([xx[0] for xx in y])

def get_positive_list(word):
    result = positivize(word,pm=1.5)
    if len(result) == 0:
        result = positivize(word,pm=3)
        if len(result) == 0:
            print("no matches")
            return {word}
    return result

r = get_positive_list('terrible')
print(random.choice(list(r)))
    
'''
aw = swn.all_senti_synsets()
word_list = []
polar_words = []
for i,word in enumerate(aw):
    # sent = average_polarity(
    word_polarity = word.pos_score() - word.neg_score()
    word_list.append(word)
    if word_polarity != 0.0: polar_words.append([word,word_polarity])
    if i%1000 == 0: print(i)


def get_sentiment(phrase):
    t = textblob.TextBlob(phrase)
    return t,{'text':phrase,'polarity':round(t.sentiment.polarity*100),'subjectivity':round(t.sentiment.subjectivity*100)}



news=[]
f = open('News_Final.csv','r',encoding='utf8')
c = csv.reader(f)
for line in c:
    news.append(line)
f.close()

sentiments = np.array([[float(x[6]),float(x[7])] for x in news[1:]])
'''


'''
inputs = []
labels = []
names = []
for i, word in enumerate(polar_words):
    word_name = word[0].synset.name()[:-5]
    if word_name in gn.vocab:
        inputs.append(gn.word_vec(word_name))
        labels.append(word[1])
        names.append(word_name)
    if i % 10000 == 0: print(i)
'''
# def replace_random(sent, model=gn):
#     words = sent.split(' ')
#     word_index =  np.random.randint(len(words))
#     word = words[word_index]
#     out_word = word
#     try:
#         nearest_words = model.most_similar_cosmul(word)
#         out_word = nearest_words[0][0]
#     except:
#         print(word + ' not in dictionary')
#     words[word_index] = out_word
#     # return(words)
#     output = ' '.join(words)
#     speak.Speak(output)
#     return output
