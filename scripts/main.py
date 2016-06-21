# -*- coding: utf-8 -*-
# main.py

import json
import sys
import re
import parser

SEVERITY_MAPPING = "../json/severity.json"

class UserProfile:

    def __init__(self, userid=-1, username="", keywords={}, severity=-1, symptoms=[]):
        self.userid = userid
        self.username = username
        self.keywords = keywords
        self.severity = severity
        self.symptoms = symptoms

    def __str__(self):
        return "UserID: {}\nUsername: {}\nKeywords: {}\nSeverity: {}\nSymptoms: {}".format(
            self.userid, self.username, self.keywords, self.severity, self.symptoms)

def _init_severity():

    sev_file = open(SEVERITY_MAPPING)
    sev_dict = json.loads(sev_file.read())['keywords']
    sev_ratings = {sev_element['name']: sev_element['rating'] for sev_element in sev_dict.values()}
    return sev_ratings

SEVERITY = _init_severity()

def _get_severity(user_profile):

    user_severity = 0
    for keyword, num_occurence in user_profile.keywords.items():
        user_severity += num_occurence * int(SEVERITY[keyword])

    return user_severity

def _parse_bio(in_file, out_file, profile_name):

    word_dict = parser.parse_text(in_file, out_file)
    user_profile = UserProfile(username=str.capitalize(profile_name))

    # Fill in fields of user_profile
    user_keywords = {element[0]: element[1] for element in word_dict.items() if element[0] in SEVERITY}
    user_profile.keywords = user_keywords
    user_profile.severity = _get_severity(user_profile)

    print(user_profile)

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