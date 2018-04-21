#importing libraries
import urllib.request
from bs4 import BeautifulSoup
import os
import pickle
import string
from collections import OrderedDict

### Functions to read in pickup lines
def read_text_file(file_path):
    """Reads in whatever text file is passed in and return a list
    of lines to be manipulated in future functionsself.
    Args
    file_path: the full file path of the text file to be read_text_file
    Return values
    lines1: the text file as a list of strings with the whitespace removed and
    each string as a separate pickup line"""
    text = open(file_path,'r')
    lines = list(text)
    lines1 = []
    for line in lines:
        line = line.strip(string.whitespace)
        line = line.replace('','')
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
    """
    This should be able to go through all the pages of pickuplines.net and store all of the html code in a single file
    it should initially create the file and store all of the first page code into it
    then it should load the information from that file and modify it
    then it should store it back into the file, overwrite what was already there
    """
    exists = os.path.isfile(filename) #True if file exists, False if file doesn't exist

    if exists == False:
        get_webpage(link,filename)

        for i in range(69):
            new_link = link + "page/" + str(i+2) + "/"
            print(new_link)
            get_webpage(new_link,filename)

### Uses functions defined above to import all pickup line files and combine them
### into one list

get_website('http://pickup-lines.net/','pickup-lines.p')
html_str = load_html_str("pickup-lines.p")
ever = create_pickup_list(html_str)
in_class = read_text_file('/home/libby/TindEEEEr/InClassSurveyPickuplines.txt')
carpe = read_text_file('/home/libby/TindEEEEr/CarpeSurveyPickuplines.txt')
emma = read_text_file('/home/libby/TindEEEEr/emma_lines.txt')
more = read_text_file('/home/libby/TindEEEEr/more.txt')
random = read_text_file('/home/libby/TindEEEEr/random.txt')
all_the_pickup_lines = ever + carpe + in_class + emma + more + random

olin = read_text_file('/home/libby/TindEEEEr/olin.txt')
star_wars = read_text_file('/home/libby/TindEEEEr/StarWars.txt')
music = read_text_file('/home/libby/TindEEEEr/Music.txt')
HIMYM = read_text_file('/home/libby/TindEEEEr/HIMYM.txt')
GOT = read_text_file('/home/libby/TindEEEEr/GOT.txt')
Disney = read_text_file('/home/libby/TindEEEEr/Disney.txt')
biochem = read_text_file('/home/libby/TindEEEEr/Biochem.txt')
accountant = read_text_file('/home/libby/TindEEEEr/accountant.txt')
animal = read_text_file('/home/libby/TindEEEEr/animal.txt')
art = read_text_file('/home/libby/TindEEEEr/art.txt')
baseball = read_text_file('/home/libby/TindEEEEr/baseball.txt')
beach = read_text_file('/home/libby/TindEEEEr/beach.txt')
basketball = read_text_file('/home/libby/TindEEEEr/basketball.txt')
books = read_text_file('/home/libby/TindEEEEr/books.txt')
car = read_text_file('/home/libby/TindEEEEr/car.txt')
chocolate = read_text_file('/home/libby/TindEEEEr/chocolate.txt')
coffee = read_text_file('/home/libby/TindEEEEr/coffee.txt')
doctor = read_text_file('/home/libby/TindEEEEr/doctor.txt')
dentist = read_text_file('/home/libby/TindEEEEr/dentist.txt')
dogs = read_text_file('/home/libby/TindEEEEr/dogs.txt')
engineer = read_text_file('/home/libby/TindEEEEr/engineer.txt')
environmental = read_text_file('/home/libby/TindEEEEr/environmental.txt')
firefighter = read_text_file('/home/libby/TindEEEEr/firefighter.txt')
fitness = read_text_file('/home/libby/TindEEEEr/fitness.txt')
golf = read_text_file('/home/libby/TindEEEEr/golf.txt')
football = read_text_file('/home/libby/TindEEEEr/football.txt')
history = read_text_file('/home/libby/TindEEEEr/history.txt')
hockey = read_text_file('/home/libby/TindEEEEr/hockey.txt')
lawyer = read_text_file('/home/libby/TindEEEEr/lawyer.txt')
LOTR = read_text_file('/home/libby/TindEEEEr/LOTR.txt')
math = read_text_file('/home/libby/TindEEEEr/math.txt')
military = read_text_file('/home/libby/TindEEEEr/military.txt')
nerdy = read_text_file('/home/libby/TindEEEEr/nerdy.txt')
pizza = read_text_file('/home/libby/TindEEEEr/pizza.txt')
policeofficer = read_text_file('/home/libby/TindEEEEr/policeofficer.txt')
psychology = read_text_file('/home/libby/TindEEEEr/psychology.txt')
robot = read_text_file('/home/libby/TindEEEEr/robot.txt')
scifi = read_text_file('/home/libby/TindEEEEr/scifi.txt')
tallperson = read_text_file('/home/libby/TindEEEEr/tallperson.txt')
soccer = read_text_file('/home/libby/TindEEEEr/soccer.txt')
tennis = read_text_file('/home/libby/TindEEEEr/tennis.txt')
walkingdead = read_text_file('/home/libby/TindEEEEr/walkingdead.txt')
volleyball = read_text_file('/home/libby/TindEEEEr/volleyball.txt')
yoga = read_text_file('/home/libby/TindEEEEr/yoga.txt')

