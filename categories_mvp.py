#Importing libraries and functions
from processing_pickup_lines2 import *
from datamuse import datamuse
import itertools
import string
#defining useful functions
def get_list(dictionary,word):
    rel_words = []
    for d in dictionary:
        w = d['word']
        rel_words.append(w)
    rel_words.append(word)
    return rel_words

def standardize_format(word):
    """
    Input: unformatted string of a word
    Output: string of that word w/ no punctuation or capitalization
    """
    for c in string.punctuation:
        word = word.replace(c," ")
    word = word.lower()
    return word

def get_related_words(keyword,n = 10):
    """Input: keyword, n
       Output: list containing keyword and up to n related words (10 by default)"""
    related_words = []
    related_words.append(key_word)
    related_words += (get_list(api.words(ml = key_word, max = n),key_word))
    return related_words

def get_trigger_words(related_words,n = 10):
    """Input: list of related_words, n
       Output: list containing all of the related words, as well as n trigger words per related words
       """
    trigger_words =[]
    trigger_words += related_words
    trigger_words += (get_list(api.words(rel_trg = key_word, max = n),key_word))
    return trigger_words

def find_category(related_words):
    """Input: list of words including keyword and related words
       Output: dictionary of pickuplines related to the original keyword,
               False if no dictionary is found

       This function goes through each of the words in the list and searches
       for a category of the same name. If it finds one, it returns that
       dictionary.
       """
    for related_word in related_words:
        for category in all_dicts: #for every category dictionary within the main dictionary
            if related_word == category: #if the related word is the same as the name of the category
                return(all_dicts[related_word]) #return the dictionary of that category
    return False

def all_in_one(all_dicts):
    """Input: dictionary containing dictionaries of all the categories
       Output: dictionary containing all of the pickup lines from all categories
       """
    all_lines = {}
    for category in all_dicts:
        all_lines += category

def create_category(key_word,trigger_words,all_dicts):
    """
    Input: trigger_words is a list containing the original keyword, related words, and trigger words
           all_dicts is the dictionary containing all of the pickup lines
    Output: dictionary for new catgeory of pickup lines
    This function searches through all of the pickup lines in the database, and creates a new dictionary
    in all_dicts containing the pickup lines for a new category of words
    """
    new_category = {}
    for word in trigger_words: #for each trigger word
        for category in all_dicts: #for every category we have
            for pickupline in all_dicts[category]: # for every pickup line in that category
                formatted_line = standardize_format(pickupline) #standardize the format of the pickup line
                line_word_list = formatted_line.split() #split up the pickup line into words
                for line_word in line_word_list: #for every word in that list
                    if word == line_word: #if it matches the trigger word
                        new_category[pickupline] = 0

    all_dicts[key_word] = new_category
    return new_category, all_dicts

#setting up datamuse api
api = datamuse.Datamuse()

#pickling in the database of pickup lines
pickle_files = find_pickled_files()
all_dicts = get_dicts(pickle_files)

#taking a keyword and searching for relevant categories
key_word = standardize_format(input("Beep boop! Give me one key word and I'll give you pickup lines! Beep boop! \n"))
related_words = get_related_words(key_word)
category_dict = find_category(related_words)

#if no categories exist, the script makes its own and returns it
if category_dict == False:
    print("Hmm... I don't think anyone's asked for that key word before! Let me search around in my bigger database.")
    trigger_words = get_trigger_words(related_words)
    new_category, all_dicts = create_category(key_word,trigger_words,all_dicts)
    print(new_category)

#if a category does exist, the script returns the relevant category
else:
    print(category_dict)
