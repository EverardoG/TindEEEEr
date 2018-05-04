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
from os.path import exists
import sys
from pickle import dump, load
import numpy
import re
import pickle
def pickle_dictionary(dictionary, file_name):
    dump(dictionary, open(file_name, 'wb'))

def create_list_of_near_names(name):
    api = datamuse.Datamuse()
    list_of_dictionaries = api.words(sl = name, max = 10)
    list_of_names = []
    for i in list_of_dictionaries:
        if i['score'] == 100:
            list_of_names.append(i['word'])
    if name not in list_of_names:
        list_of_names.append(name)
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
        return pickuplines
    else:
        print("No pickup lines for "+ name+ " found on Reddit.")
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
    return [name.title() + " - your name is a palindrome, I like it. I'd do you forwards and backwards"]

def return_anagram_PULine_D(name):
    named = name.lower()+'d'
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
    return pickuplines

def return_anagram_PULine_V(name):
    named = name.lower()+'v'
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
    return pickuplines

def gather_all_PU_lines_for_a_name(name):
      names_list = create_list_of_near_names(name)
      PULines = []
      for each_name in names_list:
          PULines+=return_reddit_PULine(each_name)

      PULines+=return_palindrome_PULine(name)
      try:
          PULines+=return_anagram_PULine_D(name)
          PULines+=return_anagram_PULine_V(name)
      except:
          pass
      return PULines


lines = '1MichaelJessica2MatthewAshley3ChristopherEmily4JacobSamantha5JoshuaSarah6NicholasTaylor7TylerHannah8BrandonBrittany9DanielAmanda10AustinElizabeth11AndrewKayla12JosephRachel13JohnMegan14ZacharyAlexis15RyanLauren16DavidStephanie17JamesCourtney18JustinJennifer19AnthonyNicole20WilliamVictoria21AlexanderBrianna22RobertAmber23JonathanMorgan24KyleDanielle25KevinJasmine26CodyAlexandra27ThomasAlyssa28ChristianRebecca29JordanMadison30AaronKatherine31BenjaminAnna32EricHaley33SamuelKelsey34DylanAllison35JoseMelissa36BrianAbigail37StevenKimberly38AdamShelby39NathanOlivia40TimothyMary41JasonMichelle42RichardKaitlyn43PatrickSydney44CharlesMaria45SeanChristina46JesseTiffany47AlexChelsea48JeremySara49CameronErin50JuanJordan51LoganNatalie52MarkBrooke53HunterMarissa54CalebHeather55ConnorAndrea56DakotaLaura57StephenMiranda58DevinPaige59LuisKatelyn60EvanSierra61TrevorGabrielle62DustinJulia63JaredVanessa64JeffreyKelly65GabrielKristen66TravisDestiny67IanEmma68CarlosSavannah69TaylorErica70BryanJacqueline71PaulMariah72KennethAlexandria73NathanielShannon74CoreyBriana75EthanBreanna76JesusAmy77BlakeKatie78BradleyCassandra79MitchellMadeline80GarrettCrystal81MarcusCaitlin82LukeLindsey83DerekKathryn84GregoryJenna85AntonioAngela86TannerCheyenne87DaltonMonica88EdwardMackenzie89PeterAlicia90VictorCatherine91LucasSelena92ScottCaroline93ElijahJamie94MiguelKaitlin95ChaseSabrina96SethBailey97AdrianGrace98IsaacMolly99NoahBrittney100ShawnAlexa'
lines = re.sub( r"([A-Z])", r" \1", lines)
for i in range(0,10):
  lines= lines.replace(str(i), ' ')
name_list = lines.split()

def add_PUL_to_database(name, PUL, dictionary):
  """Return updated dictionary"""
  if name not in dictionary:
      dictionary[name] = {PUL:15}
  else:
      dictionary[name][PUL] = 15
  return dictionary

def reset_all():
    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    dictionary = {}
    no_lines = []
    need_lines = []
    bad_lines = {} #{name:[list of bad lines]}



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

def recieving_name_request(name):
    """Returns list of 0-3 pickup-lines. Adds new lines to database"""
    name = name.lower()

    global dictionary
    global no_lines
    global need_lines
    global bad_lines
    global gather_all_PU_lines_for_a_name
    global add_PUL_to_database

    if name in no_lines:
        return 'give general' #change
    else:
        if name in dictionary:
            return pick_PULs_from_database(dictionary[name])
        else:
            dictionary[name]={}
            names_PUL_from_internet = gather_all_PU_lines_for_a_name(name)
            if not names_PUL_from_internet:
                no_lines.append(name)
                need_lines.append(name)
                return 'give general'
            else:
                for PUL in names_PUL_from_internet:
                    add_PUL_to_database(name, PUL, dictionary)
                if len(dictionary[name]) <=3:
                    need_lines.append(name)
                return pick_PULs_from_database(dictionary[name])

def load_cache(file ="names_PUL_cache"):
    cache = pickle.load( open( file, "rb" ) )
    print(cache)
    return cache
if __name__ == "__main__":
    dictionary = load_cache("names_PUL_cache")
    need_lines = []
    bad_lines = {}
    no_lines = []
    try:
        print(dictionary)
    except:
        reset_all()
        print("Resetting All")

    counter = 0
    for i in name_list:

        if i in []:
            continue
        try:
            recieving_name_request(i)
            counter += 1
            if counter % 2 == 0:
                pickle_dictionary(dictionary, 'names_PUL_cache')
                pickle_dictionary(need_lines, 'names_need_lines_cache')
                pickle_dictionary(no_lines, 'names_no_lines_cache')
                print(str(counter)+" names scraped: ")
                print(dictionary)
        except:
            print("Failed on "+i+". Moving on...")
