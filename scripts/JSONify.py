# -*- coding: utf-8 -*-
# JSONify.py

import json
import sys
from screen import _init_disorders_list

def _convert_object(disorder_list, out_file):

	results = {}
	disorders_count = len(disorder_list)
	results['disorders'] = disorder_list
	results['count'] = disorders_count

	json.dump(results, out_file)

def main(out_file):

	_convert_object(disorder_list, out_file)

if __name__ == '__main__':
	out_file_name = sys.argv[1]
    out_file = open(out_file_name, 'w')
	main(out_file)