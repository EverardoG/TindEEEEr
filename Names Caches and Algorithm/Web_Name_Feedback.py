from pickle import dump, load
import sys

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

def receiving_weight_modifiers(name, PUL, value_modifier):
    name = name.lower()
    try:
        dictionary[name][PUL] += int(value_modifier)
        print('The line '+'"'+PUL+'"'+" for "+name+" had its score modified by "+str(value_modifier)+".")
        if dictionary[name][PUL] <= 0:
            print('The line '+'"'+PUL+'"'+" for "+name+" had its score fall under zero.")
            if name in bad_lines:
                if not PUL in bad_lines[name]:
                    bad_lines[name].append(PUL)
                    print('Added lines to bad_lines.')
                else:
                    print('Line already in bad_lines.')
            else:
                bad_lines[name] = [PUL]
                print('Added lines to bad_lines.')
            try:
                del dictionary[name][PUL]
                print('Deleted line from dictionary.')
            except:
                print("Failed to delete line from dictionary. Line may have already been deleted.")
            if len(dictionary[name])<= 3:
                if not name in need_lines:
                    need_lines.append(name)
                    print("Name has less than or equal to 3 lines. Adding to need_lines.")
            if len(dictionary[name])<= 0:
                if not name in no_lines:
                    no_lines.append(name)
                    print("Name has no lines. Adding to need_lines.")
    except:
        print("Could not find this pick-up line and modify its weight.")
    try:
        print('The line '+'"'+PUL+'"'+" for "+name+" has a score of "+str(dictionary[name][PUL])+".")
    except:
        pass

def main(name, PUL, value_modifier):
    load_all()
    receiving_weight_modifiers(name, PUL, value_modifier)
    pickle_all()


if __name__ == "__main__":
    """
    Takes inputs: 'name', 'PUL', int(value_modifier)
    Output: No output. Modifies database.

    """
    main(sys.argv[1], sys.argv[2], sys.argv[3])
