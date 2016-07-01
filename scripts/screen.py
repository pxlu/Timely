# -*- coding: utf-8 -*-
# screen.py

# Native libraries
import json
import sys
import re
import uuid
import math
import multiprocessing as mp
# Custom libraries
import JSONify
import parser
from classes import *

SEVERITY_MAPPING = "../json/severity.json"
DISORDERS_MAPPING = "../json/disorders.json"
CONFIDENCE_WEIGHT_FACTOR = 1.0

def _init_severity():

    sev_file = open(SEVERITY_MAPPING)
    sev_list = json.loads(sev_file.read())['results']['keywords']
    sev_ratings = {sev_element['name']: sev_element['rating'] for sev_element in sev_list}
    return sev_ratings

SEVERITY = _init_severity()

def _init_disorders_list():

    disorders_file = open(DISORDERS_MAPPING)
    disorders_list = json.loads(disorders_file.read())['results']['disorders']
    disorders = [Disorder(name=disorder['name'],disid=disorder['id'],symptoms=[symptom for symptom in disorder['symptoms'].split(',')],base_rate=disorder['base_rate']) for disorder in disorders_list]

    return disorders

DISORDERS = _init_disorders_list()

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

def _disorder_severities(disorders_dict, severity_dict):

    for disorder in disorders_dict:
        disorder_severity = 0
        for symptom in disorder.symptoms:
            disorder_severity += float(severity_dict[symptom])
        disorder.severity = disorder_severity

def _get_severity(user_profile):

    user_severity = 0
    for keyword, num_occurence in user_profile.keywords.items():
        user_severity += num_occurence * int(SEVERITY[keyword])

    return user_severity

def _parse_bio(in_file, profile_name):

    word_dict = parser.parse_text(in_file)
    _disorder_severities(DISORDERS, SEVERITY)
    user_profile = UserProfile(name=str.capitalize(profile_name))

    # Filter by keywords only
    # Use filter function here!
    user_keywords = {element[0]: element[1] for element in word_dict.items() if element[0] in SEVERITY}

    # Fill in fields of user_profile
    user_profile.uid = uuid.uuid4()
    user_profile.keywords = user_keywords
    user_profile.severity = _get_severity(user_profile)
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

def _execute_options(user_option):

    if user_option == 'Quit':
        raise QuitException('User has selected to quit.')
    elif user_option == 'New':
        print('-- Please enter your persona below: ')
        persona = input('==> ')
        user_persona_file = open(user_name + '.md', 'r+')
        user_persona_file.write(persona)
    else:
        print('-- Please enter the pre-existing persona file to screen: ')
        user_persona_file_name = input('==> ')
        user_persona_file = open(user_persona_file_name, 'r')

    return user_persona_file

def main():

    try:
        user_name = _begin_prompt()
        user_option = -1
        while user_option is -1:
            user_option = _selection_prompt()
        user_persona_file = _execute_options(user_option)
        user_profile = _parse_bio(user_persona_file, user_name)
        print('================================================== \
            \n[!] Your results: \n' + str(user_profile) + '\
            \n==================================================')
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
        _parse_bio(in_file, profile_name)
    except IndexError:
        print("Usage: `python main.py [inFile]`")
    '''
    main()
    # '''