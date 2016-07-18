# -*- coding: utf-8 -*-
# common.py

# Native Python Libraries
import json
import time
import os
# Third Party Libraries
# Local Libraries
from timely_classes import *

# Current working directory
_cwd = os.path.dirname(os.path.realpath(__file__))

def _init_keyword_list(path="/../json/keywords.json"):

    """
    Initialize a list of keyword objects from the given json file.

    :param path: the path to the json file
    :return the list of keyword objects represented in the json file
    """

    keyw_file = open(_cwd + path)
    keyw_list = json.loads(keyw_file.read())["results"]["keywords"]
    keyw_ratings = [KeyWord(
        name=keyw_element["name"],
        description=keyw_element["description"],
        rating=keyw_element["rating"]
        ) for keyw_element in keyw_list]
    
    return keyw_ratings

def _get_keywords(keywords_list):

    """
    Return the names of the keyword objects in keywords_list.

    :param keywords_list: a list of keyword objects to be parsed
    :return a list of keyword names corresponding to the keywords in keywords_list
    """

    keyword_names = [keyword.name for keyword in keywords_list]

    return keyword_names

def _init_disorder_list(path="/../json/disorders.json"):

    """
    Initialize a list of disorder objects from the given json file.

    :param path: the path to the json file
    :return the list of disorder objects represented in the json file
    """

    disorders_file = open(_cwd + path)
    disorders_list = json.loads(disorders_file.read())["results"]["disorders"]

    disorders = [Disorder(
        name=disorder["name"],
        dID=disorder["id"],
        symptoms=[symptom for symptom in disorder["symptoms"].split(",")],
        base_rate=disorder["base_rate"]
        ) for disorder in disorders_list]

    return disorders

def _init_resource_list(path="/../json/resources.json"):

    """
    Initialize a list of resource objects from the given json file.

    :param path: the path to the json file
    :return the list of resource objects represented in the json file
    """

    resources_file = open(_cwd + path)
    resources_list = json.loads(resources_file.read())["results"]["resources"]

    resources = [Resource(
        name=resource["name"], 
        rID=resource["id"], 
        resourcetype=resource["type"], 
        capacity=resource["capacity"], 
        location=resource["location"], 
        address=resource["address"] if resource["address"] != "" else None,
        contact=resource["contact"], 
        services=resource["services"], 
        cost=resource["cost"] if resource["cost"] != "" else None,
        availability=OperatingHours(oph_dict=_init_OperatingHours_dict(resource["availability"]))
        ) for resource in resources_list]

    return resources

def _init_OperatingHours_dict(availibility_dict):

    """
    Returns an intialized dictionary of converted json to time objects. Intended for the OperatingHours class.

    :param availibility_dict: a dictionary of strings to be parsed into time objects
    :return a dictionary of {String: (time, time)}
    """

    op_hours_dict_out = {}
    for op_hours in availibility_dict.items():
        if op_hours[1] == "24 Hours".lower():
            op_hours_dict_out[op_hours[0]] = (time.strptime("0", "%H"), time.strptime("23 59", "%H %M"))
        elif op_hours[1] == "":
            op_hours_dict_out[op_hours[0]] = (time.strptime("0", "%H"), time.strptime("0", "%H"))
        else:
            timetuple = op_hours[1].replace(":"," ").split("-")
            op_hours_dict_out[op_hours[0]] = (time.strptime(timetuple[0], "%H %M"), time.strptime(timetuple[1], "%H %M"))

    return op_hours_dict_out