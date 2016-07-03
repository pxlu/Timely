# -*- coding: utf-8 -*-
# screen.py

# Native libraries
import json
import sys
import re
import uuid
import math
# Custom libraries
from classes import *
import JSONify
import parser
import common

CONFIDENCE_WEIGHT_FACTOR = 1.0

KEYWORDS = common._init_keywords_list()
KEYWORDS_NAMES = common._get_keywords(KEYWORDS)
DISORDERS = common._init_disorders_list()

def _calculate_adjustment(base_rate, disorder_confidence, rate_difference, weight_factor):

    confidence_value = -1
    # If greater, adjust down from base rate
    if base_rate >= disorder_confidence:
        confidence_value = base_rate - (1 - base_rate) * rate_difference * CONFIDENCE_WEIGHT_FACTOR
    # Otherwise adjust up
    else:
        confidence_value = base_rate + (1 - base_rate) * rate_difference * CONFIDENCE_WEIGHT_FACTOR

    return confidence_value

def _disorder_confidence(user_profile):

    confidence_list = []
    for disorder in DISORDERS:
        disorder_confidence = 0
        disorder_list = disorder.symptoms
        for symptom in user_profile.keywords.keys():
            if symptom in disorder_list:
                disorder_confidence += 1
        disorder_confidence /= len(DISORDERS)

        # Start with base rate and adjust from there
        base_rate = float(disorder.base_rate)
        rate_difference = math.fabs(base_rate - disorder_confidence)
        confidence_value = _calculate_adjustment(base_rate, disorder_confidence, rate_difference, CONFIDENCE_WEIGHT_FACTOR)
        confidence_list.append((disorder.name, str(math.ceil(confidence_value * 100))  + '%'))

    return sorted(confidence_list, key=lambda l_value: int((l_value[1])[:-1]), reverse=True)

def _disorder_severities(disorders_dict, keywords_list):

    for disorder in disorders_dict:
        disorder_severity = 0
        for symptom in disorder.symptoms:
            keyword_sev = next((x.rating for x in keywords_list if x.name == symptom), 0)
            disorder_severity += int(keyword_sev)
        disorder.severity = disorder_severity

def _get_severity(user_profile, keywords_list):

    user_severity = 0
    for keyword, num_occurence in user_profile.keywords.items():
        keyword_sev = next((x.rating for x in keywords_list if x.name == keyword), 0)
        user_severity += num_occurence * int(keyword_sev)

    return user_severity

def _get_profile(in_file, profile_name):

    word_dict = parser.parse_text(in_file)
    _disorder_severities(DISORDERS, KEYWORDS)
    user_profile = UserProfile(name=str.capitalize(profile_name))

    # Filter by keywords only
    # Use filter function here!
    user_keywords = {element[0]: element[1] for element in word_dict.items() if element[0] in KEYWORDS_NAMES}

    # Fill in fields of user_profile
    user_profile.uid = uuid.uuid4()
    user_profile.keywords = user_keywords
    user_profile.severity = _get_severity(user_profile, KEYWORDS)
    user_profile.confidence = _disorder_confidence(user_profile)

    in_file.close()

    return user_profile

### User testing helpers ###

def _begin_prompt():

    print('-- Hello! You are using Timely-[Screen], an interactive screening tool for assessing potential mental health disorders.')
    print('-- To begin, could you please tell me your name?')
    user_name = input('==> ')
    if not re.match(r'[A-Za-z]+', user_name):
        raise InvalidInputException('Sorry! Only names with alphabetical characters are accepted.')
    welcome_msg = '-- Welcome {}!'.format(user_name.capitalize())
    print(welcome_msg)

    return user_name

def _selection_prompt():

    print('-- Please select an option from below: \n======================================= \
                \n-> [New] to perform a screening from the beginning, with your input. \
                \n-> [Existing] to specify an existing persona file to be screened.\
                \n-> [Quit] to quit this program.')
    user_option = input('==> ').capitalize()
    if not re.match(r'New|Existing|Quit', user_option):
        print('[!] Sorry, you chose an invalid option.')
        user_option = -1

    return user_option

def _execute_options(user_option, user_name):

    if user_option == 'Quit':
        print('Thanks for using Timely-[Screen]!')
        raise QuitException
    elif user_option == 'New':
        print('-- Please enter your persona below: ')
        persona = input('==> ')
        user_persona_file = open(user_name + '.md', 'w')
        user_persona_file.write(persona)
        user_persona_file.close()
        user_persona_file = open(user_name + '.md', 'r')
    else:
        file_found = False
        while file_found is False:
            print('-- Please enter the pre-existing persona file to screen: ')
            try:
                user_persona_file_name = input('==> ')
                user_persona_file = open(user_persona_file_name, 'r')
                file_found = True
            except FileNotFoundError:
                print("That is not a valid file name! Please enter a valid file name.")

    return user_persona_file

def main():

    try:
        user_name = _begin_prompt()
        user_option = -1
        while True:
            while user_option is -1:
                user_option = _selection_prompt()
            user_persona_file = _execute_options(user_option, user_name)
            user_profile = _get_profile(user_persona_file, user_name)
            print('================================================== \
                \n[!] Your results: \n' + str(user_profile) + '\
                \n==================================================')
            user_option = -1
    except InvalidInputException:
        sys.exit()
    except QuitException:
        sys.exit()

if __name__ == '__main__':
    '''
    try:
        in_file_name = sys.argv[1]
        profile_name = re.search('[A-Za-z]+\.md', in_file_name).group(0).split('.')[0]
        in_file = open(in_file_name, 'r')
        _get_profile(in_file, profile_name)
    except IndexError:
        print("Usage: `python main.py [inFile]`")
    '''
    main()
    # '''