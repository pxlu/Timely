# -*- coding: utf-8 -*-
# main.py

import json
import sys
import re
import parser
import uuid
import math
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

    return confidence_list

def _disorder_severities():

    for disorder in DISORDERS:
        disorder_severity = 0
        for symptom in disorder.symptoms:
            disorder_severity += float(SEVERITY[symptom])
        disorder.severity = disorder_severity

def _get_severity(user_profile):

    user_severity = 0
    for keyword, num_occurence in user_profile.keywords.items():
        user_severity += num_occurence * int(SEVERITY[keyword])

    return user_severity

def _parse_bio(in_file, out_file, profile_name):

    word_dict = parser.parse_text(in_file, out_file)
    print(word_dict)
    _disorder_severities()
    user_profile = UserProfile(name=str.capitalize(profile_name))

    # Filter by keywords only
    user_keywords = {element[0]: element[1] for element in word_dict.items() if element[0] in SEVERITY}

    # Fill in fields of user_profile
    user_profile.uid = uuid.uuid4()
    user_profile.keywords = user_keywords
    user_profile.severity = _get_severity(user_profile)
    user_profile.confidence = _disorder_confidence(user_profile)

    print(user_profile)
    for disorder in DISORDERS:
        print(disorder)
    #out_file.write(str(user_profile))

if __name__ == '__main__':
    try:
        in_file_name = sys.argv[1]
        out_file_name = sys.argv[2]
        profile_name = re.search('[A-Za-z]+\.md', in_file_name).group(0).split('.')[0]
        in_file = open(in_file_name, 'r')
        with open(out_file_name, 'w') as out_file: 
            _parse_bio(in_file, out_file, profile_name)
    except IndexError:
        print("Usage: `python main.py [inFile] [outFile]`")