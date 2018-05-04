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
    name = name.replace(" ", "")
    name = name.replace(string.punctuation, "")
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
    name = name.replace(" ", "")
    name = name.replace(string.punctuation, "")
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
