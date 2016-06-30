# -*- coding: utf-8 -*-
# JSONify.py

import json
import sys
import pprint
from screen import _init_disorders_list

def _convert_objects(disorder_list, out_file):

	results = {}
	disorders_count = len(disorder_list)
	results['disorders'] = disorder_list
	results['count'] = disorders_count

	json.dump(results, out_file, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def main(out_file):

	DISORDERS = _init_disorders_list()
	_convert_object(DISORDERS, out_file)

if __name__ == '__main__':
	out_file_name = sys.argv[1]
	out_file = open(out_file_name, 'w')
	main(out_file)