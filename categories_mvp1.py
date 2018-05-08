#Importing libraries and functions
from processing_pickup_lines2 import *
from datamuse import datamuse
import itertools
import string
import copy
import random
#
# global all_dicts
# all_dicts = initialize_all_dicts()

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

def get_related_words(key_word,n = 10):
    """Input: keyword, n
       Output: list containing keyword and up to n related words (10 by default)"""
    api = datamuse.Datamuse()
    related_words = []
    related_words.append(key_word)
    related_words += (get_list(api.words(ml = key_word, max = n),key_word))
    return related_words

def get_trigger_words(related_words,n = 10):
    """Input: list of related_words, n
       Output: list containing all of the related words, as well as n trigger words per related words
       """
    api = datamuse.Datamuse()
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
    all_dicts = initialize_all_dicts()
    for related_word in related_words: #for every related word
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

def serialize_dicts(all_dicts):
    """
    Input: all_dicts, the massive dict containing all of the category dicts
    Output: None
    This function serializes all of the category dictionaries into pickle files named appropriately"""
    for category_name in all_dicts.keys():
        pickle_out = open(category_name+'.pickle','wb')
        pickle.dump(all_dicts[category_name],pickle_out)

def adjust_weight(user_input, category_name ,category_dict, pickup_line, all_dicts):
    """
    Input: yes, no, or wrong as user_input, a key-value pair as pickup_line, the category dictionary the line came from as category_dict, the category name as category_name
    Output: None
    This function adjusts the value associated with a pickup line positively if good, nuetrally if okay negatively if bad, and very negatively if wrong"""
    if user_input not in ["good","bad","okay","wrong"]:
        return category_dict, all_dicts
    elif user_input == "good":
        adjust = 2
    elif user_input == "bad":
        adjust = -2
    elif user_input == "okay":
        adjust = 1
    elif user_input == "wrong":
        adjust = -4
    category_dict[pickup_line] += adjust
    all_dicts[category_name][pickup_line] += adjust
    return category_dict, all_dicts


def find_highest_weight(category_dict):
    """
    Input: a dictionary of a given category, category_dict
    Output: pickupline with the highest weight
    This function finds the pickup line with the highest associated
    value in a category dictionary, and returns it."""
    pul_val = max(category_dict.values())
    pul = list(category_dict.keys())[list(category_dict.values()).index(pul_val)]
    return pul

def find_top_weights(category_dict,num_lines):
    """
    Input: a dictionary for given category, category_dict, number of lines you want, num_lines
    Output: a list of top num_lines pickup lines according to their weights
    This function takes in category dictionary and a number of lines you want, and returns the top specified number of lines
    """
    pul_list = []
    temp_dict = copy.deepcopy(category_dict)
    if num_lines == 0:
        return pul_list, temp_dict
    for i in range(num_lines):
        pul = find_highest_weight(temp_dict)
        pul_list.append(pul)
        del temp_dict[pul]
    return pul_list, temp_dict

def find_random(temp_dict,num_lines):
    """
    Input: a dictionary for given category, category_dict, number of lines you want, num_lines
    Output: a list of random num_lines pickup lines
    This function takes in category dictionary and a number of lines you want, and returns the number of specified random lines
    """
    pul_list = []
    if num_lines == 0:
        return pul_list, temp_dict
    for i in range(num_lines):
        pul = random.choice(list(temp_dict.keys()))
        pul_list.append(pul)
        del temp_dict[pul]
    return pul_list, temp_dict

def check_num_lines(category_dict,num_lines_weight,num_lines_random):
    """
    Input: a dictionary for given category, category_dict, the set number of lines for a given weight, num_lines_weight and a number of random lines, num_lines_random
    Output: num_lines_weight and num_lines_random
    This function checks whether or not the category of concern contains enough pick up lines to return the number requested by num_lines_random and num_lines_weight and
    if there are not enough lines, it adjusts num_lines_weight and num_lines_random accordingly
    """
    d = len(list(category_dict.keys())) - (num_lines_random + num_lines_weight)
    if d >= 0:
        return num_lines_random, num_lines_weight
    else:
        num_lines_random += d
        if num_lines_random < 0:
            num_lines_weight += num_lines_random
            num_lines_random = 0
        return num_lines_random, num_lines_weight

def initialize_all_dicts():
    api = datamuse.Datamuse()
    pickle_files = find_pickled_files()
    all_dicts = get_dicts(pickle_files)
    return all_dicts

def give_pickup_lines(key_word,num_lines_weight = 2,num_lines_random = 1):
    """
    Inputs:
    key_word - the category for which you want related pickuplines
    num_lines_weight - how many relevant pickup lines you want based on weights
    num_lines_random - how many relevant pickup lines you want that are random
    """
    api = datamuse.Datamuse()
    related_words = get_related_words(key_word)
    category_dict = find_category(related_words)

    if category_dict == False:
        trigger_words = get_trigger_words(related_words)
        new_category, all_dicts = create_category(key_word,trigger_words,all_dicts)
        num_lines_random, num_lines_weight = check_num_lines(new_category,num_lines_weight,num_lines_random)
        pul_list, temp_dict = find_top_weights(new_category,num_lines_weight)
        pul_list1, temp_dict = find_random(temp_dict,num_lines_random)
        pul_list += pul_list1
    else:
        num_lines_random, num_lines_weight = check_num_lines(category_dict,num_lines_weight,num_lines_random)
        pul_list, temp_dict = find_top_weights(category_dict,num_lines_weight)
        pul_list1, temp_dict = find_random(temp_dict,num_lines_random)
        pul_list += pul_list1
    return pul_list, category_dict

