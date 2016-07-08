# -*- coding: utf-8 -*-
# common.py

# Native
import json
import time

# Local
from timely_classes import *

KEYWORDS_MAPPING = "../json/keywords.json"
DISORDERS_MAPPING = "../json/disorders.json"
RESOUCES_MAPPING = "../json/resources.json"

def _init_keyword_list():

    keyw_file = open(KEYWORDS_MAPPING)
    keyw_list = json.loads(keyw_file.read())['results']['keywords']
    keyw_ratings = [KeyWord(
        name=keyw_element['name'],
        description=keyw_element['description'],
        rating=keyw_element['rating']
        ) for keyw_element in keyw_list]
    
    return keyw_ratings

def _get_keywords(keywords_list):

	keyword_names = [keyword.name for keyword in keywords_list]

	return keyword_names

def _init_disorder_list():

    disorders_file = open(DISORDERS_MAPPING)
    disorders_list = json.loads(disorders_file.read())['results']['disorders']

    disorders = [Disorder(
        name=disorder['name'],
        dID=disorder['id'],
        symptoms=[symptom for symptom in disorder['symptoms'].split(',')],
        base_rate=disorder['base_rate']
        ) for disorder in disorders_list]

    return disorders

def _init_resource_list():

    resources_file = open(RESOUCES_MAPPING)
    resources_list = json.loads(resources_file.read())['results']['resources']

    resources = [Resource(
        name=resource['name'], 
        rID=resource['id'], 
        resourcetype=resource['type'], 
        capacity=resource['capacity'], 
        location=resource['location'], 
        address=resource['address'] if resource['address'] != '' else None,
        contact=resource['contact'], 
        services=resource['services'], 
        cost=resource['cost'] if resource['cost'] != ''else None,
        availibility=OperatingHours(oph_dict=_init_OperatingHours_dict(resource['availibility']))
        ) for resource in resources_list]

    return resources

def _init_OperatingHours_dict(availibility_dict):

    '''
    Returns an intialized dictionary of converted json to time objects. Intended for the OperatingHours class.

    :param availibility_dict: 
    :return a dictionary of {String: time}
    '''

    op_hours_dict_out = {}
    for op_hours in availibility_dict.items():
        if op_hours[1] == "24 Hours".lower():
            #incomplete. need to convert to time objects
            op_hours_dict_out[op_hours[0]] = (time.strptime("0", "%H"), time.strptime("23 59", "%H %M"))
        elif op_hours[1] == "":
            op_hours_dict_out[op_hours[0]] = (time.strptime("0", "%H"), time.strptime("0", "%H"))
        else:
            splitstring = op_hours[1].replace(":"," ").split('-')
            op_hours_dict_out[op_hours[0]] = (time.strptime(splitstring[0], "%H %M"), time.strptime(splitstring[1], "%H %M"))

    return op_hours_dict_out