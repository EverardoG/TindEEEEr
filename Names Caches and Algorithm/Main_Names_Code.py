start_session()
load_all()

pickle_counter = 0
pickle_by_time_counter = 0

now = time.time()
end = now + 18000 # a few hours
while time.time() < end:
    time.sleep(5)
    pickle_counter += 1
    pickle_by_time_counter += 1
    if pickle_counter > 300:
        try:
            pickle_all()
        except:
            print("PICKLE FAILED.")
        pickle_counter = 0
    if pickle_by_time_counter > 7000:
        try:
            pickle_all_by_date()
        except:
            print("PICKLE FAILED.")
        pickle_counter_by_time = 0

    try:
        matches = session._api.matches(0)
        add_new_matches_to_match_status_dictionary(matches)
    except:
        print("Failed to receive matches and add to match_status_dictionary.")
        start_session()
        quit()
    try:
        for match in matches:
            try:
                if is_unread(match):
                    process_unread_message(match)
            except:
                pass
        print(match_status_dictionary)
    except:
        start_session()
        quit()