### Functions to modify the list into a dictionary
def standardize_format(list):
    """Removes whitespace, punctuation, and uppercase letters to standardize the
    format across pickup line lists for ease of comparison
    Args:
    list of pickup lines as strings
    Return Value:
    list of pickup lines as strings sans whitespace, punctuation and capitalization
    """
    lines = []
    for pul in list:
        pul = pul.strip(string.whitespace)
        for i in range(32):
            pul = pul.replace(string.punctuation[i],'')
        pul = pul.replace('','')
        pul = pul.lower()
        lines.append(pul)
    stringlines = ' '.join(lines)
    return lines

def generate_dict(list):
    """Creates a dictionary from the strings within the list and the index of each
    string
    Args:
    list of pickup lines contained in strings
    Return Value:
    dictionary of pickup lines as values and the indeces of each pickup line within
    the list as the keys
    """
    keys = []
    values = []
    for index, pul in enumerate(list):
        keys.append(index)
        values.append(pul)
        dict = OrderedDict(zip(keys,values))
    return dict

def remove_copies(list):
    """Uses previous two functions to take the original list of pickup lines and
    remove all duplicate lines
    Args:
    list of pickup lines contained in strings
    Return Value:
    dictionary of pickup lines as keys and 0 as each value
    """
    standardized = standardize_format(list)
    original_dict = generate_dict(list)
    standardized_dict = generate_dict(standardized)
    indexes = []
    lines = []
    for k, v in standardized_dict.items():
        if v not in lines:
            lines.append(v)
            indexes.append(k)
    new_dict = dict(original_dict)
    for k,v in original_dict.items():
        if k not in indexes:
            del new_dict[k]
    pickup_lines = new_dict.values()
    return_dict = OrderedDict(zip(pickup_lines,[0 for x in range(0,len(pickup_lines))]))
    return return_dict

## Uses functions defined above to generate the pickup lines dictionary
attempt = remove_copies(all_the_pickup_lines)
Olin = remove_copies(olin)
star_wars = remove_copies(star_wars)
music = remove_copies(music)
HIMYM = remove_copies(HIMYM)
GOT = remove_copies(GOT)
disney = remove_copies(Disney)
biochem = remove_copies(biochem)

### Pickles the dictionary to be used from other files.

