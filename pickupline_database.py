#importing libraries
import urllib.request
from bs4 import BeautifulSoup
import os
import sys
import pickle
import string

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

def get_webpage(link,filename):
    """This function will take a link and serialize its html code in a file called filename"""
    # exists = os.path.isfile(filename) #True if file exists, False if file doesn't exist
    #
    # if exists == False:
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    opener = AppURLopener()
    page = opener.open(link)
    soup = BeautifulSoup(page,'html.parser')
    current_html_str = str(soup.prettify())

    if os.path.isfile(filename) == True:
        old_html_str = load_html_str(filename)
        new_html_str = current_html_str+old_html_str
    else:
        new_html_str = current_html_str

    pickle_out = open(filename,"wb")
    pickle.dump(new_html_str,pickle_out)
    pickle_out.close()

def load_html_str(filename):
    """This will take serialized html code from a file called filename and load it into python as page"""
    pickle_in = open(filename,"rb")
    html_str = pickle.load(pickle_in)
    pickle_in.close()

    return html_str

def create_pickup_list(html_str):
    """This function goes through a given string of html code and returns a list of pickup lines from that code"""
    pickup_len = len('<span class="loop-entry-line">')
    c=0
    pickup_list = []
    while c < len(html_str):
        if html_str[c:c+pickup_len] == '<span class="loop-entry-line">':
            pickup_line = ""
            finished = False
            count = 11
            while finished == False:
                pickup_line += html_str[c+pickup_len+count]
                count += 1
                if html_str[c+pickup_len+count] == "<":
                    pickup_list.append(pickup_line[0:-11])
                    finished = True
        c+=1

    return pickup_list

def get_website(link,filename):
    exists = os.path.isfile(filename) #True if file exists, False if file doesn't exist

    if exists == False:
        get_webpage(link,filename)

        for i in range(69):
            new_link = link + "page/" + str(i+2) + "/"
            print(new_link)
            get_webpage(new_link,filename)

"""
This should be able to go through all the pages of pickuplines.net and store all of the html code in a single file
it should initially create the file and store all of the first page code into it
then it should load the information from that file and modify it
then it should store it back into the file, overwrite what was already there
"""
get_website('http://pickup-lines.net/','pickup-lines.p')
html_str = load_html_str("pickup-lines.p")
pickup_list_ever = create_pickup_list(html_str)
pickup_list_in_class = get_word_list('/home/libby/TindEEEEr/InClassSurveyPickuplines.txt')
pickup_list_carpe = get_word_list('/home/libby/TindEEEEr/CarpeSurveyPickuplines.txt')
pickup_line_emma = get_word_list('/home/libby/TindEEEEr/emma_lines.txt')
all_the_pickup_lines = pickup_list_ever + pickup_list_carpe + pickup_list_in_class + pickup_line_emma

def standardize_format(list):
    lines1 = []
    for pul in list:
        pul = pul.strip(string.whitespace)
        for i in range(32):
            pul = pul.replace(string.punctuation[i],'')
        pul = pul.replace('','')
        pul = pul.lower()
        lines1.append(pul)
    stringlines = ' '.join(lines1)
    return lines1
new = standardize_format(all_the_pickup_lines)

def eliminate_repeats(list):
    n = []
    for pul in list:
        if pul not in n:
            n.append(pul)
    return n
no_duplicates = eliminate_repeats(new)
print(len(new))
print(len(no_duplicates))
