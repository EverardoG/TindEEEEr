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
    dictionary = {}
    no_lines = []
    need_lines = []
    bad_lines = {}

def see_all():
    print("Dictionary: ", len(dictionary))
    print("No_lines: ", len(no_lines))
    print("Need_lines: ", len(need_lines))
    print("Bad_lines: ", len(bad_lines))
    print(dictionary)
    print(no_lines)
    print(need_lines)
    print(bad_lines)


def load_all():
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    global contributed_PULs_WEB
    dictionary = load_cache("_names_PUL_cache")
    no_lines = load_cache("_names_no_lines_cache")
    need_lines = load_cache("_names_need_lines_cache")
    bad_lines = load_cache("_names_bad_lines_cache")
    match_status_dictionary = load_cache('_names_match_status_dictionary_cache')
    contributed_PULs_WEB = load_cache('_names_contributed_PULs_WEB')
    print("Dictionary: ", len(dictionary))
    print("No_lines: ", len(no_lines))
    print("Need_lines: ", len(need_lines))
    print("Bad_lines: ", len(bad_lines))
    print('contributed_PULs_WEB: ', len(contributed_PULs_WEB))

def pickle_all():
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    pickle_cache(dictionary, "_names_PUL_cache")
    pickle_cache(no_lines, "_names_no_lines_cache")
    pickle_cache(need_lines, "names_need_lines_cache")
    pickle_cache(bad_lines, "_names_bad_lines_cache")
    pickle_cache(contributed_PULs_WEB, '_names_contributed_PULs_WEB')


def pickle_all_by_date(date):
    date = str(date)
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    pickle_cache(dictionary, "names_PUL_cache"+date)
    pickle_cache(no_lines, "names_no_lines_cache"+date)
    pickle_cache(need_lines, "names_need_lines_cache"+date)
    pickle_cache(bad_lines, "names_bad_lines_cache"+date)
    pickle_cache(contributed_PULs_WEB, '_names_contributed_PULs_WEB'+date)

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

def is_PUL(PUL):
    if len(PUL)< 10:
        return False
    else:
        return True

def add_PUL_to_database(name, PUL):
    name = name.lower()
    if not name in dictionary:
        dictionary[name] = {PUL:15}
        print("Added "+ '"' + PUL + '"' + "to "+name+" pick-up lines.")
        add_to_contributed_PULs_WEB(name, PUL)
        print("Added line to contributed_PULs_WEB.")
    else:
        if not PUL in dictionary[name]:
            dictionary[name][PUL] = 15
            print("Added "+ '"' + PUL + '"' + "to "+name+" pick-up lines.")
            add_to_contributed_PULs_WEB(name, PUL)
            print("Added line to contributed_PULs_WEB.")
        else:
            print("Line aleady exists in dictionary.")
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
        print("Failed to remove '"+name.title()+"' from need/no_lines.")

def add_to_contributed_PULs_WEB(name, PUL): #CHECK THIS
    if not name in contributed_PULs_WEB:
        contributed_PULs_WEB[name]=[PUL]
    else:
        if PUL not in contributed_PULs_WEB[name]:
            contributed_PULs_WEB[name].append(PUL)

def adding_train_PUL(name, PUL):
    if is_PUL(PUL):
        add_PUL_to_database(name, PUL)
    else:
        print("Not a valid pick-up line.")

def main(name, PUL):
    name = name.lower()
    load_all()
    adding_train_PUL(name, PUL)
    pickle_all()
    print("\nCurrent lines for " + name + ": ", dictionary[name])
    print("\ncontributed_PULs_WEB: ", contributed_PULs_WEB)



if __name__ == "__main__":
    """
    Takes inputs: 'name', 'given PUL'
    Output: None. Modifies database.

    """
    main(sys.argv[1], sys.argv[2])