pickup_pickle = open('pickuplines.pickle','wb')
pickle.dump(attempt, pickup_pickle)
pickle_olin = open('olinlines.pickle','wb')
pickle.dump(Olin, pickle_olin)
pickle_star_wars = open('star_wars.pickle','wb')
pickle.dump(star_wars, pickle_star_wars)
pickle_music = open('music.pickle','wb')
pickle.dump(music, pickle_music)
pickle_HIMYM = open('HIMYM.pickle','wb')
pickle.dump(HIMYM, pickle_HIMYM)
pickle_GOT = open('GOT.pickle','wb')
pickle.dump(GOT, pickle_GOT)
pickle_disney = open('disney.pickle','wb')
pickle.dump(disney, pickle_disney)
pickle_biochem = open('biochem.pickle','wb')
pickle.dump(biochem, pickle_biochem)
pickle_accountant = open('accountant.pickle','wb')
pickle.dump(accountant, pickle_accountant)
pickle_animal = open('animal.pickle','wb')
pickle.dump(animal, pickle_animal)
pickle_art = open('art.pickle','wb')
pickle.dump(art, pickle_art)
pickle_baseball = open('baseball.pickle','wb')
pickle.dump(baseball, pickle_baseball)
pickle_beach = open('beach.pickle','wb')
pickle.dump(beach, pickle_beach)
pickle_basketball = open('basketball.pickle','wb')
pickle.dump(basketball, pickle_basketball)
pickle_books = open('books.pickle','wb')
pickle.dump(books, pickle_books)
pickle_car = open('car.pickle','wb')
pickle.dump(car, pickle_car)
pickle_chocolate = open('chocolate.pickle','wb')
pickle.dump(chocolate, pickle_chocolate)
pickle_coffee = open('coffee.pickle','wb')
pickle.dump(coffee, pickle_coffee)
pickle_doctor = open('doctor.pickle','wb')
pickle.dump(doctor, pickle_doctor)
pickle_dentist = open('dentist.pickle','wb')
pickle.dump(dentist, pickle_dentist)
pickle_dogs = open('dogs.pickle','wb')
pickle.dump(dogs, pickle_dogs)
pickle_engineer = open('engineer.pickle','wb')
pickle.dump(engineer, pickle_engineer)
pickle_environmental = open('environmental.pickle','wb')
pickle.dump(environmental, pickle_environmental)
pickle_firefighter = open('firefighter.pickle','wb')
pickle.dump(firefighter, pickle_firefighter)
pickle_fitness = open('fitness.pickle','wb')
pickle.dump(fitness, pickle_fitness)
pickle_golf = open('golf.pickle','wb')
pickle.dump(golf, pickle_golf)
pickle_football = open('football.pickle','wb')
pickle.dump(football, pickle_football)
pickle_history = open('history.pickle','wb')
pickle.dump(history, pickle_history)
pickle_hockey = open('hockey.pickle','wb')
pickle.dump(hockey, pickle_hockey)
pickle_lawyer = open('lawyer.pickle','wb')
pickle.dump(lawyer, pickle_lawyer)
pickle_LOTR = open('LOTR.pickle','wb')
pickle.dump(LOTR, pickle_LOTR)
pickle_math = open('math.pickle','wb')
pickle.dump(math, pickle_math)
pickle_military = open('military.pickle','wb')
pickle.dump(military, pickle_military)
pickle_nerdy = open('nerdy.pickle','wb')
pickle.dump(nerdy, pickle_nerdy)
pickle_pizza = open('pizza.pickle','wb')
pickle.dump(pizza, pickle_pizza)
pickle_policeofficer = open('policeofficer.pickle','wb')
pickle.dump(policeofficer, pickle_policeofficer)
pickle_psychology = open('psychology.pickle','wb')
pickle.dump(psychology, pickle_psychology)
pickle_robot = open('robot.pickle','wb')
pickle.dump(robot, pickle_robot)
pickle_scifi = open('scifi.pickle','wb')
pickle.dump(scifi, pickle_scifi)
pickle_tallperson = open('tallperson.pickle','wb')
pickle.dump(tallperson, pickle_tallperson)
pickle_soccer = open('soccer.pickle','wb')
pickle.dump(soccer, pickle_soccer)
pickle_tennis = open('tennis.pickle','wb')
pickle.dump(tennis, pickle_tennis)
pickle_walkingdead = open('walkingdead.pickle','wb')
pickle.dump(walkingdead, pickle_walkingdead)
pickle_volleyball = open('volleyball.pickle','wb')
pickle.dump(volleyball, pickle_volleyball)
pickle_yoga = open('yoga.pickle','wb')
pickle.dump(yoga, pickle_yoga)
