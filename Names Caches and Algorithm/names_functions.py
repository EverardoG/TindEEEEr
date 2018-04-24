from os.path import exists
import sys
from pickle import dump, load
import pickle
from datamuse import datamuse #may need to pip3 install python-datamuse
api = datamuse.Datamuse()
import praw #may need to pip install praw
import requests.auth
import string
reddit = praw.Reddit(client_id='fAkqHqn2XyBt3g',
                     client_secret="B1Rv2IY6KfA3PusqSeaFAu8brIw",
                     user_agent='USERAGENT')
import enchant #may need to pip install pyenchant
import itertools
import numpy

def load_cache(file):
    cache = pickle.load( open( file, "rb" ) )
    return cache

def pickle_cache(variable, file_name):
    dump(variable, open(file_name, 'wb'))

def reset_all():
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    global match_status_dictionary
    global PUL_contributors
    dictionary = {}
    no_lines = []
    need_lines = []
    bad_lines = {}
    match_status_dictionary = {}
    PUL_contributors = {}

def see_all():
    print("Dictionary: ", len(dictionary))
    print("No_lines: ", len(no_lines))
    print("Need_lines: ", len(need_lines))
    print("Bad_lines: ", len(bad_lines))
    print('Match_status_dictionary: ', len(match_status_dictionary))
    print("PUL_contributors: ", len(PUL_contributors))
    print(dictionary)
    print(no_lines)
    print(need_lines)
    print(bad_lines)
    print(match_status_dictionary)
    print(PUL_contributors)

def load_all():
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    global match_status_dictionary
    global PUL_contributors    
    dictionary = load_cache("names_PUL_cache")
    no_lines = load_cache("names_no_lines_cache")
    need_lines = load_cache("names_need_lines_cache")
    bad_lines = load_cache("names_bad_lines_cache")
    match_status_dictionary = load_cache('names_match_status_dictionary_cache')
    PUL_contributors = load_cache('names_PUL_contributors_cache')
    print("Dictionary: ", len(dictionary))
    print("No_lines: ", len(no_lines))
    print("Need_lines: ", len(need_lines))
    print("Bad_lines: ", len(bad_lines))
    print('Match_status_dictionary: ', len(match_status_dictionary))
    print("PUL_contributors: ", len(PUL_contributors))

def pickle_all():
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    global PUL_contributors
    global match_status_dictionary
    pickle_cache(dictionary, "names_PUL_cache")
    pickle_cache(no_lines, "names_no_lines_cache")
    pickle_cache(need_lines, "names_need_lines_cache")
    pickle_cache(bad_lines, "names_bad_lines_cache")
    pickle_cache(PUL_contributors, 'names_PUL_contributors_cache')
    pickle_cache(match_status_dictionary, 'names_match_status_dictionary_cache')

def pickle_all_by_date(date):
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    global PUL_contributors
    global match_status_dictionary
    pickle_cache(dictionary, "names_PUL_cache"+date)
    pickle_cache(no_lines, "names_no_lines_cache"+date)
    pickle_cache(need_lines, "names_need_lines_cache"+date)
    pickle_cache(bad_lines, "names_bad_lines_cache"+date)
    pickle_cache(PUL_contributors, 'names_PUL_contributors_cache'+date)
    pickle_cache(match_status_dictionary, 'names_match_status_dictionary_cache'+date)

def recalculate_nolines_and_needlines(dictionary):
    global no_lines
    global need_lines
    no_lines = []
    need_lines = []
    for name, PULS in dictionary.items():
        if len(dictionary[name]) <= 3:
            need_lines.append(name)
        if len(dictionary[name]) <= 0:
            no_lines.append(name)

def create_list_of_near_names(name):
    api = datamuse.Datamuse()
    list_of_dictionaries = api.words(sl = name, max = 10)
    list_of_names = []
    for i in list_of_dictionaries:
        if i['score'] == 100:
            list_of_names.append(i['word'])
    if name not in list_of_names:
        list_of_names.append(name)
    if len(list_of_names) > 10:
        list_of_names = list_of_names[:9]
    return list_of_names

def return_reddit_PULine(name):
    """Function that takes name and outputs comments from r/pickuplines that have the name in the title
    and the name in the comment in a list. """
    pickuplines = []
    name = name.lower()
    for submission in reddit.subreddit('pickuplines').top(limit=20000):
        if " "+name in submission.title.lower():
            submission.comments.replace_more(limit=0)
            for top_level_comment in submission.comments:
                if name.lower() in top_level_comment.body.lower():
                    pickuplines.append(top_level_comment.body)

    for submission in reddit.subreddit('pickuplines').hot(limit=5000):
        if " "+name in submission.title.lower():
            submission.comments.replace_more(limit=0)
            for top_level_comment in submission.comments:
                if name.lower() in top_level_comment.body.lower():
                    pickuplines.append(top_level_comment.body)
    if not pickuplines:
        for submission in reddit.subreddit('pickuplines').new(limit=10000):
            if " "+name in submission.title.lower():
                submission.comments.replace_more(limit=0)
                for top_level_comment in submission.comments:
                    if name.lower() in top_level_comment.body.lower():
                        pickuplines.append(top_level_comment.body)

    if pickuplines:
        print(str(len(pickuplines))+" pick-up lines for "+ name.title()+ " found on Reddit.")
        return pickuplines
    else:
        print("No pickup lines for "+ name+ " found on Reddit.")
        return pickuplines

