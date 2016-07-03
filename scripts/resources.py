# -*- coding: utf-8 -*-
# resources.py

# Native libraries
import sys
import json
# Custom libraries
import common 
import JSONify
import classes
import screen

RESOURCES = common._init_resource_list()
DISORDERS = common._init_disorder_list()

def _map_disorder_to_resources(disorder_name, resource_list):

	'''
	Return a list of resources that treat for a disorder.
	:param disorder_name: a name of a disorder
	:param resource_list: a list of resources
	:return: a list of resources from resource_list that treat disorder_name
	'''

	return [resource for resource in resource_list if disorder_name.lower() in resource.services]

def _calculate_compatibility(resource, resource_list, user_profile):

	'''
	Calculate the compatibility of a resource given a user profile.
	:param resource: a resource to be checked
	:param resource_list: a list of resources
	:user_profile: a profile of a user to be checked
	:return: the compatibility of the user with that resource, expressed as a percentage
	'''

	compatibility_value = 0
	for disorder in user_profile.disorders:
		treatment_places = _map_disorder_to_resources(disorder[0].name, resource_list)
		if resource in treatment_places:
			compatibility_value += 1

	compatibility_value = (compatibility_value / len(user_profile.disorders)) * 100

	return compatibility_value

def _get_total_compatibility(resource_list, user_profile):

	'''
	Return the total additive compatibility value of all resources in resource_list.
	:param resource: a resource to be checked
	:param resource_list: a list of resources
	:user_profile: a profile of a user to be checked
	:return: the compatibility of the user with all resources, expressed as a percentage
	'''

	total_compatibility_value = 0
	for resource in resource_list:
		resource_compatibility_value = _calculate_compatibility(resource, resource_list, user_profile)
		total_compatibility_value += resource_compatibility_value

	total_compatibility_value /= len(resource_list)

def _recommend_resource(resource, resource_list, user_profile):

	'''
	Return a boolean value of whether the resource for the given user_profile should be recommended or not.
	:param resource: a resource to be recommended
	:param resource_list: a list of resources to be recommended
	:user_profile: a profile of a user to be checked against
	:return: a tuple of (bool, value) indicating whether the resource is recommended or not and it's compatibility value with the user_profile
	'''

	# Currently, value is up in the air on what the threshold is to be recommended
	comp_value = _calculate_compatibility(resource, resource_list, user_profile)
	recommendation = True if comp_value > 0.33 else False

	return (recommendation, comp_value)

def _get_resources(in_file):

	user_profile = screen._get_profile(in_file, 'peter')
	rr = _recommend_resource(RESOURCES[0], RESOURCES, user_profile)
	print(rr)

if __name__ == '__main__':
	in_file_name = sys.argv[1]
	with open(in_file_name, 'r') as in_file:
		_get_resources(in_file)
