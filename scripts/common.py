# -*- coding: utf-8 -*-
# common.py

import json
from classes import *

KEYWORDS_MAPPING = "../json/keywords.json"
DISORDERS_MAPPING = "../json/disorders.json"
RESOUCES_MAPPING = "../json/resources.json"

def _init_keyword_list():

    keyw_file = open(KEYWORDS_MAPPING)
    keyw_list = json.loads(keyw_file.read())['results']['keywords']
    keyw_ratings = [KeyWord(name=keyw_element['name'],description=keyw_element['description'],rating=keyw_element['rating']) for keyw_element in keyw_list]
    
    return keyw_ratings

def _get_keywords(keywords_list):

	keyword_names = [keyword.name for keyword in keywords_list]

	return keyword_names

def _init_disorder_list():

    disorders_file = open(DISORDERS_MAPPING)
    disorders_list = json.loads(disorders_file.read())['results']['disorders']

    disorders = [Disorder(name=disorder['name'],dID=disorder['id'],symptoms=[symptom for symptom in disorder['symptoms'].split(',')],base_rate=disorder['base_rate']) for disorder in disorders_list]

    return disorders

def _init_resource_list():

	resources_file = open(RESOUCES_MAPPING)
	resources_list = json.loads(resources_file.read())['results']['resources']

	# Availibility is None until I figure out how to make a correct datetime object list
	resources = [Resource(name=resource['name'], rID=resource['id'], type=resource['type'],capacity=resource['capacity'], location=resource['location'], address=resource['address'] if resource['address'] != '' else None, contact=resource['contact'], services=resource['services'], cost=resource['cost'] if resource['cost'] != ''else None, availibility=None) for resource in resources_list]

	return resources