def new_reddit_PULines(name):
    """Function that takes name and outputs comments from r/pickuplines that have the name in the title
    and the name in the comment in a list. """
    pickuplines = []
    name = name.lower()
    for submission in reddit.subreddit('pickuplines').new(limit=10000):
        if " "+name in submission.title.lower():
            submission.comments.replace_more(limit=0)
            for top_level_comment in submission.comments:
                if name.lower() in top_level_comment.body.lower():
                    pickuplines.append(top_level_comment.body)
    if pickuplines:
        print(str(len(pickuplines))+" pick-up lines for "+ name.title()+ " found on Reddit.")
        return pickuplines
    else:
        print("No new pickup lines for "+name+ " found on Reddit.")
        return pickuplines

def return_palindrome_PULine(name):
    name = name.lower()
    i = 0
    j = len(name)-1
    while i<j:
        if name[i] != name[j]:
            print(name.title() + " is not a palindrome.")
            return []
        i = i+1
        j = j-1
    print(name.title() + " is a palindrome.")
    return [name.title() + " - your name is a palindrome, I like it. I'd do you forwards and backwards"]

def return_anagram_PULine_D(name):
    named = name.lower()+'d'
    named = named.strip(' ')
    english_dictionary = enchant.Dict("en_US")
    spanish_dictionary = enchant.Dict("es_ES")

    list_of_all_anagrams = ["".join(perm) for perm in itertools.permutations(named)]

    list_of_real_anagrams = []
    pickuplines = []
    spanish = False
    for i in list_of_all_anagrams:
        if english_dictionary.check(i):
            list_of_real_anagrams.append(i)

    if not list_of_real_anagrams:
        spanish = True
        for i in list_of_all_anagrams:
            if spanish_dictionary.check(i):
                list_of_real_anagrams.append(i)

    if not spanish:
        for i in list_of_real_anagrams:
            pickuplines.append(name.title() + ", if you add a D to your name, it's an anagram for the word "
                       + i
                       + ". So I guess the question is - do you want the D?")
            list_of_real_anagrams.remove(i)
    else:
        for i in list_of_real_anagrams:
            pickuplines.append(name.title() + ", if you add a D to your name, it's an anagram for the Spanish word "
                       + i
                       + ". So I guess the question is - do you want the D?")
            list_of_real_anagrams.remove(i)
    if pickuplines:
        print(name.title()+" has at least one anagram.")
    return pickuplines

def return_anagram_PULine_V(name):
    named = name.lower()+'v'
    named = named.strip(' ')
    english_dictionary = enchant.Dict("en_US")
    spanish_dictionary = enchant.Dict("es_ES")

    list_of_all_anagrams = ["".join(perm) for perm in itertools.permutations(named)]

    list_of_real_anagrams = []
    pickuplines = []
    spanish = False
    for i in list_of_all_anagrams:
        if english_dictionary.check(i):
            list_of_real_anagrams.append(i)

    if not list_of_real_anagrams:
        spanish = True
        for i in list_of_all_anagrams:
            if spanish_dictionary.check(i):
                list_of_real_anagrams.append(i)

    if not spanish:
        for i in list_of_real_anagrams:
            pickuplines.append(name.title() + ", if you add a V to your name, it's an anagram for the word "
                       + i
                       + ". So I guess the question is - do you want the V?")
            list_of_real_anagrams.remove(i)
    else:
        for i in list_of_real_anagrams:
            pickuplines.append(name.title() + ", if you add a V to your name, it's an anagram for the Spanish word "
                       + i
                       + ". So I guess the question is - do you want the V?")
            list_of_real_anagrams.remove(i)

    if pickuplines:
        print(name.title()+" has at least one anagram.")

    return pickuplines

def gather_all_PU_lines_for_a_name(name):
    names_list = create_list_of_near_names(name)
    PULines = []
    try:
        for each_name in names_list:
            PULines+=return_reddit_PULine(each_name)
        try:
            PULines+=return_palindrome_PULine(name)
            PULines+=return_anagram_PULine_D(name)
            PULines+=return_anagram_PULine_V(name)
        except:
            print("Failed palindrome/anagram line generation.")
            pass
    except:
        print("Failed Reddit Scrape.")
        pass
    print("Coming back from the interwebs...")
    return PULines

