# -*- coding: utf-8 -*-
# JSONify.py

import json
import sys
import csv
from classes import KeyWord, Disorder, Resource

# Disorders => JSON <= CSV

def _disorders_to_json(disorder_list, out_file):

	# Taken from http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
	results = {}
	results['disorders'] = disorder_list
	results['count'] = len(disorder_list)

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _disorders_csv_to_json(csv_file_name, out_file):

	pass

def _keywords_to_json(keywords_list, out_file)

def _keywords_csv_to_json(csv_file_name, out_file):

	results = {}

	keywords_reader = csv.DictReader(open(csv_file_name))
	keywords_list = [KeyWord(name=row['Keyword'], description=row['Description']) for row in keywords_reader]

	results['keywords'] = keywords_list
	results['count'] = len(keywords_list)

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _resources_to_json():
	
	pass

def _resources_csv_to_json():

	pass

if __name__ == '__main__':
	csv_file_name = sys.argv[1]
	out_file_name = sys.argv[2]
	with open(out_file_name, 'w') as out_file:
		_disorders_csv_to_json(csv_file_name, out_file)