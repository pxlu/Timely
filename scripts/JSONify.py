# -*- coding: utf-8 -*-
# JSONify.py

import json
import sys
import csv
from classes import KeyWord

# Disorders => JSON <= CSV

def _disorders_to_json(disorder_list, out_file):

	# Taken from http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
	results = {}
	results['disorders'] = disorder_list
	results['count'] = len(disorder_list)

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _disorders_csv_to_json(csv_file_name, out_file):

	results = {}
	disorders_reader = csv.DictReader(open(csv_file_name))
	disorders_list = [KeyWord(name=row['Keyword'], description=row['Description']) for row in disorders_reader]
	results['disorders'] = disorders_list
	results['count'] = len(disorders_list)

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _resources_to_json():
	
	pass

def _resources_csv_to_json():

	pass

def main(out_file):

	pass

if __name__ == '__main__':
	csv_file_name = sys.argv[1]
	out_file_name = sys.argv[2]
	with open(out_file_name, 'w') as out_file:
		_disorders_csv_to_json(csv_file_name, out_file)