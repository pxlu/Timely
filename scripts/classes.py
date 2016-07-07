# -*- coding: utf-8 -*-
# classes.py

import json
import datetime
import uuid
import random

### Custom Exceptions

class InvalidInputException(Exception):
    pass

class QuitException(Exception):
    pass

### Custom Classes

class UserProfile:

    def __init__(self, uid=-1, name="", keywords={}, severity=-1, disorders=[]):
        self.uid = uid
        self.name = name
        self.keywords = keywords
        self.severity = severity
        self.disorders = disorders

    def __str__(self):
        disorders_return = [(disorder[0].name, disorder[1]) for disorder in self.disorders]
        return "UserID: {}\nUsername: {}\nKeywords: {}\nSeverity: {}\nDisorders: {}".format(
            self.uid, self.name, self.keywords, self.severity, disorders_return)

    def _generate_uid(self):

        return uuid.uuid4()

class KeyWord:

    def __init__(self, name="", description="", rating=-1):
        self.name = name
        self.description = description
        self.rating = rating
        
    def __str__(self):
        return "{} is a keyword, described as {}, with a serverity rating of {}.".format(self.name, self.description, self.rating)

class Disorder:

    def __init__(self, name="", dID=-1, symptoms=[], base_rate=-1, risk_factors = [], severity=-1):
        self.name = name
        self.dID = dID
        self.symptoms = symptoms
        self.base_rate = base_rate
        self.risk_factors = risk_factors
        self.severity = severity

    def __str__(self):
        return "{} is a mental health disorder described in the DSM-5. It has symptoms of {}, with a base rate of {}. It has risk factors of {} and has severity rating of {}.".format(self.name, self.symptoms, self.base_rate, self.risk_factors, self.severity)
	
    # Taken from http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
    def _to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def _generate_dID(self):

        pass

class Resource:

    def __init__(self, name="", rID=-1, resourcetype="", capacity="", location="", address=None, contact="", services=[], cost="", availibility=None):
        # Availbility should be a datetime object
        # Type should be hotline, specialist, etc
        # Capacity should be whether the resource accepts new patients or not
        self.name = name
        self.rID = rID
        self.type = resourcetype
        self.capacity = capacity
        self.location = location
        self.address = address
        self.contact = contact
        self.services = [service.lower() for service in services]
        self.cost = cost
        self.availibility = availibility

    def __str__(self):
        return "############################################ \
        \nName: {}\
        \nrID: {}\
        \nType: {}\
        \nCapacity: {}\
        \nLocation: {}\
        \nAddress: {}\
        \nContact: {}\
        \nServices: {}\
        \nCost: {}\
        \nAvailibility: {}\
        \n############################################".format(self.name, self.rID, self.resourcetype, self.capacity, self.location, self.address, self.contact, self.services, self.cost, self.availibility)

    def _generate_rID(self):

        pass