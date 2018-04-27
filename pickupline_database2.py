from processing_pickup_lines2 import *
from pickupline_database import *

def find_text_files():
    directory = os.listdir()
    textfiles = []
    for filename in directory:
        if filename[-3:] == 'txt':
            textfiles.append(filename)
    return textfiles

def get_lists(textfiles):
    LIST = []
    for textfile in textfiles:
        name = str(textfile)[:-4]
        list = read_text_file(textfile)
        LIST.append((name, list))
    return LIST

def deal_with_all_the_shit(list):
    BIG_LIST2 = []
    for tuple in list:
        name = tuple[0]
        # print(name + '/n')
        lines = remove_copies(tuple[1])
        BIG_LIST2.append((name, lines))
    return BIG_LIST2

def pickle_shit(big_list):
    for tuple in big_list:
        # print(tuple[1])
        pickup_pickle = open(tuple[0],'wb')
        pickle.dump(tuple[1], pickup_pickle)

def text_to_pickle():
    step1 = find_text_files()
    step2 = get_lists(step1)
    step3 = deal_with_all_the_shit(step2)
    pickle_shit(step3)

text_to_pickle()
