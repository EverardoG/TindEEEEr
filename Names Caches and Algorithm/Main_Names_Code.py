import argparse
import configparser
import json
from random import randint
import requests
import re
import sys
import robobrowser
import time
import datetime
import pynder
import random
from os.path import exists
from pickle import dump, load
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

def create_list_of_near_names(name):
    api = datamuse.Datamuse()
    list_of_dictionaries = api.words(sl = name, max = 10)
    list_of_names = []
    for i in list_of_dictionaries:
        if i['score'] == 100:
            list_of_names.append(i['word'])
    if name not in list_of_names:
        list_of_names.append(name)
    if len(list_of_names) > 5:
        list_of_names = list_of_names[:4]
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

    pickuplines = []
    if len(name)> 10:
        return pickuplines

    named = name.lower()+'d'
    named = named.replace(' ', "")
    english_dictionary = enchant.Dict("en_US")
    spanish_dictionary = enchant.Dict("es_ES")

    list_of_all_anagrams = ["".join(perm) for perm in itertools.permutations(named)]

    list_of_real_anagrams = []
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

    pickuplines = []
    if len(name)> 10:
        print("Name is too long for anagrams.")
        return pickuplines

    named = name.lower()+'v'
    named = named.replace(" ", "")
    named = named.replace(string.punctuation, "")
    english_dictionary = enchant.Dict("en_US")
    spanish_dictionary = enchant.Dict("es_ES")

    list_of_all_anagrams = ["".join(perm) for perm in itertools.permutations(named)]

    list_of_real_anagrams = []

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


def get_access_token(email, password):
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
    FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    ## Submit login form
    f = s.get_form()
    f["pass"] = password
    f["email"] = email
    s.submit_form(f)

    ## Click the 'ok' button on the dialog informing you that you have already authenticated with the Tinder app
    f = s.get_form()
    s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])

    ## Get access token from the http response
    access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
    return access_token

def log(msg):
    print('[' + str(datetime.datetime.now()) + ']' + ' ' + msg)

def start_session():
    try:
        access_token = get_access_token('pickupgenerator@gmail.com', 'softdes')
        print('Succeeded in retrieve access token.')
        auth = str(access_token)
    except:
        log('Unable to get retrieve token.')
        try:
            access_token = get_access_token('pickupgenerator@gmail.com', 'softdes')
            print('Succeeded in retrieve access token.')
            auth = str(access_token)
        except:
            log('Unable to get retrieve token on second try. Shutting down...')
            quit()
    facebook_ID = 100025429656340 #taken from https://findmyfbid.com/

    requests.packages.urllib3.disable_warnings()  # Find way around this...
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    global session
    session = None

    log("Starting Tinder session...")
    try:
        session = pynder.Session(facebook_id = str(facebook_ID), facebook_token=auth)
        log("Session started.")
    except pynder.errors.RequestError:
        log("Session failed. Trying again to start session...")
        auth = get_access_token(str(pickupgenerator@gmail.com), str(softdes))
        try:
            pynder.Session(facebook_id = str(facebook_ID), facebook_token=auth)
            log("Session started.")
        except pynder.errors.RequestError:
            log("Unable to start session on second try. Shutting down and pickling...")
            pickle_all()
            quit()

def add_contributed_PUL_to_contributors(match, PUL, name): #CHECK THIS
    if not match['_id'] in PUL_contributors:
        PUL_contributors[match['_id']]={}
    PUL_contributors[match['_id']][PUL] = name

def add_new_matches_to_match_status_dictionary(matches):
    for match in matches:
        try:
            if not match['_id'] in match_status_dictionary:
                match_status_dictionary[match['_id']] = {'status': 'new',
                                                        'last_time_checked': 0}
        except:
            print("Failed to match with ",match['_id'])

def is_unread(match):
    if match['messages']:
        last_message = match['messages'][-1]
        if last_message['from'] == session.profile.id or last_message['timestamp'] <= match_status_dictionary[match['_id']]['last_time_checked']:
            return False
        else:
            return True
    else:
        return True
def is_name(name):
    if name in ["", " ", "   ", "no"] or len(name) <= 1:
        return False
    else:
        return True

def is_PUL(PUL):
    if len(PUL)< 10:
        return False
    else:
        return True

