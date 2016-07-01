# -*- coding: utf-8 -*-
# JSONify.py

import json
import sys

# Disorders => JSON <= CSV

def _disorders_to_json(disorder_list, out_file):

	# Taken from http://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file-in-python
	results = {}
	disorders_count = len(disorder_list)
	results['disorders'] = disorder_list
	results['count'] = disorders_count

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def _csv_to_json(csv_file, out_file):

	pass

def main(out_file):

	pass

if __name__ == '__main__':
	out_file_name = sys.argv[1]
	out_file = open(out_file_name, 'w')
	main(out_file)