def add_PUL_to_database(name, PUL):
    """Return updated dictionary"""
    if not name in dictionary:
        dictionary[name] = {PUL:15}
    else:
        if not PUL in dictionary[name]:
            dictionary[name][PUL] = 15
    try:
        if name in need_lines:
            if len(dictionary[name]) > 3:
                print("Removing "+name.title()+" from need_lines list.")
                need_lines.remove(name)
        if name in no_lines:
            if len(dictionary[name]) > 0:
                print("Removing "+name.title()+" from no_lines list.")
                no_lines.remove(name)
    except:
        print("Failed to remove '"+PUL+"' from "+ name.title()+" pick-up lines.")

def remove_PUL_from_database(name, PUL):
    try:
        del dictionary[name][PUL]
        print('Deleted '+name.title()+' pick-up line: ', PUL)
    except:
        print('Failed to delete '+name.title()+' pick-up line: ', PUL)
    try:
        if not name in need_lines:
            if len(dictionary[name]) <=3:
                print("Adding "+name.title()+" to need_lines list.")
                need_lines.append(name)
        if not name in no_lines:
            if len(dictionary[name]) <= 0:
                print("Adding "+name.title()+" to no_lines list.")
                no_lines.append(name)
    except:
        print("Failed to remove '"+PUL+"' from "+ name.title()+" pick-up lines.")

def pick_PULs_from_database(dictionary_of_PULs):
    if len(dictionary_of_PULs)<=3:
        return list(dictionary_of_PULs.keys())
    else:
        lines = list(dictionary_of_PULs.keys())
        weights = []
        sum_of_weights = sum(dictionary_of_PULs.values())
        for i in dictionary_of_PULs.values():
            weights.append(i/sum_of_weights)
        chosen_PUL = list(numpy.random.choice(lines,size=3,replace=False, p=weights))
        return chosen_PUL


def receiving_name_request(name):
    """Returns list of 0-3 pickup-lines. Adds new lines to database"""
    name = name.lower()
    name.strip(" ")
    if name in no_lines:
        print(name.title()+" is in no_lines list.")
        return 'Give General.'
    else:
        if name in dictionary:
            print("Giving pick-up lines from database for "+name+".")
            return pick_PULs_from_database(dictionary[name])
        else:
            print(name.title()+" not in database. Searching online...")
            dictionary[name]={}
            names_PUL_from_internet = gather_all_PU_lines_for_a_name(name)
            if not names_PUL_from_internet:
                print("No lines found online for "+name.title()+". Adding to no_lines and need_lines list.")
                if not name in no_lines:
                    no_lines.append(name)
                if not name in need_lines:
                    need_lines.append(name)
                return 'Give General.'
            else:
                print("Found "+str(len(names_PUL_from_internet))+" pick-up lines online for "+name.title()+
                      ". Adding to database now.")
                for PUL in names_PUL_from_internet:
                    add_PUL_to_database(name, PUL)
                if len(dictionary[name]) <=3:#needs to be here
                    print("3 or less pick-up lines found for "+name.title()+
                         ". Adding it to the need_lines list.")
                    if not name in need_lines:
                        need_lines.append(name)
                return pick_PULs_from_database(dictionary[name])

def update_name_from_internet(name):
    if name == '' or name == " ":
        return 'No Input.'
    name = name.lower()
    name.strip(" ")
    if not name in dictionary:
        receiving_name_request(name)
    else:
        print(name.title()+" is already in the database. It currently has "+str(len(dictionary[name]))+
              " pick-up lines. \n Scraping reddit for new lines...")
        names_PUL_from_internet = new_reddit_PULines(name)
        if names_PUL_from_internet:
            if not name in bad_lines:
                for PUL in names_PUL_from_internet:
                    add_PUL_to_database(name, PUL)
            else:
                for PUL in names_PUL_from_internet:
                    if PUL in bad_lines[name]:
                        names_PUL_from_internet.remove(PUL)
                    else:
                        add_PUL_to_database(name, PUL)
            if names_PUL_from_internet:
                print("Adding ", names_PUL_from_internet, " to "+name+" pick-up lines. REPEATS WILL BE REMOVED.")
            else:
                print("No new pick-up lines found online for "+ name +".")

        else:
            print("No new pick-up lines found online for "+ name +".")

def receiving_weight_modifiers(name, PUL, value_modifier):
    try:
        dictionary[name][PUL] += value_modifier
        if dictionary[name][PUL] <= 0:
            if name in bad_lines:
                if not PUL in bad_lines[name]:
                    bad_lines[name].append(PUL)
            else:
                bad_lines[name] = [PUL]
            try:
                del dictionary[name][PUL]
            except:
                print(PUL+" was already deleted.")
            if len(dictionary[name])<= 3:
                if not name in need_lines:
                    need_lines.append(name)
            if len(dictionary[name])<= 0:
                if not name in no_lines:
                    no_lines.append(name)
    except:
        print("Could not find this pick-up line and modify its weight.")


if __name__ == "__main__":
    load_all()
    print(receiving_name_request(sys.argv[1]))
    print(dictionary)