def is_feedback(feedback):
    feedback = feedback.replace(" ","")
    feedback = feedback.replace(string.punctuation, "")
    feedback = feedback.lower()
    valid = ['g', 'b', 'w', 'o', 'good', 'bad', 'wrong', 'ok', 'okay']
    if feedback in valid:
        return True
    return False

def is_pass(feedback):
    feedback = feedback.lower()
    feedback = feedback.replace(string.punctuation, "")
    feedback = feedback.replace(" ","")
    valid = ['pass', 'no', 'idk']
    for i in valid:
        if i == feedback:
            return True
    return False

def return_weight_modifier_from_feedback(feedback):
    feedback = feedback.lower()
    if 'g' in feedback:
        return 2
    elif 'b' in feedback:
        return -2
    elif 'w' in feedback:
        return -4
    elif 'o' in feedback:
        return 1
    else:
        return 0


def update_last_time_checked(match):
    match_status_dictionary[match['_id']]['last_time_checked'] = match['messages'][-1]['timestamp']

def send_message(match, message):
    time.sleep(2)
    add_space = randint(1,2)
    if add_space == 1:
        message = message + " "
    session._api._post('/user/matches/' + match['_id'],
                                {"message": message})
    time.sleep(1)
def change_status_to(match, status):
    match_status_dictionary[match['_id']]['status'] = status

def get_last_message_text(match):
    return match['messages'][-1]['message']

def process_new(match):
    send_message(match, "*beep boop* Hello! Thanks for swiping right on me. I will do my best to help you find"+
                " the perfect pick-up lines! All you need to do is message the word 'help' whenever you need me.")
    change_status_to(match,'idle')
    update_last_time_checked(match)

def help_sensor(match):
    last_message = get_last_message_text(match)
    last_message = last_message.lower()
    if 'help' in last_message:
        send_message(match, "Give me the first name of the person you need a pick-up line for. For example, 'Emma'.")
        change_status_to(match, 'waiting_for_name')
        update_last_time_checked(match)
        return True
    else:
        return False

def grab_random_name_from_no_lines_or_need_lines():
    if no_lines:
        return random.choice(no_lines)
    else:
        if need_lines:
            return random.choice(need_lines)

def change_a_value_in_status_dictionary(match, key, value):
    match_status_dictionary[match['_id']][key] = value

def robot_sensor(match):
    last_message = get_last_message_text(match)
    if '🤖' in last_message and len(last_message)<=3:
        if not no_lines or not need_lines:
            send_message(match, "*beep boop* Thanks for coming to help out! Unfortunately my memory is full right now. Can't learn any more lines *rattle*")
            return False
        #try:
        send_message(match, "*beep boop* Learning all of these pick-up lines is hard work. *rattle* "+
                     "Thanks for coming to help out! I will give you a highly requested name"+
                    " that I have no lines for, and you can help me think of one. Every once in a while, "+
                    "I'll send you a report on whether people liked your lines or not!")
        train_name = grab_random_name_from_no_lines_or_need_lines()
        send_message(match, "Can you give me one pick-up line for "+train_name.upper()+"? Type 'pass' if you're stuck.")
        change_status_to(match, 'training')
        change_a_value_in_status_dictionary(match,'train_name', train_name)
        update_last_time_checked(match)
        return True
        #except:
            #send_message(match, "*beep boop* Thanks for coming to help out! Unfortunately my memory is full right now. Can't learn any more lines *rattle*")
            #return False
    else:
        return False

def process_idle(match):
    if help_sensor(match):
        return
    elif robot_sensor(match):
        return
    send_message(match, "*zzzzz* I'm taking a break. Send the word 'help' when you need me.")
    update_last_time_checked(match)


def process_waiting_for_name(match):
    if help_sensor(match):
        return
    elif robot_sensor(match):
        return

    name = get_last_message_text(match)
    name = name.lower()
    name = name.replace(" ", "")
    name = name.replace(string.punctuation, "")
    if not is_name(name):
        send_message(match, "*beep beep* Try giving me another name.")
        update_last_time_checked(match)
        return
    else:
        send_message(match, "*vrrrr* Searching...")
        list_of_PULs = receiving_name_request(name)
        send_message(match, "*beep boop* Let me know how my lines are. Respond the words 'good', 'ok' or 'bad'."+
                     "  If the line doesn't make any sense, respond the word 'wrong'.")
        change_a_value_in_status_dictionary(match,'name_request', name)
        if list_of_PULs == 'Give General.' or list_of_PULs == []:
            send_message(match, "No pick-up lines were found for "+name.title()+". But I have these sweet lines"+
                        " for you instead:")
            list_of_PULs = receiving_name_request('random')
            change_a_value_in_status_dictionary(match,'name_request', 'random')
        send_message(match, list_of_PULs[0])
        change_a_value_in_status_dictionary(match,'PULs_to_give', list_of_PULs)
        change_status_to(match, "giving_lines")
        update_last_time_checked(match)

