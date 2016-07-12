# timely_classes.py

# Native Python Libraries
import uuid
# Third Party Libraries
from collections import OrderedDict
# Local Libraries

### Custom Exceptions

class InvalidInputException(Exception):
    pass

class QuitException(Exception):
    pass

### Custom Classes

class UserProfile(object):

    """
    A profile of a user, with a unique userid, a unique username, a collection of keywords parsed from the user's bio, the severity rating of the user, and collection of possible disorders that the user may have, along with the confidence.

    :field uid:         (type: `str`) the user id of the profile
    :field name:        (type: `str`) the user name of the profile
    :field keywords:    (type: `dict`) a collection of keywords parsed from the user's bio 
    :field severity:    (type: `int`) a severity rating based off of the user's keywords
    :field disorders:   (type: `list`) a collection of possible disorders and their confidence values
    """

    def __init__(self, uid=-1, name="", keywords={}, severity=-1, disorders=[]):
        self.uid = uid
        self.name = name
        #not equivalent to keywords that are symptoms. is instead parsed words from user bio
        self.keywords = keywords 
        # Severity rating to be used for graph
        self.severity = severity
        # List of disorders and the probability of the user having it
        self.disorders = disorders 

    def __str__(self):
        disorders_return = [(disorder[0].name, disorder[1]) for disorder in self.disorders]
        return "UserID: {}\nUsername: {}\nKeywords: {}\nSeverity: {}\nDisorders: {}".format(
            self.uid, self.name, self.keywords, self.severity, disorders_return)

    def _generate_uid(self):

        """
        Returns a unique uuid, to be used as the user id.

        :return (type: `str`) an unique user id
        """

        return uuid.uuid4()

class KeyWord(object):

    """
    A keyword object representing a symptom or condition, with a unique name, description, and a rating.

    :field name:        (type: `str`) the name of the keyword
    :field description: (type: `str`) the description for the keyword
    :field rating:      (type: `int`) the severity rating for the keyword
    """

    def __init__(self, name="", description="", rating=-1):
        self.name = name
        self.description = description
        self.rating = rating
        
    def __str__(self):
        return "{} is a keyword, described as {}, with a serverity rating of {}.".format(self.name, self.description, self.rating)

class Disorder(object):

    """
    A disorder object representing a mental health disorder, with an unique name, an unique disorder id, a collection of symptoms, a base rate, a collection of risk factors, and a severity rating.

    :field name:            (type: `str`) the name of the disorder
    :field dID:             (type: `str`) the id of the disorder
    :field symptoms:        (type: `list`) the symptoms of the disorder
    :field base_rate:       (type: `float`) the base rate of the disorder
    :field risk_factors:    (type: `list`) the risk factors of the disorder
    :field severity:        (type: `int`) the severity rating of the disorder
    """

    def __init__(self, name="", dID=-1, symptoms=[], base_rate=0.0, risk_factors = [], severity=-1):
        self.name = name
        self.dID = dID
        self.symptoms = symptoms
        self.base_rate = base_rate
        self.risk_factors = risk_factors
        # Severity rating as a constraint for graph algo
        self.severity = severity

    def __str__(self):
        return "{} is a mental health disorder described in the DSM-5. It has symptoms of {}, with a base rate of {}. It has risk factors of {} and has severity rating of {}.".format(self.name, self.symptoms, self.base_rate, self.risk_factors, self.severity)

    def _generate_dID(self):

        """
        Returns a unique uuid, to be used as the disorder id.

        :return (type: `str`) an unique disorder id
        """

        return uuid.uuid4()

class Resource(object):

    """
    A resource object representing a mental health resource, with an unique name, an unique rID, a resource type, a capacity, a location, an address, a contact, a collection of services, a cost, and availability as an OperatingHours object.

    :field name:            type(`str`) the name of the resource
    :field rID:             type(`str`) the id of the resource
    :field resourcetype:    type(`str`) the type of the resource
    :field capacity:        type(`str`) the capacity of the resource
    :field location:        type(`str`) the location of the resource
    :field address:         type(`str`) the address of the resource
    :field contact:         type(`str`) the contact information of the resource
    :field services:        type(`list`) the services provided by the resource
    :field cost:            type(`str`) the cost of the resource
    :field availability:    type(`OperatingHours`) the availability of the resource
    """

    def __init__(self, name="", rID=-1, resourcetype="", capacity="", location="", address=None, contact="", services=[], cost="", availability=None):
        # Availbility should be a datetime object
        # Type should be hotline, specialist, etc
        # Capacity should be whether the resource accepts new patients or not
        self.name = name
        self.rID = rID
        self.resourcetype = resourcetype
        self.capacity = capacity
        self.location = location
        self.address = address
        self.contact = contact
        self.services = [service.lower() for service in services]
        self.cost = cost
        # Custom object that tells operating hours of such a resource(clinic)
        self.availability = availability

    def __str__(self):
        return "============================================= \
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
        \n=============================================".format(self.name, self.rID, self.resourcetype, self.capacity, self.location, self.address, self.contact, self.services, self.cost, self.availibility)

    def _generate_rID(self):

        """
        Returns a unique uuid, to be used as the resource id.

        :return (type: `str`) an unique resourcd id
        """

        return uuid.uuid4()

class OperatingHours:

    """
    A operating hours object representing the operating hours of a resource, with a dictionary of time objects.

    :field day_order:   type(`list`) the order of the days
    :field oph_dict:    type(`OrderedDict`) the dict of time objects
    """

    def __init__(self, oph_dict={}):

        self.day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        # oph stands for (Op)erating (H)ours
        self.oph_dict = OrderedDict(sorted(oph_dict.items(), key=lambda item: self.day_order.index(item[0])))

    def __str__(self):

        output = "\n==============================\n"

        for day, hours in self.oph_dict.items():

            opening_time_int = int(str(hours[0].tm_hour) + str(hours[0].tm_min))
            closing_time_int = int(str(hours[1].tm_hour) + str(hours[1].tm_min))

            if ((closing_time_int - opening_time_int) == 0):
                output += day + ": Closed\n"
            elif ((closing_time_int - opening_time_int) == 2359):
                output += day + ": Open 24 Hours\n"
            else:
                timestring = str(hours[0].tm_hour) + ":" + str(hours[0].tm_min).rjust(2, '0') + "-" + str(hours[1].tm_hour) + ":" + str(hours[1].tm_min).rjust(2, '0')  + "\n"
                output += day + ": " + timestring

        return output[:-1]
