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

RESOURCES = common._init_resources_list()
DISORDERS = common._init_disorders_list()

def _map_disorder_to_resources(disorder_name, resources_list):

	'''
	Return a list of resources that treat for a disorder.
	:param disorder_name: a name of a disorder
	:resources_list: a list of resources
	'''

	return [resource for resource in resources_list if disorder_name.lower() in resource.services]

def _get_resources(in_file):

	user_profile = screen._get_profile(in_file, 'peter')
	for disorder in user_profile.disorders:
		places = _map_disorder_to_resources(disorder[0].name, RESOURCES)

if __name__ == '__main__':
	in_file_name = sys.argv[1]
	with open(in_file_name, 'r') as in_file:
		_get_resources(in_file)
