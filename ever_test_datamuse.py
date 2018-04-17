from datamuse import datamuse
import itertools
import string
api = datamuse.Datamuse()

def get_list(dictionary,word):
    rel_words = []
    for d in dictionary:
        w = d['word']
        rel_words.append(w)
    rel_words.append(word)
    return rel_words

def get_word_list(file_name):
    text = open(file_name,'r')
    lines = list(text)
    lines1 = []
    for line in lines:
        line = line.strip(string.whitespace)
        for i in range(32):
            line = line.replace(string.punctuation[i],'')
        line = line.replace('','')
        line = line.lower()
        lines1.append(line)
    stringlines = ' '.join(lines1)
    return lines1

list1 = get_word_list('InClassSurveyPickuplines.txt')
list2 = get_word_list('CarpeSurveyPickuplines.txt')
list3 = get_word_list('Disney.txt')
list4 = get_word_list('emma_lines.txt')
list5 = get_word_list('more.txt')
list6 = get_word_list('Music.txt')
list7 = get_word_list('random.txt')

main_list = list1+list2+list3+list4+list5+list6+list7

key_word = input("Pls give me a keyword \n")
related_words = []
related_words+=(get_list(api.words(ml = key_word, max = 10),key_word))
print("\n######### related_words ##########")
print(related_words)

new_list = []
for word in related_words:
    temp_rel_words = get_list(api.words(rel_trg = word, max = 10),word)
    new_list = new_list + temp_rel_words
print("\n######### new_list ##########")
print(new_list)

good = []
for line in main_list:
    split_list = line.split()
    for word in split_list:
        if word in new_list:
            good.append(line)
print("\n######### pickup_lines ##########")
print(good)
