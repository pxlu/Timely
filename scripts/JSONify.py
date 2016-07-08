# -*- coding: utf-8 -*-
# JSONify.py

import json
import sys
import csv
from timely_classes import KeyWord, Disorder, Resource

# Disorders => JSON <= CSV

def _disorders_to_json(disorders_list, out_file):

	# Taken from http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
	results = {}
	results['disorders'] = disorders_list
	results['count'] = len(disorders_list)

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _disorders_csv_to_json(csv_file_name, out_file):

	disorders_reader = csv.DictReader(open(csv_file_name))
	disorders_list = [Disorder(name=row['name'], symptoms=row['symptoms'], base_rate=row['base_rate'], risk_factors=row['risk_factors'], severity=row['severity']) for row in disorders_reader]

	_disorders_to_json(disorders_list, out_file)

# KeyWords => JSON <= CSV

def _keywords_to_json(keywords_list, out_file):

	results = {}
	results['keywords'] = keywords_list
	results['count'] = len(keywords_list)

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _keywords_csv_to_json(csv_file_name, out_file):

	keywords_reader = csv.DictReader(open(csv_file_name))
	keywords_list = [KeyWord(name=row['Keyword'], description=row['Description']) for row in keywords_reader]

	_keywords_to_json(keywords_list, out_file)

# Resources => JSON <= CSV

def _resources_to_json(resources_list, out_file):
	
	results = {}
	results['resources'] = resources_list
	results['count'] = len(resources_list)

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _resources_csv_to_json(csv_file_name, out_file):

	resources_reader = csv.DictReader(open(csv_file_name))
	resources_list = [Resource(name=row['name'], rID=row['id'], type=row['type'],capacity=row['capacity'], location=row['location'], address=row['address'] if row['address'] != '' else None, contact=row['contact'], services=row['services'], cost=row['cost'] if row['cost'] != ''else None, availibility=None) for row in resources_reader]

	_resources_to_json(resources_list, out_file)

if __name__ == '__main__':
	csv_file_name = sys.argv[1]
	out_file_name = sys.argv[2]
	with open(out_file_name, 'w') as out_file:
		_disorders_csv_to_json(csv_file_name, out_file)