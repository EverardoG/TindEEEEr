from names_functions import *
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
        access_token = get_access_token('contact.businesshaven@gmail.com', 'softdes')
        print('Succeeded in retrieve access token.')
        auth = str(access_token)
    except:
        log('Unable to get retrieve token.')
        try:
            access_token = get_access_token('contact.businesshaven@gmail.com', 'softdes')
            print('Succeeded in retrieve access token.')
            auth = str(access_token)
        except:
            log('Unable to get retrieve token on second try. Shutting down...')
            quit()
    facebook_ID = 100025429656340 #taken from https://findmyfbid.com/

    requests.packages.urllib3.disable_warnings()  # Find way around this...
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    #global session
    #session = None

    log("Starting Tinder session...")
    try:
        session = pynder.Session(facebook_id = str(facebook_ID), facebook_token=auth)
        log("Session started.")
    except pynder.errors.RequestError:
        log("Session failed. Trying again to start session...")
        auth = get_access_token(str(contact.businesshaven@gmail.com), str(softdes))
        try:
            pynder.Session(facebook_id = str(facebook_ID), facebook_token=auth)
            log("Session started.")
        except pynder.errors.RequestError:
            log("Unable to start session on second try. Shutting down...")
            quit()

def add_contributed_PUL_to_contributors(match, PUL, name): #CHECK THIS
    if not match['_id'] in PUL_contributors:
        PUL_contributors[match['_id']]={}
    PUL_contributors[match['_id']][PUL] = name

def add_new_matches_to_match_status_dictionary(matches):
    for match in matches:
        if not match['_id'] in match_status_dictionary:
            match_status_dictionary[match['_id']] = {'status': 'new',
                                                    'last_time_checked': 0}

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
    feedback = feedback.strip(" ")
    feedback = feedback.lower()
    valid = ['g', 'b', 'w', 'o', 'good', 'bad', 'wrong', 'ok', 'okay']
    if feedback in valid:
        return True
    return False

def is_pass(feedback):
    feedback = feedback.lower()
    feedback = feedback.strip(' ')
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
    update_last_time_checked(match)

def process_waiting_for_name(match):
    if help_sensor(match):
        return
    elif robot_sensor(match):
        return

    name = get_last_message_text(match)
    name = name.lower()
    name.strip(" ")
    if not is_name(name):
        send_message(match, "*beep beep* Try giving me another name.")
        update_last_time_checked(match)
        return
    else:
        list_of_PULs = receiving_name_request(name)
        send_message(match, "*beep boop* Let me know how my lines are. Respond the words 'ok', 'good' or 'bad'."+
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
    feedback = feedback.strip(" ")
    if not is_feedback(feedback):
        send_message(match, "*rattle* Please tell me if this line is 'ok', 'good', 'bad' or 'wrong'."+
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