def process_giving_lines(match):
    if help_sensor(match):
        return
    elif robot_sensor(match):
        return

    feedback = get_last_message_text(match)
    feedback = feedback.lower()
    feedback = feedback.replace(" ","")
    feedback = feedback.replace(string.punctuation, "")
    if not is_feedback(feedback):
        send_message(match, "*rattle* Please tell me if this line is 'good', 'ok', 'bad' or 'wrong'."+
                     " You can send abbreviated words like 'g' for good as well.")
        update_last_time_checked(match)
        return
    else:
        name = match_status_dictionary[match['_id']]['name_request']
        PUL = match_status_dictionary[match['_id']]['PULs_to_give'][0]
        value_modifier = return_weight_modifier_from_feedback(feedback)
        receiving_weight_modifiers(name, PUL, value_modifier)
        try:
            del match_status_dictionary[match['_id']]['PULs_to_give'][0]
        except:
            print("Failed to delete pick_up line from PULs_to_give.")
        if not match_status_dictionary[match['_id']]['PULs_to_give']:
            send_message(match, "That's all I've got! Send 'help' when you need me again.")
            change_status_to(match, 'idle')
            update_last_time_checked(match)
            return
        else:
            next_PUL = match_status_dictionary[match['_id']]['PULs_to_give'][0]
            send_message(match, next_PUL)
            update_last_time_checked(match)
            return

def process_training(match):
    if help_sensor(match):
        return
    elif robot_sensor(match):
        return

    feedback = get_last_message_text(match)
    name = match_status_dictionary[match['_id']]['train_name']
    if is_pass(feedback):
        train_name = grab_random_name_from_no_lines_or_need_lines()
        send_message(match, "Can you give me one pick-up line for "+train_name.upper()+"? Type 'pass' if you're stuck.")
        change_a_value_in_status_dictionary(match,'train_name', train_name)
        update_last_time_checked(match)
        return
    else:
        send_message(match, "*beep boop* Adding line to memory...")
        if is_PUL(feedback):
            add_PUL_to_database(name, feedback)
            add_contributed_PUL_to_contributors(match, feedback, name)
        send_message(match, "Do you have another line for "+name.upper()+"? Type 'pass' if you're stuck.")
        update_last_time_checked(match)


def process_unread_message(match):
    status = match_status_dictionary[match['_id']]['status']
    if status == 'new':
        process_new(match)
    elif status == 'idle':
        process_idle(match)
    elif status == 'waiting_for_name':
        process_waiting_for_name(match)
    elif status == 'giving_lines':
        process_giving_lines(match)
    elif status == 'training':
        process_training(match)

start_session()
load_all()

pickle_counter = 0
pickle_by_time_counter = 0

now = time.time()
end = now + 18000 # a few hours
while time.time() < end:
    try:
        sleep_time = randint(15,35)
        print("Sleeping for ", str(sleep_time), " seconds...")
        time.sleep(sleep_time)
        pickle_counter += 1
        pickle_by_time_counter += 1
        if pickle_counter > 300:
            print("Pickling all.")
            pickle_all()
            pickle_counter = 0
        if pickle_by_time_counter > 3600:
            print("Pickling all by time.")
            pickle_all_by_date(str(time.time()))
            pickle_counter_by_time = 0

        matches = session._api.matches(0)
        print(len(matches))
        add_new_matches_to_match_status_dictionary(matches)
        try:
            for match in matches:
                try:
                    if is_unread(match):
                        process_unread_message(match)
                except:
                    try:
                        print("Failed to process new message from ", match['person']['name'])
                    except:
                        print("Failed to process new message.")
        except:
            print("Failed to iterate through matches.")

        print(match_status_dictionary)
    except:
        print("Loop failed. Restarting session now. Will quit if restart fails.")
        try:
            start_session()
        except:
            print("Shutting down. Pickling...")
            pickle_all()
            quit()
    #except:
        #try:
            #print("Failed to loop through matches.")
            #start_session()
        #except:
            #quit()
            #pass