def adjust_weight_web(adjust, key_word ,category_dict, pickup_line, all_dicts):
    """
    Input: yes, no, or wrong as user_input, a key-value pair as pickup_line, the category dictionary the line came from as category_dict, the category name as category_name
    Output: None
    This function adjusts the value associated with a pickup line positively if good, nuetrally if okay negatively if bad, and very negatively if wrong"""

    category_dict[pickup_line] += adjust
    all_dicts[key_word][pickup_line] += adjust
    return category_dict, all_dicts

def main(key_word):
    all_dicts = initialize_all_dicts()
    list_and_cat = give_pickup_lines(key_word)
    return list_and_cat
#
# adjust =1
# key_word = "coffee"
#
# all_dicts = initialize_all_dicts()
# list_and_cat = give_pickup_lines(key_word)
# pul_list = list_and_cat[0]
# cat_dict = list_and_cat[1]
# dicts = adjust_weight_web(adjust, key_word, cat_dict, pul_list[0], all_dicts)

######################################################################
# Uncommment everything below to run this locally

# #setting up datamuse api
#
# api = datamuse.Datamuse()
#
# #pickling in the database of pickup lines
# pickle_files = find_pickled_files()
# all_dicts = get_dicts(pickle_files)
#
# # print(all_dicts)
#
# while 1:
#     num_lines_weight = 2
#     num_lines_random = 1
#     #taking a keyword and searching for relevant categories
#     key_word = standardize_format(input("Beep boop! Give me one key word and I'll give you pickup lines! Beep boop! \n"))
#     related_words = get_related_words(key_word)
#     category_dict = find_category(related_words)
#
#
#     #if no categories exist, the script makes its own and returns it
#     if category_dict == False:
#         print("Hmm... I don't think anyone's asked for that key word before! Let me search around in my bigger database.")
#         trigger_words = get_trigger_words(related_words)
#         new_category, all_dicts = create_category(key_word,trigger_words,all_dicts)
#
#         num_lines_random, num_lines_weight = check_num_lines(new_category,num_lines_weight,num_lines_random)
#         if num_lines_random + num_lines_weight == 0:
#             print("Whoops, didn't find any relevant pickup lines for that. Feel free to try other words though!")
#
#         pul_list, temp_dict = find_top_weights(new_category,num_lines_weight)
#         for pul in pul_list:
#             print("\n"+ pul +"\n")
#             user_input = input("Give me feedback on the pickup line! \n Type good if it was good \n Type okay if it was okay \n Type bad if it was bad \n Type wrong if it was irrelavent \n")
#             new_category, all_dicts = adjust_weight(user_input, key_word, new_category, pul, all_dicts)
#             serialize_dicts(all_dicts)
#         pul_list, temp_dict = find_random(temp_dict,num_lines_random)
#         for pul in pul_list:
#             print("\n"+ pul+"\n")
#             user_input = input("Give me feedback on the pickup line! \n Type good if it was good \n Type okay if it was okay \n Type bad if it was bad \n Type wrong if it was irrelavent \n")
#             new_category, all_dicts = adjust_weight(user_input, key_word, new_category, pul, all_dicts)
#             serialize_dicts(all_dicts)
#
#     #if a category does exist, the script returns the relevant category
#     else:
#         num_lines_random, num_lines_weight = check_num_lines(category_dict,num_lines_weight,num_lines_random)
#         if num_lines_random + num_lines_weight == 0:
#             print("Whoops, didn't find any relevant pickup lines for that. Feel free to try other words though!")
#
#         pul_list, temp_dict = find_top_weights(category_dict,num_lines_weight)
#         for pul in pul_list:
#             print("\n"+ pul +"\n")
#             user_input = input("Give me feedback on the pickup line! \n Type good if it was good \n Type okay if it was okay \n Type bad if it was bad \n Type wrong if it was irrelavent \n")
#             category_dict, all_dicts = adjust_weight(user_input, key_word, category_dict, pul, all_dicts)
#             serialize_dicts(all_dicts)
#         pul_list, temp_dict = find_random(temp_dict,num_lines_random)
#         for pul in pul_list:
#             print("\n"+ pul +"\n")
#             user_input = input("Give me feedback on the pickup line! \n Type good if it was good \n Type okay if it was okay \n Type bad if it was bad \n Type wrong if it was irrelavent \n")
#             category_dict, all_dicts = adjust_weight(user_input, key_word, category_dict, pul, all_dicts)
#             serialize_dicts(all_dicts)
