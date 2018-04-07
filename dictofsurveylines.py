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
    print(lines1)
    return lines1

get_word_list('/home/libby/TindEEEEr/InClassSurveyPickuplines.txt')
get_word_list('/home/libby/TindEEEEr/CarpeSurveysPickuplines.txt')
