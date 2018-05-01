from pickle import dump, load
import sys
import random

def load_cache(file):
    cache = load( open( file, "rb" ) )
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
    dictionary = load_cache("_names_PUL_cache")
    no_lines = load_cache("_names_no_lines_cache")
    need_lines = load_cache("_names_need_lines_cache")
    bad_lines = load_cache("_names_bad_lines_cache")
    match_status_dictionary = load_cache('_names_match_status_dictionary_cache')
    PUL_contributors = load_cache('_names_PUL_contributors_cache')
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
    pickle_cache(dictionary, "_names_PUL_cache")
    pickle_cache(no_lines, "_names_no_lines_cache")
    pickle_cache(need_lines, "names_need_lines_cache")
    pickle_cache(bad_lines, "_names_bad_lines_cache")
    pickle_cache(PUL_contributors, '_names_PUL_contributors_cache')
    pickle_cache(match_status_dictionary, '_names_match_status_dictionary_cache')

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


def grab_random_name_from_no_lines_or_need_lines():
    try:
        if no_lines:
            return random.choice(no_lines)
        else:
            if need_lines:
                return random.choice(need_lines)
    except:
        return 'No names need training.'


if __name__ == "__main__":
    """
    Takes inputs: No input.
    Output: Random 'name' that needs PULs or 'No names need training.'

    """
    load_all()
    result = grab_random_name_from_no_lines_or_need_lines()
    print('\nThe website should recieve this output: ', result, '\n')
