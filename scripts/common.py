# -*- coding: utf-8 -*-
# common.py

import json

KEYWORDS_MAPPING = "../json/keywords.json"
DISORDERS_MAPPING = "../json/disorders.json"

def _init_keywords():

    keyw_file = open(KEYWORDS_MAPPING)
    keyw_list = json.loads(keyw_file.read())['results']['keywords']
    keyw_ratings = {keyw_element['name']: keyw_element['rating'] for keyw_element in keyw_list}
    
    return keyw_ratings

def _init_disorders_list():

    disorders_file = open(DISORDERS_MAPPING)
    disorders_list = json.loads(disorders_file.read())['results']['disorders']
    disorders = [Disorder(name=disorder['name'],disid=disorder['id'],symptoms=[symptom for symptom in disorder['symptoms'].split(',')],base_rate=disorder['base_rate']) for disorder in disorders_list]

    return disorders
