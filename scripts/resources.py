# -*- coding: utf-8 -*-
# resources.py

# Native libraries
import sys
import json
# Custom libraries
from screen import _get_profile
import common
import classes
import JSONify

RESOUCES = common._init_resources_list()

def _get_resources():

	pass

if __name__ == '__main__':
	in_file_name = sys.argv[1]
	with open(in_file_name, 'r') as in_file:
		_get_resources(in_file)
