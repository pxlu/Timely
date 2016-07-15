# -*- coding: utf-8 -*-
# screen.py

# Native Python Libraries
import sys
import re
import math
from collections import OrderedDict
# Third Party Libraries
from nltk.stem.snowball import SnowballStemmer
# Local Libraries
import JSONify
from timely_classes import *
import timely_parser
import timely_common

KEYWORDS = timely_common._init_keyword_list()
KEYWORDS_NAMES = timely_common._get_keywords(KEYWORDS)
DISORDERS = timely_common._init_disorder_list()

def _calculate_adjustment(base_rate, disorder_confidence, rate_difference):

    '''
    Calculates the adjustment from the base_rate, based on observed (anecdotal) confidence from the user provided by disorder_confidence, with consideration to the difference between the base_rate and disorder_confidence, provided by rate_difference, and with final adjustment with weight_factor.

    :param: base_rate: the base rate of the disorder
    :param: disorder_confidence: the observed rate of the disorder from the user
    :param: rate_difference: the absolute difference between the base_rate and the disorder_confidence
    :return: the adjusted confidence_value for the disorder for the user, adjusted from the base_rate with consideration for observed user data
    '''

    confidence_value = -1
    CONFIDENCE_WEIGHT_FACTOR = 1.0

    adjustment = (1 - base_rate) * rate_difference * CONFIDENCE_WEIGHT_FACTOR
    # If greater, adjust down from base rate
    confidence_value = base_rate - adjustment if base_rate >= disorder_confidence else base_rate + adjustment

    return confidence_value

def _disorder_confidence(user_profile, disorder_list):

    '''
    Outputs a list of disorders with their confidence values for the given user_profile, sorted in descending order of confidence_value.

    :param: user_profile: a given user profile to calculate disorder confidence from
    :disorder_list: a list of possible disorders
    :return a list of possible disorder from the given user_profile, in descending order of confidence_value
    '''

    disorders_stemmer = SnowballStemmer("english")
    confidence_list = []

    for disorder in disorder_list:
        user_disorder_confidence = 0
        symptoms_list = [disorders_stemmer.stem(symptom) for symptom in disorder.symptoms]

        # Get the confidence rate of the disorder based on the user_profile
        for symptom in user_profile.keywords.keys():
            if symptom in symptoms_list:
                user_disorder_confidence += 1
        user_disorder_confidence /= len(DISORDERS)

        # Start with base rate and adjust based on user_disorder_confidence
        base_rate = float(disorder.base_rate)
        rate_difference = math.fabs(base_rate - user_disorder_confidence)
        confidence_value = _calculate_adjustment(base_rate, user_disorder_confidence, rate_difference)

        # Get the name of the disorder and append the confidence value and the name into the return list as a tuple
        disorder_name = next((list_disorder for list_disorder in disorder_list if list_disorder.name == disorder.name), None)
        confidence_list.append((disorder_name, str(math.ceil(confidence_value * 100))  + '%'))

    return sorted(confidence_list, key=lambda l_value: int((l_value[1])[:-1]), reverse=True)

def _init_disorder_severities(disorders_dict, keywords_list):

    '''
    Initilize the severity rating of disorders from the disorders_dict, given a list of keywords provided by keywords_list.

    :param disorders_dict: a dictionary of disorders to calculate the serverity for
    :param keywords_list: a list of keywords used to calculate disorder serverities
    :return void (Doesn't return anything)
    '''

    for disorder in disorders_dict:
        disorder_severity = 0
        for symptom in disorder.symptoms:
            keyword_sev = next((x.rating for x in keywords_list if x.name == symptom), 0)
            disorder_severity += int(keyword_sev)
        disorder.severity = disorder_severity

def _get_severity(user_profile, keywords_list):

    '''
    Output the severity of the user_profile, given the keywords_list.

    :param user_profile: the user profile to calculate the serverity for
    :param keywords_list: a list of keywords used to calculate the serverity
    :return the severity of the user_profile
    '''

    user_severity = 0 # Fix for default value
    for keyword, num_occurence in user_profile.keywords.items():
        keyword_sev = next((x.rating for x in keywords_list if x.name == keyword), 0)
        user_severity += num_occurence * int(keyword_sev)

    return user_severity

def _get_profile(in_file, profile_name):

    '''
    Initilize and output a user profile for the given in_file, with user_profile.name represented by profile_name.

    :param in_file: a bio of a user to be parsed to generate the user_profile
    :param profile_name: the name of the user
    :return a user profile based on the information given in in_file
    '''

    # Init stemmer
    stemmer = SnowballStemmer("english")
    keywords_stem = [stemmer.stem(word) for word in KEYWORDS_NAMES]

    # Parse words from user profile and init severities & user profile
    word_list = timely_parser.parse_text(in_file)
    _init_disorder_severities(DISORDERS, KEYWORDS)
    user_profile = UserProfile(name=str.capitalize(profile_name))

    # Filter by keywords only
    user_keywords = {word[0]: word[1][0] for word in word_list if word[0] in keywords_stem}
    sorted_user_words = OrderedDict(sorted(user_keywords.items(), key=lambda element: element[0]))

    # Fill in fields of user_profile
    user_profile.uid = user_profile._generate_uid()
    user_profile.keywords = sorted_user_words
    user_profile.severity = _get_severity(user_profile, KEYWORDS)
    user_profile.disorders = _disorder_confidence(user_profile, DISORDERS)

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
        print('-- Please tell me a little bit about your condition...')
        persona = input('==> ')
        user_persona_file = open(user_name + '.md', 'w')
        user_persona_file.write(persona)
        user_persona_file.close()
        user_persona_file = open(user_name + '.md', 'r')
        print('Please wait while your profile is being created...')
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
        print('Please wait while your profile is being created...')
    return user_persona_file

def start_screen():

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
    start_screen()